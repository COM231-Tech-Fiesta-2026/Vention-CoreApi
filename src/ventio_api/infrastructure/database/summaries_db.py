from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.summary import Summary

class SummaryDatabase(BaseDatabase[Summary]):
	collection_name = "summaries"
	model = Summary