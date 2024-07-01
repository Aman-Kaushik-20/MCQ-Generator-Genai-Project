import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv


#imporing necessary packages packages from langchain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key=os.getenv("OPENAI_API_KEY")


print(key)