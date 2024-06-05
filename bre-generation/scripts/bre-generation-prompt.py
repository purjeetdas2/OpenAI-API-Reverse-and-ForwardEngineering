from datetime import datetime
import os
import json

from mainframe_analyzer import MainframeAnalyzer

def prompt_user():
    print("Select the type of mainframe program to reverse engineer:")
    print("1. All (include all components - JCLs, COBOL, PROC, etc.)")
    print("2. COBOL Main Program")
    print("3. COBOL Subroutine")
    choice = input("Enter your choice (1/2/3): ")
    return choice

def load_prompts(file_path):
    with open(file_path, 'r') as file:
        prompts = json.load(file)
    return prompts

def main():   

    choice = prompt_user()
    folder = input("Enter Program folder:")
    current_working_directory = os.getcwd()

 
 
    try:
        # Extract the specific prompt you want to use
        # Load the prompts from the external file
        prompts = load_prompts(file_path=os.path.join(current_working_directory, 'prompt-templates','SUMMARIZE_JCL_COBOL.json'))
        prompt = prompts.get('prompt', 'Default prompt in case key is not found')
        print(prompt)
        analyzer = MainframeAnalyzer(api_key=None, organization=None, prompt=prompt)
        code = analyzer.extract_code(input_folder=os.path.join(current_working_directory, 'code', folder))
        extracted_content = analyzer.extract_business_rules(mainframe_code=code)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{folder}_{timestamp}.docx"
        analyzer.save_to_docx(content=extracted_content, target_file_name=os.path.join(current_working_directory, 'docs', filename))
        print(f"BRE document generated - [{filename}]")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()