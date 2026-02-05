from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.message import Message


class MessageDatabase(BaseDatabase[Message]):
    collection_name = "messages"
    model = Message

    def __init__(self):
        super().__init__()
