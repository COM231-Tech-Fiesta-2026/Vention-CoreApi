from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from ...models.summary_model import Summary


class SummaryDatabase(BaseDatabase[Summary]):
    collection_name = "summaries"
    model = Summary
