from typing import Any, Optional
from datetime import datetime
from src.ventio_api.core.utils import calculate_age, format_db_id, to_mongo_dict
from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.user import UserSignup, UserUpdate
from src.ventio_api.models.user import User
from src.ventio_api.exceptions import NotFoundException, DatabaseException
from src.ventio_api.infrastructure.auth.security import get_password_hash

class UserDatabase(BaseDatabase[User]):
    collection_name = "users"
    model = User

    async def insert(self, user: User) -> User:
        try:
            user_dict = user.model_dump()
            if user_dict.get("birthday"):
                user_dict["birthday"] = datetime.combine(user_dict["birthday"], datetime.min.time())

            result = self.collection.insert_one(user_dict)
            
            return user
        except Exception as e:
            raise DatabaseException(f"Failed to insert user: {str(e)}") from e

    async def get(self, **query: Any) -> User:
        """
        Overriding the base get to handle the synchronous MongoClient 
        while keeping the interface asynchronous for the service layer.
        """
        try:
            query = self.normalize(query) 
            doc = self.collection.find_one(query)
            
            if not doc:
                raise NotFoundException(f"User not found. Query: {query}")
            
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)
            return self.model(**doc)
        except NotFoundException:
            raise
        except Exception as e:
            print(f"DEBUG: Internal Override Error: {e}")
            raise DatabaseException(f"Database error: {str(e)}") from e

    async def get_by_username(self, username: str) -> User:
        return await self.get(username=username)

    async def get_user_by_id(self, user_id: str) -> User:
        return await self.get(_id=format_db_id(user_id))

    async def update_user_by_id(self, user_id: str, updates: UserUpdate):
        update_data = updates.model_dump(exclude_unset=True)
        
        if "birthday" in update_data and update_data["birthday"]:
            update_data["age"] = calculate_age(update_data["birthday"])           
        if update_data:
            return await self.partial_update(
                set=update_data, 
                _id=format_db_id(user_id)
            )
        
    async def partial_update(
        self,
        set: Optional[dict[Any, Any]] = None,
        push: Optional[dict[Any, Any]] = None,
        **query: Any,
    ) -> User:
        try:
            update_operations: dict[str, dict[Any, Any]] = {}
            if set is not None:
                normalized_set = self.normalize(set)
                update_operations["$set"] = to_mongo_dict(normalized_set)
                
            if push is not None:
                update_operations["$push"] = to_mongo_dict(self.normalize(push))
            result = self.collection.update_one(query, update_operations)
            
            if result.matched_count == 0:
                raise NotFoundException(f"Failed to update {self.model}. Query: {query}")
            return await self.get(**query)
            
        except Exception as e:
            print(f"DEBUG: Partial Update Error: {e}")
            raise DatabaseException(f"Database error: {str(e)}") from e

users_db = UserDatabase()