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

with open(r"Response.json", "r") as f:
    RESPONSE_JSON=json.load(f)


st.title(" MCQs Generator Application With Langchain ")

with st.form("User Input"):
    uploaded_file=st.file_uploader("Upload PDF or Text File :")

    mcq_count=st.number_input("No. of MCQs :", min_value=3, max_value=20)

    tone = st.text_input("Complexity Level Of Questions :", max_chars=20, placeholder="Simple")

    subject = st.text_input("Insert Subject :", max_chars = 20)

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                #count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "RESPONSE_JSON":json.dumps(RESPONSE_JSON)
                        }
                    )
                #st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Totel Tokens :{cb.total_tokens}")
                print(f"Prompt Tokens :{cb.prompt_tokens}")
                print(f"Completion Tokens :{cb.completion_tokens}")
                print(f"Totel Cost :{cb.total_cost}")
                if isinstance(response, dict):
                    #extract The Quiz data from the response
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(json.dumps(quiz))
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display The review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("ERROR in the table data")
                    else:
                        st.write(response)







