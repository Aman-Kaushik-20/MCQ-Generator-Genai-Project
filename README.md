
# MCQs Generator Application with Langchain

This project is a Streamlit-based web application designed to generate and evaluate multiple-choice questions (MCQs) using Langchain. The application accepts PDF or text files and generates MCQs based on the input content.



![image](https://github.com/Aman-Kaushik-20/MCQ-Generator-Genai-Project/assets/143441723/533bf58d-ed87-440b-bc65-417afe53845f)

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [License](#license)

## Features

- **Streamlit Web Interface**: For uploading files and generating MCQs.
- **PDF and Text File Support**: Allows users to upload PDF or text files for MCQ generation.
- **Langchain Integration**: For handling language model prompts and responses.
- **Token and Cost Tracking**: Tracks the tokens used and the cost of API calls.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/mcq-generator-langchain.git
   cd mcq-generator-langchain
   ```

2. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add the required environment variables (see below).

## Environment Variables

Create a `.env` file in the root directory and add the following variables:

```
# Example
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. **Run the Streamlit application**:
   ```sh
   streamlit run app.py
   ```

2. **Access the application**:
   - Open your browser and go to `http://localhost:8501`.

## File Structure

```
mcq-generator-langchain/
│
├── src/
│   └── mcqgenerator/
│       ├── utils.py             # Utility functions for file reading and table data extraction
│       ├── mcqgenerator.py      # Function to generate and evaluate MCQs
│       └── logger.py            # Logger setup
│
├── .env                         # Environment variables file
├── app.py                       # Main application file
├── Response.json                # JSON file with predefined responses
├── requirements.txt             # List of Python packages required
└── README.md                    # This README file
```

## Dependencies

- **Streamlit**: Web framework for creating interactive web applications.
- **Pandas**: Data manipulation and analysis.
- **Langchain**: For handling language model prompts and responses.
- **dotenv**: For loading environment variables.
- **json**: For handling JSON data.
- **traceback**: For error handling and debugging.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Detailed Code Explanation

### Importing Required Libraries

```python
import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
```

### Loading Predefined Responses

```python
with open(r"Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)
```

### Streamlit Application

```python
st.title("MCQs Generator Application With Langchain (For Code Jr. - By Aman Kaushik)")

with st.form("User Input"):
    uploaded_file = st.file_uploader("Upload PDF or Text File :")
    mcq_count = st.number_input("No. of MCQs :", min_value=3, max_value=20)
    tone = st.text_input("Complexity Level Of Questions :", max_chars=20, placeholder="Simple")
    subject = st.text_input("Insert Subject :", max_chars=20)
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "RESPONSE_JSON": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("ERROR in the table data")
                    else:
                        st.write(response)
```

This README file includes all the necessary details to understand, install, and run the project effectively.
