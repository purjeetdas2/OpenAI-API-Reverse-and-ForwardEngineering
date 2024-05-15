# OpenAI-API-Reverse-and-ForwardEngineering

This is **Mainframe Code Reverse and Forward Engineering** project! This repository contains tools and scripts for performing reverse and forward engineering on mainframe code utilizing Python and the OpenAI API. Goal is to facilitate the understanding, analysis, and transformation of legacy mainframe code into modern architectures.

## Contents
- [Overview](#overview)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project leverages Python and the OpenAI API to:
- Conduct reverse engineering of mainframe code (e.g., JCL, COBOL)
- Translate and transform legacy code into modern frameworks
- Allow business rule extraction and code analysis for modern application development

## Features

- **Reverse Engineering**: Analyze and revert compiled mainframe code into a human-readable format.
- **Forward Engineering**: Translate legacy code into modern programming languages and frameworks.
- **API Integration**: Utilize the OpenAI API for natural language processing to assist in code understanding and transformation.

## Setup and Installation

### Prerequisites

Make sure you have the following prerequisites installed:

- Python 3.7 or higher
- `pip` package installer

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

    > **Note**: Make sure your `requirements.txt` includes:
    > ```
    > openai
    > python-docx
    > ```

4. **Set up your OpenAI API key and organization ID**:

    Create an `.env` file in the root directory of your project and add your OpenAI API key and organization ID:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_ORG_ID=your_openai_org_id
    ```

    Alternatively, you can directly add these in the script where the API client is initialized:

    ```python
    client = OpenAI(api_key='your_openai_api_key', organization='your_openai_org_id')
    ```

5. **Prepare your folder structure**:

    Make sure the following directories exist:

    ```plaintext
    your-repo-name/
    ├── code/       # Directory to place your .txt files with the mainframe code
    ├── docs/       # Directory where the generated DOCX files will be saved
    ├── your_script.py    # Your main script file
    ├── requirements.txt
    └── README.md
    ```

6. **Run the script**:

    Execute the main script to process the files in the `code/` directory and save the generated DOCX in the `docs/` directory:

    ```bash
    python your_script.py
    ```

    > **Note**: Replace `your_script.py` with the actual name of your script.

### Example Usage

1. Place your mainframe code files with a `.txt` extension into the `code/` directory.
2. Run the script:

    ```bash
    python your_script.py
    ```

3. The output DOCX file will be saved in the `docs/` directory.

### Troubleshooting

If you encounter any issues, ensure that:

- Your Python version is 3.7 or higher.
- You have correctly installed all required packages.
- Your OpenAI API key and organization ID are correctly set.

