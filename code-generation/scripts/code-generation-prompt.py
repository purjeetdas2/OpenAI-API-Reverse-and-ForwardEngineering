from openai import OpenAI
from datetime import datetime
import os
import json
from code_generator import CodeGenerator

def load_prompts(file_path):
    with open(file_path, 'r') as file:
        prompts = json.load(file)
    return prompts

def main():
    
 
    folder = input("Enter Program folder:")
    current_working_directory = os.getcwd()

    try:
        # Extract the specific prompt you want to use
        # Load the prompts from the external file
        #prompts = load_prompts(file_path=os.path.join(current_working_directory, 'prompt-templates','SUMMARIZE_JCL_COBOL.json'))
        #prompt = prompts.get('prompt', 'Default prompt in case key is not found')
        prompt = "Content of the document: \n- High-level summary of JCL Job functionalities \n- Details of COBOL program logic \n- Description of Subroutine workflows \n- Content and structure of Copybooks"
        #print(prompt)
        
        code_generator = CodeGenerator(api_key=None, organization=None, prompt=prompt)
        bre_doc = code_generator.extract_bre(input_folder=os.path.join(current_working_directory, 'docs', folder))
        extracted_code = code_generator.extract_code(bre=bre_doc)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{folder}_{timestamp}.docx"
        code_generator.save_to_code_location(content=extracted_code,target_file_name=os.path.join(current_working_directory, 'code', filename))
        print("...... Code Generated successfully ...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()