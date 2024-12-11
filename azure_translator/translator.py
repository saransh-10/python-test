import requests, uuid, json

class AzureTranslator:

    def __init__(self):
        """
        Initializes an instance of the Translator class.
        """
        #https://trsl-hayya-dev-we-001.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3
 
        self.subscription_key = "1b310f3994264332a346697967a3e391"
        self.endpoint = "https://trsl-hayya-dev-we-001.cognitiveservices.azure.com/translator/text/v3.0/" 
        self.location = "westeurope"
        
    
    def check(self, text):
        subscription_key = self.subscription_key
        endpoint =self.endpoint
        region = "westeurope"  # Example: "westus2"

        # Define the API path and parameters
        path = '/translate'
        constructed_url = f"{endpoint}{path}"
        params = {
            'api-version': '3.0',
            'from': 'en',         # Language of the input text (optional)
            'to': ['fr', 'es']    # List of target languages (e.g., French, Spanish)
        }

        # Create the request headers
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())  # Unique ID for tracking
        }

        # Define the text to translate
        body = [{
            'text': text
        }]

        # Make the API request
        response = requests.post(constructed_url, params=params, headers=headers, json=body)

        # Parse and display the response
        if response.status_code == 200:
            translations = response.json()
            for item in translations:
                print(f"Original: {item['text']}")
                for translation in item['translations']:
                    print(f"Translated to {translation['to']}: {translation['text']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

        
    def detect_language(self, text):
        """
        Detect the language of the input text.
        :param text: Text to detect the language for
        :return: Detected language
        """
        try:
            path = '/detect'
            constructed_url = self.endpoint + path

            params = {
                'api-version': '3.0'
            }

            headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Ocp-Apim-Subscription-Region": self.location,
            "Content-Type": "application/json",
            'X-ClientTraceId': str(uuid.uuid4())
            }

            body = [{
                'text': text
            }]

            request = requests.post(constructed_url, params=params, headers=headers, json=body)
            response = request.json()  
                      
            # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
            return response[0]['language']
        except Exception as e:
            print(str(e))
            return ''

    def query_translate(self, text, source_language='ar', target_language='en'):
        """
        Translates the given text from the source language to the target language using the Azure Translator service.

        Args:
            text (str): The text to be translated.
            source_language (str): The source language (default is 'ar' for Arabic).
            target_language (str): The target language (default is 'en' for English).

        Returns:
            str: The translated text or an empty string in case of an error.
        """
        try:
            path = '/translate'
            constructed_url = self.endpoint + path

            params = {
                'api-version': '3.0',
                'from': source_language,
                'to': target_language
            }

            headers = {
                'Ocp-Apim-Subscription-Key': self.subscription_key,
                'Ocp-Apim-Subscription-Region': self.location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }

            body = [{
                'text': text
            }]

            request = requests.post(
                constructed_url, params=params, headers=headers, json=body)
            response = request.json()
            return response[0]['translations'][0]['text']
        except Exception as e:
            return ''
        
    
    def final_gpt_ans(self, text, source_language='en', target_language='ar'):
        """
        Translates the given text from the source language to the target language using the Azure Translator service.

        Args:
            text (str): The text to be translated.
            source_language (str): The source language (default is 'ar' for Arabic).
            target_language (str): The target language (default is 'en' for English).

        Returns:
            str: The translated text or an empty string in case of an error.
        """
        try:
            path = '/translate'
            constructed_url = self.endpoint + path

            params = {
                'api-version': '3.0',
                'from': source_language,
                'to': target_language
            }

            headers = {
                'Ocp-Apim-Subscription-Key': self.subscription_key,
                'Ocp-Apim-Subscription-Region': self.location,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }

            body = [{
                'text': text
            }]

            request = requests.post(
                constructed_url, params=params, headers=headers, json=body)
            response = request.json()
            return response[0]['translations'][0]['text']
        except Exception as e:
            return ''

    def process_text(self, text):
        """
        Process the text by checking its language and translating if necessary.
        :param text: Input text
        :return: Processed text in English
        """
        try:
            detected_language = self.detect_language(text)
            if detected_language == "ar":  # Arabic language code
                translated_text = self.translate(text, "en")  # Translate to English
                return translated_text
            elif detected_language == "en":  # English language code
                return text  # No translation needed
            else:
                return f"Unsupported language: {detected_language}"
        except Exception as e:
            return f"Error processing text: {e}"

