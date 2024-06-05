import requests
import openai
import os
import docx
from openai import OpenAI

class CodeGenerator:
    def __init__(self, api_key: str, prompt: str, service: str = 'openai', endpoint: str = None, organization: str = None):
        self.service = service.lower()
        self.prompt = prompt
        self.api_key = api_key
        self.endpoint = endpoint

        if self.service == 'openai':
            self.client = OpenAI(api_key=api_key,organization=organization)
        elif self.service == 'azure' and not endpoint:
            raise ValueError("Azure endpoint must be provided for Azure OpenAI service")

    def _create_chat_messages(self, bre: str) -> list:
        return [
            {
                "role": "system",
                "content": "You are an expert software developer proficient in both mainframe technologies and modern Java-based frameworks, particularly Spring Batch. Your task is to convert given business rules and logic from mainframe systems into a Spring Batch application."
            },
            {
                "role": "user",
                "content": self.prompt + bre
            },
            {
                "role": "assistant",
                "content": "Please provide: \n1. Translation of JCL Job functionalities to Spring Batch configurations. \n2. Java equivalents of COBOL program, Subroutine logic using Spring Batch framework. \n3. Mapping of Subroutine workflows to Spring Batch components. \n4. Conversion of Copybooks content and structure to equivalent Java classes or data structures used in Spring Batch. Follow the best practices and naming conventions in Spring batch. Generate unit test classes required to test the spring batch."
            }
        ]

    def extract_code(self, bre: str) -> str:
        messages = self._create_chat_messages(bre)
        response = None

        if self.service == 'azure':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            data = {
                "model": "gpt-4-omni",
                "messages": messages,
                "temperature": 0.7,
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
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=4000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content

    @staticmethod
    def extract_bre(input_folder: str) -> str:
        print(f"Read the bre from the input folder location ...[{input_folder}]")
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path) and file_path.endswith(".docx"):
                print(file_path)
                doc = docx.Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                return '\n'.join(full_text)
        raise FileNotFoundError(f"No .docx files found in the provided directory: {input_folder}")

    def save_to_code_location(self, content: str, target_file_name: str):
        print(f"Writing the extracted code to file - [{target_file_name}]")
        doc = docx.Document()
        doc.add_heading('Response:', level=1)

        paragraphs = content.split('\n')
        for paragraph in paragraphs:
            clean_paragraph = paragraph.strip()
            if clean_paragraph.startswith('###'):
                doc.add_heading(clean_paragraph.strip('# ').title(), level=2)
            elif clean_paragraph.startswith('####'):
                doc.add_heading(clean_paragraph.strip('# ').title(), level=3)
            elif clean_paragraph.startswith('-'):
                p = doc.add_paragraph(clean_paragraph.lstrip('- '))
                p.style = 'List Bullet'
            elif clean_paragraph:
                self._add_paragraph_with_formatting(doc, clean_paragraph)

        doc.save(target_file_name)

    @staticmethod
    def _add_paragraph_with_formatting(doc: docx.Document, text: str):
        paragraph = doc.add_paragraph()
        parts = text.split('**')
        bold = False
        for part in parts:
            run = paragraph.add_run(part)
            if bold:
                run.bold = True
            bold = not bold
