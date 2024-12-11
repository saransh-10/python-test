import uuid
import traceback
from azure.cosmos import CosmosClient, ContainerProxy


class COSMOS_DB:
    def __init__(self):
        # ! TODO: Remove these credentials
        self.cosmos_endpoint  = "https://cosmos-hayya-dev-we-001.documents.azure.com:443/"
        self.cosmos_key       = "ENl4eZt1CXuBkjyPdK6QBNyUoeGDVD6XTMMolFlKyFtta6RPpSYqJsrk9yQBeaivjTQkfKLHwlt1ACDbPQP02g=="
        self.cosmos_database  = "dev-test-db"
        self.cosmos_container = "con01"
        self.cosmos_database_faqs = "dashboard_faqs"
        self.cosmos_container_faqs = "items"

    def _get_container_client(self, database_name: str, container_name: str) -> ContainerProxy:
        client    = CosmosClient(self.cosmos_endpoint, self.cosmos_key)
        database  = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        return container
    
    def _add_conversation_item(self, user_email: str, conv_id: str, question_type: str, item: dict) -> bool:
        details = {
            "id": uuid.uuid4().hex,
            "partitionKey": user_email,
            "conv_id": conv_id,
            "question_type": question_type
        }

        try:
            self._get_container_client(database_name = self.cosmos_database, container_name = self.cosmos_container).upsert_item({**details, **item})
            return True
        except Exception as ex:
            tb = traceback.format_exc()
            print(f"Error adding conversation item: {str(ex)} Traceback:\n{tb}")
            # logger.log(msg=f"Error adding conversation item: {str(ex)}", level=logging.ERROR)
            return False

cosmos = COSMOS_DB()
containers = cosmos._get_container_client("dev-test-db", "con01")
print("Created")