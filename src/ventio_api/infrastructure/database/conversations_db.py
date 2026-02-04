from base_database import BaseDatabase
from ventio_api.api.schema.converstation import Converstation

class ConverstationDatabase(BaseDatabase[Converstation]):
	collection_name = "converstations"
	model = Converstation