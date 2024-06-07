import requests
import os
import openai
import re
import json
from openai import OpenAI
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from document_generator import WordDocumentGenerator




class MainframeAnalyzer:
    def __init__(self, api_key: str, prompt: str, service: str = 'openai', endpoint: str = None, organization: str = None):
        self.service = service.lower()
        self.prompt = prompt
        self.api_key = api_key
        self.endpoint = endpoint
        if self.service == 'openai':
            self.client = OpenAI(api_key=api_key,organization=organization)
        elif self.service == 'azure' and not endpoint:
            raise ValueError("Azure endpoint must be provided for Azure OpenAI service")

    def _create_chat_messages(self, mainframe_code: str) -> list:
        return [
            {"role": "system", "content": "You are an IBM Mainframe code expert"},
            {"role": "user", "content": self.prompt + mainframe_code}
        ]

    def extract_business_rules(self, mainframe_code: str) -> str:
        messages = self._create_chat_messages(mainframe_code)
        response = None

        if self.service == 'azure':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            data = {
                "model": "gpt-4-omni",
                "messages": messages,
                "temperature": 0.5,
                "max_tokens": 4000,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            response = requests.post(f"{self.endpoint}/openai/deployments/gpt-4-omni/completions", headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad status codes
            result = response.json()
            return result['choices'][0]['message']['content']

        elif self.service == 'openai':
            response = self.client.chat.completions.create(model="gpt-4o",
            messages=messages,
            temperature=0.5,
            max_tokens=4000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0)
            return response.choices[0].message.content


    @staticmethod
    def extract_code(input_folder: str) -> str:
        print(f"Reading the code from the input folder location ...[{input_folder}]")
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path) and file_path.endswith(".txt"):
                with open(file_path, 'r') as file:
                    return file.read()
        raise FileNotFoundError(f"No .txt files found in the provided directory: {input_folder}")


    
    
    def save_to_docx(self, response: str, target_file_name: str):
        print(f"Writing the extracted business rules to file - [{target_file_name}]")
      
        # Print raw response for debugging (optional)
        print("Raw response:\n", response)

        # Use a regular expression to find the JSON part
        json_pattern = re.compile(r"\{.*\}", re.DOTALL)
        match = json_pattern.search(response)

        if match:
            json_string = match.group(0)
            # Convert the JSON string to a Python dictionary
            try:
                data = json.loads(json_string)

            except json.JSONDecodeError as e:
                print("Failed to decode JSON:", e)
        else:
            print("No JSON found in the response.")
        
       
        doc_generator = WordDocumentGenerator(data,file_name=target_file_name)
        doc_generator.generate_document()
        
        
    