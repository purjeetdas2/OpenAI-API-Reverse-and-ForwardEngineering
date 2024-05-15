from openai import OpenAI
from docx import Document
import os

# Initialize the OpenAI client
client = OpenAI()

# Define the prompt to be sent to the OpenAI model
prompt = """

You need to explain the below JCL Job, JCL Parameters ,COBOL Code ,Subroutine, Copybook and provide the below details
1. Summarize the program flow
2. List of business validation rules implemented.

Display the response in below sections tailored for "Business Analysts" to fulfill business requirements.Do not use technical terms unless necessary.

1. High Level Code flow
2. Code Flow diagram
3. Summarize the JCL Job , COBOL Main Program , Subroutine in the below format.
-Consider the following points while generating "Summary of the JCL JOB":
1. Job Name and Description : Provide a clear and concise name and description.
2. Job Steps:
   List all the steps included in the JCL.
   Include the name of each step and its corresponding program or utility.
3. Step Parameters:
    Document the parameters specified for each step.
4. Data sets:
   Identify all the datasets referenced in the JCL.
5. Execution Control statements
   Note any execution control statements used in JCL such as condition nodes, restart parameters or scheduling directives.

-Consider the following points while generating "Summary of the COBOL program":
1. Program Name and Purpose : Provide a clear and concise name and description.
2. Program Structure:
   Outline structure of the program including divisions,sections and paragraphs.
   Describe the flow of control within the program.
3. Input and Output:
    Identify the input sources(eg. files,databases,user input) and describe their format.
    Describe the output destinations and formats(eg. files, reports,screens).
4. Logic and Processing:
   Document the main logic flow of the program.
   Describe the processing performed on input data to produce the desired output.
5. Data Description: 
    List and describe the data items used in the program..
6. Subroutine Calls:
    Identify any subroutine called by the main program..
7. Error Handling
   Document how the subroutine handles errors or exceptional conditions.

-Consider the following points while generating "Summary of the Subroutine":
1. Subroutine Name and Purpose : Provide a clear and concise name and description.
2. Input Parameters: 
    List and describe each input parameter accepted by the subroutine.
    Include data types, lengths and any restrictions.
3. Output Parameters:
    Enumerate the output parameters returned by the subroutine
    Specify the data types and expected values
4. Functionality Overview: 
    Outline the main tasks performed by the subroutine.
    Describe the logic flow it follows.
5. Subroutine Dependencies:
    Identify any external resources or modules the subroutine relies on.
    List any data files,databases for libraries accessed.
6. Error Handling
   Document how the subroutine handles errors or exceptional conditions.

 Follow the below numbers to identify the JCL Job , JCL Parameters , Subroutine , COBOL Program and Copybook in the provided code.
1. COBOL Program
2. Subroutine
3. Copybook
4. JCL Job
5. JCL Parameters
"""
def extract_business_rules(mainframe_code):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        {   
            "role": "system",
            "content": "You are an IBM Mainframe Natural code expert"
        },
        {   
            "role": "user",
            "content": prompt+mainframe_code
        }
        ],
        temperature=0.5,
        max_tokens=4000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content
def extract_code(input_folder):
    print(f"..... Reading the code from the input folder location ...[{input_folder}]")
    for filename in os.listdir(input_folder):
        file_path= os.path.join(input_folder,filename)
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            with open(file_path,'r') as file:
                file_content=file.read()
                return file_content
    raise FileNotFoundError(f"No .txt files found in the provided directory: {input_folder}")

def save_to_docx(content,target_file_name):
    print(f"..... Writing the extracted business rules to file - [{target_file_name}]")    
    doc = Document()
    doc.add_paragraph(content)
    doc.save(target_file_name)

def main():
    current_working_directory = os.getcwd()    
    try:
        code = extract_code(input_folder=os.path.join(current_working_directory, 'code'))
        extracted_content = extract_business_rules(mainframe_code=code)       
        print(extracted_content)        
        save_to_docx(content=extracted_content, target_file_name=os.path.join(current_working_directory, 'docs', 'samplebre.docx'))        
        print("...... BRE document saved successfully ...")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()