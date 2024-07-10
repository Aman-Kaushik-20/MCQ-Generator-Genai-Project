# MCQ Generator Application With Langchain

This project is a Streamlit-based web application designed to generate multiple choice questions (MCQs) using Langchain and OpenAI's GPT-3.5-turbo model. The application reads text from uploaded files, generates MCQs based on the text, and evaluates the complexity of the generated questions.


![image](https://github.com/Aman-Kaushik-20/MCQ-Generator-Genai-Project/assets/143441723/533bf58d-ed87-440b-bc65-417afe53845f)

# Running Tutorial -
link - https://drive.google.com/file/d/1k9SCSg5TjSpFNWf6a127sC7CIQO2MlJY/view?usp=sharing


## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [License](#license)

## Features

- **Streamlit Web Framework**: For creating the web interface.
- **Langchain Integration**: For handling prompt templates and language model interactions.
- **OpenAI GPT-3.5-turbo**: For generating and evaluating MCQs.
- **Pandas**: For displaying the generated MCQs in a tabular format.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/mcq-generator.git
   cd mcq-generator
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
OPENAI_KEY=your_openai_api_key
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
mcq-generator/
│
├── src/
│   ├── mcqgenerator/
│   │   ├── __init__.py
│   │   ├── utils.py          # Contains helper functions
│   │   ├── mcqgenerator.py   # Contains the SequentialChain setup
│   │   ├── logger.py         # Contains logging setup
│
├── Response.json             # JSON file with response format
├── .env                      # Environment variables file
├── app.py                    # Main application file
├── requirements.txt          # List of Python packages required
└── README.md                 # This README file
```

## Dependencies

- **Streamlit**: Web framework for interactive applications.
- **Langchain**: For handling prompt templates and chains.
- **OpenAI**: For GPT-3.5-turbo model access.
- **Pandas**: For data manipulation and display.
- **dotenv**: For loading environment variables.

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

### Loading JSON Response Template

```python
with open(r"Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)
```

### Streamlit UI Setup

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

### Environment Variable Loading

```python
load_dotenv()
key = os.getenv("OPENAI_KEY")
print("Key of OpenAI API is: ")
print(key)
```

### Language Model Setup

```python
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.7)

with open(r"Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)
```

### Prompt Template for Quiz Generation

```python
TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON format is given below--
{RESPONSE_JSON}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key='quiz', verbose=True)
```

### Prompt Template for Quiz Evaluation

```python
TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students,\
you need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
If the quiz is not at par with the cognitive and analytical abilities of the students,\
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student's abilities.
Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key='review', verbose=True)
```

### Sequential Chain Setup

```python
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    output_variables=["quiz", "review"],
    verbose=True,
)
```

This README file includes all the necessary details to understand, install, and run the project effectively.
