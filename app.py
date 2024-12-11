from flask import Flask, request, jsonify
from collections import OrderedDict
from openai import AzureOpenAI
import re
import json
from flask_cors import CORS
from datetime import datetime
from azure_translator import translator
from azure_cognitive_search import az_cognitive_search
from azure_blob import blob_storage
from azure_openai import azure_openai
from operations.greetings import is_greeting
from operations.databricks_query import execute_databricks_sql_query


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

translator = translator.AzureTranslator()
blob_storage = blob_storage.AzureBlobStorage()
az_cognitive_search = az_cognitive_search.AZCognitiveSearch()
azure_openai = azure_openai.OpenAIHandler()

api_key = "f840f3cfc8fa4c9fa85c8c5d55971354"
api_base = "https://oai-hayya-dev-sc-001.openai.azure.com/"  # Replace with your endpoint
api_type = "azure"
api_version = "2024-10-21"
deployment_name = "gpt-4o"

client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}"
)

@app.route('/', methods=['GET'])
def read_root():
    try:
        # Log a message indicating successful execution        
        return {"Application": "App is running"}
    except Exception as e:
        # Log any unexpected errors
        return {"message": str(e)}

@app.route('/api/messages', methods=['POST'])
def queryTranslator():
    """
    A POST API to check the language.
    """
    try:
        # Get JSON data from the request
        
        data = request.get_json()
        query = data.get('query')
        query_details = {"lang":"en", 
                        "en_query":query, 
                        "raw_response":"NaN", 
                        "en_response":"NaN",
                        "ar_query":"Nan",
                        "ar_response":"NaN", 
                        "sql_query":"NaN",
                        "sql_response" : "NaN", 
                        "similar_ques":[], 
                        "datetime":str(datetime.now()), 
                        "followup": "NaN", 
                        "rephrase_query":"NaN", 
                        "response_time":"NaN",
                        "cog_section":"NaN"
                        }
        
        print("USER QUERY: ",query)
        detected_language = translator.detect_language(query)
        
        if detected_language == "ar":
            lang_type = "ar"
            query_details["ar_query"] = query
            query_details["lang"] = "ar"
            query =translator.query_translate(query, lang_type)
            query_details['en_query'] = query
        # print(query_details['en_query'])

        elif detected_language == "en":
            lang_type = "en"

        if is_greeting(query):
            response = client.chat.completions.create(
                model=deployment_name,  
                messages=[
                    {"role": "system", "content": "I am HAYYA, a QnA Expert Bot.If you are being greeted then greet back, in a friendly manner with a arabic accent in English.\
                    /n If you are being appreciated by words like good, good job etc. , answer in a way such as 'thank you, how may I assist you further"},
                    { "role": "user", "content": query}
                ]
            )
            ans = response.choices[0].message.content
            query_details['en_response'] = ans
            final_response = ans
        else:
            user_question = data.get('query')
            select_cols = ["head_content", "schema_name", "table_name", "columns"]  
            tables = az_cognitive_search.azure_vector_search(final_query = user_question, select = select_cols)

            print("******************* TABLES ******************",type(tables))
            
            table_info = OrderedDict()
            for i in tables:
                # print("DONE 1",i)
                table_info[f"{i['table_name']}"] = {
                    "table_name": i["table_name"],
                    "schema_name": i["schema_name"],
                    "columns": i["columns"],
                    "head_content": i["head_content"]
                    
                }
            # print("TABLE INFORMATION: ",table_info)
            schema = ""
            for key in table_info.keys():
                table_name = table_info[key]["table_name"]
                schema_name = table_info[key]["schema_name"]
                schema += f"SCHEMA_NAME: {schema_name}\nTABLE_NAME: {table_name}\nSAMPLE_DATA: \n{table_info[key]['head_content']}\nCOLUMNS: {table_info[key]['columns']}\n"

            print("SCHEMA ",schema)
            
            rag_information = f"""
                    {schema}

                    QUESTION: {user_question}
                    """
            gpt_response = azure_openai.sql_openai(rag_information)
            print("GPT RESPONSE: ",gpt_response)
            gpt_response = json.loads(gpt_response)
            print(gpt_response)
            if gpt_response['sql_query'] == "NO SQL QUERY CAN BE GENERATED.":
                final_response = "Please ask question based on your data."
            else: 
                res=execute_databricks_sql_query(gpt_response['sql_query'])
                final_response = azure_openai.generate_response(res)

            if detected_language == "ar":
                final_response = translator.final_gpt_ans(final_response)

            return {"RESPONSE":final_response}

        return {"RESPONSE":final_response}
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
