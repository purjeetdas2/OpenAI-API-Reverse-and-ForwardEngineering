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
    current_working_directory = os.getcwd()
    program_folders_available = os.listdir(os.path.join(current_working_directory, 'code'))
    print(f"Programs available in the inout folder{program_folders_available}")
    folder = input("Enter Program folder:")
 
    try:
        # Extract the specific prompt you want to use
        # Load the prompts from the external file
        prompts = load_prompts(file_path=os.path.join(current_working_directory, 'prompt-templates','SUMMARIZE_JCL_COBOL.json'))
        prompt = prompts.get('prompt', 'Default prompt in case key is not found')
        #print(prompt)

        prompt = """
        Explain the below JCL , JCL Param , Copy Book , Cobol Code and provide below details
             1. Summarize the program flow
             2. List of the validation rules implemented.
        Display the response in below sections and should adhere to Word document standards and stick to the naming conventions while including the following sections:
        1. Input
        2. High level Code Flow. Mention all the steps along with their input and output parameters if applicable. Provide a flow diagram at the end of this section.
        3. Business validation rules list.
        4. Sql Queries. Ensure for each validation rule include all SQL's used include query condition and subprogram names referenced.
        5. Tables Referenced. Ensure to list all tables referenced based table schems categorize into different business domain
        6. Business Rules/Logic Extraction - Extract all the rules from the cobol program.
        6. Data Structures. Ensure to extract all the data structures used and include it in the output (Field Name, Data Type, Size)

        Create separate sections Cobol Extracted code and JCL extracted.Make sure to use the best practices in Word document formatting.

        Sample structure of the required outcome - start
        
        1. Input
            The Job is designed to [ what does the JCL , PROC , Cobol main program do at high level ] 
        2. High-Level Code Flow 
           1 Initalization of Job (name of the JCL): [ Explin the job parameteres. Highlight the libraries too.]
           2 [List all the steps in the proc including the input passed to each of the steps and the output. ]
           3 Execution of the COBOL Programs (name of the cobol program) :[summarize the logic in the COBOL program ]
              Code Flow Diagram
              [Provide the code flow diagram below]
        3. Business Validation Rules:
            [ Provide the numbered list of what is the COBOL program perfoms based on the code snippets]
        4. SQL's Used
             [The provide may be interacting with DB2 tables. Provide all of that.]
        5. Subprograms References
            [List all the subroutines along with the logc performed with those provided code snippets]
        6. List of Tables Referenced
            [Provide all the explicit references to the tables]
        7. Data Structures in Copybooks
             [Provide a number list and provide an explanation of each one of those. Also provide field Name Datatype and Size]
        8. Business Rules/Logic Extraction - Cobol (Cobol Program name)
            High Level Code Flow 
               1 Initalization of Porgram (name of the JCL): [ Explin the program parameteres. Highlight the libraries too.]
               2 Provide the logic in layman language.
               3 Provide the details of the end of the program.Does it provide any output
               Code Flow Diagram.
               [Provide the code flow diagram below]
        [Repeat it for all the main subprograms as well.]


        Summary:
            Provide a concise summary.Also categorize the complexity level of the job flow

        Provide the response in JSON format
        ---- Example End -----


        """
        
        analyzer = MainframeAnalyzer(api_key=None, organization=None, prompt=prompt)
        code = analyzer.extract_code(input_folder=os.path.join(current_working_directory, 'code', folder))
        extracted_content = analyzer.extract_business_rules(mainframe_code=code)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{folder}_{timestamp}.docx"
        analyzer.save_to_docx(response=extracted_content, target_file_name=os.path.join(current_working_directory, 'docs', filename))
        print(f"BRE document generated - [{filename}]")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()