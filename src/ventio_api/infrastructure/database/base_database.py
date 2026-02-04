from enum import Enum
from typing import Any, Generic, Optional, Type, TypeVar
from pydantic import BaseModel

# from .mongo import db
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from ...config import env
from ...exceptions import DatabaseException, DuplicateException, NotFoundException

client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
    env.MONGODB_LOCAL_URL, uuidRepresentation="standard"
)
db = client["iconnect"]

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseDatabase(Generic[ModelType]):
    """
    A generic Object Data Mapper (ODM) base class for MongoDB collections.

    This class provides a type-safe interface for common CRUD operations on MongoDB
    collections. It cannot be used directly and must be subclassed with a specific
    Pydantic model and collection name.

    The class handles automatic serialization/deserialization between Pydantic models
    and MongoDB documents, including normalization of Enum values and MongoDB ObjectId
    conversions.

    Type Parameters:
        ModelType: A Pydantic BaseModel subclass that defines the schema for documents
                   in the collection.

    Attributes:
        collection_name (str): The name of the MongoDB collection. Must be set in subclass.
        model (Type[ModelType]): The Pydantic model class. Must be set in subclass.
        collection: The PyMongo collection instance.

    Example:

        class OrganizationDatabase(BaseDatabase[Organization]):
            collection_name = "organizations"
            model = Organization

        # Usage
        org_db = OrganizationDatabase()
        org = org_db.get(organization_id="org-123")


    Raises:
        ValueError: If collection_name or model is not set in the subclass.
        DatabaseException: For general database operation errors.
        DuplicateException: When inserting a document violates a unique constraint.
        NotFoundException: When a queried document is not found.

    Note:
        Both collection_name and model must be defined as class attributes in
        any subclass before instantiation.
    """

    collection_name: str
    model: Type[ModelType]

    async def __init__(self):
        if not hasattr(self, "collection_name"):
            raise ValueError("collection_name must be set")
        if not hasattr(self, "model"):
            raise ValueError("model class must be defined")

        self.collection = db[self.collection_name]

    async def insert(self, item: ModelType) -> ModelType:
        """
        Insert a new document into the collection.

        Serializes the Pydantic model to a dictionary, normalizes Enum values,
        and inserts it into MongoDB.

        Args:
            item (ModelType): The Pydantic model instance to insert.

        Returns:
            ModelType: The inserted item (same as input).

        Raises:
            DuplicateException: If the document violates a unique constraint.
            DatabaseException: If any other database error occurs.
        """
        try:
            data = item.model_dump()
            data = self.normalize(data)
            self.collection.insert_one(data)
            return item
        except DuplicateKeyError as e:
            raise DuplicateException from e
        except Exception as e:
            raise DatabaseException from e

    async def get(self, **query: Any) -> ModelType:
        """
        Retrieve a single document from the collection matching the query.

        Queries the collection and deserializes the first matching document into
        a Pydantic model instance. Converts MongoDB's _id to a string 'id' field.

        Args:
            **query: Keyword arguments to filter the query. Field names should match
                    the model's field names. Values can include Enums which will be
                    normalized to their values.

        Returns:
            ModelType: The Pydantic model instance representing the found document.

        Raises:
            NotFoundException: If no document matches the query.
            DatabaseException: If any other database error occurs.

        Example:

            user = user_db.get(email="user@example.com")
            org = org_db.get(organization_id="org-123")

        """
        try:
            query = self.normalize(query)
            doc = self.collection.find_one(query)
            if not doc:
                raise NotFoundException(f"{self.model} not found. Query: {query}")
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)
            return self.model(**doc)
        except NotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseException from e

    async def get_many(self, **query: Any) -> list[ModelType]:
        """
        Retrieve multiple documents from the collection matching the query.

        Queries the collection and deserializes all matching documents into a list
        of Pydantic model instances. If no query is provided, returns all documents.
        Sorting can be applied based on specified fields.

        Args:
            **query: Keyword arguments to filter the query. Field names should match
                    the model's field names. If empty, retrieves all documents.
                    Special keyword 'sort': Optional[list[tuple[str, int]]] - sort criteria
                                           as a list of (field, direction) tuples.

        Returns:
            list[ModelType]: A list of Pydantic model instances. Returns an empty
                           list if no documents match.

        Raises:
            DatabaseException: If a database error occurs.

        Example:

            # Get all users
            all_users = user_db.get_many()

            # Get users by organization
            org_users = user_db.get_many(organization_id="org-123")

            # Get users by role
            admins = user_db.get_many(role=UserRole.ADMIN)

            # Get users with sorting
            sorted_users = user_db.get_many(organization_id="org-123", sort=[("created_at", -1)])

        """
        try:
            sort = query.pop("sort", None)
            filter = query.pop("filter", {})
            query_normalized = self.normalize(query)
            if filter:
                query_normalized = {"$and": [query_normalized, self.normalize(filter)]}

            if sort:
                docs = self.collection.find(query_normalized).sort(sort)
            else:
                docs = self.collection.find(query_normalized)

            models: list[ModelType] = []
            for doc in docs:
                doc["id"] = str(doc["_id"])
                doc.pop("_id", None)
                model = self.model(**doc)
                models.append(model)

            return models
        except Exception as e:
            raise DatabaseException from e

    async def search(
        self, search_term: str, search_fields: list[str], **additional_filters: Any
    ) -> list[ModelType]:
        """
        Search for documents using fuzzy text matching across specified fields.

        Uses MongoDB's regex search with case-insensitive matching to find documents
        where any of the specified fields contain the search term. Supports additional
        filters to narrow results.

        Args:
            search_term (str): The text to search for (partial matches allowed).
            search_fields (list[str]): List of field names to search within.
            **additional_filters: Additional query filters (e.g., organization_id).

        Returns:
            list[ModelType]: List of matching documents as Pydantic models.

        Example:

            # Search users by name or email within an organization
            results = user_db.search(
                search_term="john",
                search_fields=["full_name", "email"],
                organization_id="org-123"
            )

        """
        try:
            regex_pattern = {"$regex": search_term, "$options": "i"}

            or_conditions = [{field: regex_pattern} for field in search_fields]

            query: dict[str, Any] = {"$and": [{"$or": or_conditions}]}

            if additional_filters:
                normalized_filters = self.normalize(additional_filters)
                for key, value in normalized_filters.items():
                    query["$and"].append({key: value})

            docs = self.collection.find(query)

            models: list[ModelType] = []
            for doc in docs:
                doc["id"] = str(doc["_id"])
                doc.pop("_id", None)
                model = self.model(**doc)
                models.append(model)

            return models
        except Exception as e:
            raise DatabaseException from e

    async def update(self, item: ModelType, **query: Any) -> ModelType:
        """
        Update a document in the collection matching the query.

        Uses MongoDB's $set operator to update only the fields present in the item.
        Updates only the first document that matches the query.

        Args:
           item (ModelType): The Pydantic model instance with updated values.
            **query: Keyword arguments to identify which document to update.

        Returns:
            ModelType: The updated item (same as input).

        Raises:
            NotFoundException: If no document matches the query.
            DatabaseException: If any other database error occurs.

        Example:

            # Update user by email
            updated_user = user_db.update(user, email="user@example.com")

            # Update organization by ID
            updated_org = org_db.update(org, organization_id="org-123")

        """
        try:
            data = item.model_dump()
            data = self.normalize(data)
            query = self.normalize(query)
            result = self.collection.update_one(query, {"$set": data})
            if result.matched_count == 0:
                raise NotFoundException(
                    f"Failed to update {self.model}. Query: {query}"
                )
            return item
        except NotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseException from e

    async def partial_update(
        self,
        set: Optional[dict[Any, Any]] = None,
        push: Optional[dict[Any, Any]] = None,
        **query: Any,
    ) -> ModelType:
        try:
            update_operations: dict[str, dict[Any, Any]] = {}
            if set is not None:
                set = self.normalize(set)
                update_operations["$set"] = set
            if push is not None:
                push = self.normalize(push)
                update_operations["$push"] = push

            result = self.collection.update_one(query, update_operations)
            if result.matched_count == 0:
                raise NotFoundException(
                    f"Failed to update {self.model}. Query: {query}"
                )

            model = self.get(**query)
            return model
        except NotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseException from e

    async def delete(self, **query: Any) -> list[ModelType]:
        """
        Delete all documents from the collection matching the query.

        Retrieves the documents before deletion to return them. Deletes all
        documents that match the query criteria.

        Args:
            **query: Keyword arguments to identify which documents to delete.

        Returns:
            list[ModelType]: A list of the deleted Pydantic model instances.

        Raises:
            NotFoundException: If no documents match the query.
            DatabaseException: If any other database error occurs.

        Example:

            # Delete a specific user
            deleted_users = user_db.delete(email="user@example.com")

            # Delete all users in an organization
            deleted = user_db.delete(organization_id="org-123")


        Warning:
            This method deletes ALL documents matching the query. Be careful when
            using broad queries to avoid unintended deletions.
        """
        try:
            query = self.normalize(query)
            deleted = self.get_many(**query)
            result = self.collection.delete_many(query)
            if result.deleted_count == 0:
                raise NotFoundException(
                    f"Failed to delete {self.model}. Query: {query}"
                )

            return deleted
        except NotFoundException as e:
            raise
        except Exception as e:
            raise DatabaseException from e

    async def normalize(self, doc: dict[Any, Any]) -> dict[Any, Any]:
        """
        Normalize a dictionary by converting Enum and HttpUrl values to their primitive values.

        This ensures that Enum instances and HttpUrl instances are properly serialized for
        MongoDB storage and queries. All other values are passed through unchanged.

        Args:
            doc (dict[Any, Any]): The dictionary to normalize, typically from
                                 model_dump() or query parameters.

        Returns:
            dict[Any, Any]: A new dictionary with Enum values converted to their
                          underlying values (strings, ints, etc.) and HttpUrl
                          values converted to strings.

        Example:

            # Before: {"role": UserRole.ADMIN, "name": "John", "url": HttpUrl("https://example.com")}
            # After:  {"role": "admin", "name": "John", "url": "https://example.com/"}

        """
        from pydantic import HttpUrl

        out: dict[Any, Any] = {}
        for k, v in doc.items():
            if isinstance(v, Enum):
                out[k] = v.value
            elif isinstance(v, HttpUrl):
                out[k] = str(v)
            else:
                out[k] = v
        return out
