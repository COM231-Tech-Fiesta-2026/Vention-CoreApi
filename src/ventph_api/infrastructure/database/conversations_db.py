from base_database import BaseDatabase
from ventph_api.api.schema.converstation import Converstation

class ConverstationDatabase(BaseDatabase[Converstation]):
	collection_name = "converstations"
	model = Converstation

convo_db = ConverstationDatabase()