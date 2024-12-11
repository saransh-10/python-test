import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from azure_openai import azure_openai
import logging
import time

azure_openai = azure_openai.OpenAIHandler()

class AZCognitiveSearch:
    def __init__(self) -> None:
        # ! Have to remove these credentials
        self.endpoint       = "https://srch-hayya-dev-we-001.search.windows.net"
        self.key            =  "U4mzBIczgkCjlxxwGRBFtIgCC85Biin0yiTm7R9nvUAzSeAmpMyC"
        self.index_name_sql = "sql-hayya-databricks-indexer"

    def azure_vector_search(self,  final_query: str, select: list[str]):
        start = time.time()
        vector_query = VectorizedQuery(
            vector              = azure_openai.openai_embeddings(final_query),
            k_nearest_neighbors = 5,
            fields              = "contentVector"
        )
        
        index_name = self.index_name_sql

        search_client = SearchClient(
            endpoint   = self.endpoint,
            index_name = index_name,
            credential = AzureKeyCredential(self.key)
        )
        
        results = search_client.search(  
            search_text    = final_query,  
            vector_queries = [vector_query],
            select         = select,
            top            = 5
        )
        end = time.time()
        print("Azure Vector Search ended..")
        return results