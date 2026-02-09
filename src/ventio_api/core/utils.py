from datetime import date, datetime
from typing import Any, Union
from bson import ObjectId
from datetime import datetime, timezone
import uuid


def calculate_age(birthday: Union[date, str]) -> int:
    """
    Calculates age from a date object or a YYYY-MM-DD string.
    """
    if isinstance(birthday, str):
        birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
    today = date.today()

    return (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )


def to_mongo_dict(data: dict[str, Any]) -> dict[str, Any]:
    """
    Converts date objects to datetime objects so PyMongo can encode them.
    """
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            data[key] = datetime.combine(value, datetime.min.time())
    return data


def format_db_id(id_val: Any) -> Union[ObjectId, uuid.UUID, str]:
    """
    Standardizes IDs for MongoDB queries.
    Handles legacy ObjectIds, new UUIDs, and raw strings.
    """
    if not isinstance(id_val, str):
        return id_val

    if len(id_val) == 24:
        try:
            return ObjectId(id_val)
        except Exception:
            pass

    try:
        return uuid.UUID(id_val)
    except (ValueError, TypeError):
        pass

    return id_val


def get_now():
    return datetime.now(timezone.utc).isoformat()
