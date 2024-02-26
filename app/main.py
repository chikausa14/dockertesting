from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
sect_chat_model = ChatOpenAI(tiktoken_model_name="ft:gpt-3.5-turbo-0613:personal::8uX3No6l")
field_chat_model = ChatOpenAI(tiktoken_model_name="ft:gpt-3.5-turbo-1106:personal::8u9SGpDi")

api_keys = [
    "my_api_key"
]

app = FastAPI()

api_key_header = APIKeyHeader(name="ES-API-KEY")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key"
    )

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/getsuggestionsectiontitle/")
def SectionResponse(user_input, api_key: str = Security(get_api_key)):
    template = "Generate a nested python dictionary with 8 entries based on the input given by the user. Each entry must contain another dictionary with the type key. The 'type' key can only be one of these types: text input, text area, auto increment, dropdown, date picker, time picker, datetime booking, table input, table select, file upload, image upload, signature, separator, radio button, checkbox, phone number, numbers, email, IC number, map, info, report list. Ensure you match the language of the input."
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template)
    ])

    messages = chat_prompt.format_messages(text=user_input)
    result = sect_chat_model.invoke(messages).content

    return result

@app.post("/getsuggestionexistingfields/")
def FieldResponse(user_input, api_key: str = Security(get_api_key)):
    template = "Generate the next 3 entries to the dictionary. The 'type' key can only be one of these types: text input, text area, auto increment, dropdown, date picker, time picker, datetime booking, table input, table select, file upload, image upload, signature, separator, radio button, checkbox, phone number, numbers, email, IC number, map, info, report list. Print only the code in a singular line."
    human_template="{text}"
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template)
    ])

    messages = chat_prompt.format_messages(text=user_input)
    result = field_chat_model.invoke(messages).content

    return result

#run using uvicorn main:app, and with --reload flag if want to develop