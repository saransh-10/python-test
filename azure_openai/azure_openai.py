import json
from openai import AzureOpenAI
from azure_openai.prompts import *

class OpenAIHandler:
    def __init__(self):
        self.api_key = "f840f3cfc8fa4c9fa85c8c5d55971354"
        self.api_version = "2024-10-21"
        self.api_endpoint = "https://oai-hayya-dev-sc-001.openai.azure.com/"
        self.deployment_name = "gpt-4o"


        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            base_url=f"{self.api_endpoint}/openai/deployments/{self.deployment_name}"
        )

    def _openai_chat_completion(self, messages):
        deployment_name = "gpt-4o"
        client = AzureOpenAI(
            api_key        = self.api_key, 
            api_version    = self.api_version,
            azure_endpoint = self.api_endpoint,
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=0.2,
            top_p=0.8,
            stop=None
        )
        return response

    def sql_openai(self, query):
        messages = [
            {'role': 'system', 'content': prompt_sql},
            {'role': 'user', 'content': query}
        ]
        response = self._openai_chat_completion(messages)
        json_obj = json.loads(response.model_dump_json(indent=2))
        content = json_obj["choices"][0]["message"]["content"]
        print("Successfully fetched SQL answers.")
        return content

    def openai_embeddings(self, query: str):
        print("Creating OpenAI embeddings...")
        client = AzureOpenAI(
        api_key        = self.api_key, 
        api_version    = self.api_version,
        azure_endpoint = self.api_endpoint,
    )
        embed_model_name="text-embedding-ada-002"
        embedding = client.embeddings.create(
            input=[query],
            model=embed_model_name
        ).data[0].embedding
        print("Successfully created OpenAI embeddings.")
        return embedding


    def generate_response(self, sql_results):
        userRole="You are response to generate a natural language response."
        assistantRole = f"""
        You are a helpful assistant. Combine the SQL results and indexer data to create a human-readable response.

        
        ### SQL Results:
        {sql_results}
    
    
        ### Instructions:
        1. Summarize the data concisely.
        2. Highlight key insights like product details and relevance.
        3. Write in natural language.
        4. Don't start with According to data, As per data, The data indicates that the age bucket for the queried group is categorized as \"Young Adult.\" Don't start with According to data, As per data, The data indicates that the age bucket for the queried group is categorized as \"Young Adult.\".
        5. Don't show data like \"Young Adult.\". 
        Response:
        """
        completion =  self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {'role': 'system', 'content': assistantRole},
                    {'role': 'user', 'content': userRole}
                    ],
            temperature=0,
            max_tokens=1000,
            top_p=0.5
            )
        return completion.choices[0].message.content
