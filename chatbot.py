import os
import streamlit as st
# from langchain import OpenAI
# from langchain.llms import OpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
# from langchain.llms.openai import OpenAIChat
# from langchain_community.llms import OpenAIChat
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

st.title("Partners Portal Assistant")

db = SQLDatabase.from_uri("sqlite:///data.db")
llm = ChatOpenAI(temperature=0,
                 openai_api_key=os.environ["OPENAI_API_KEY"],
                 model_name='gpt-3.5-turbo-0125')

agent_executor = create_sql_agent(llm,
                                  db=db,
                                  agent_type="openai-tools",
                                  verbose=True)

# If the result is a list, remove all the brackets and quotation marks.
# If there are multiple records in the result, separate each record in its own line.

# TODO: Figure out line breaks
PROMPT = """Given an input question, first create a SQLite query and execute it to find the answer,
If the result is a list with a single element,
return the first element of that element.
Print each record, line by line.
If the type_of_organization is 0, return "unknown type";
if the type_of_organization is 1, return "governmental organization";
if the type_of_organization is 2, return "non-governmental organization";
if the type_of_organization is 3, return "educational/research institution";
if the type_of_organization is 4, return "healthcare organization";
if the type_of_organization is 5, return "community center/library";
if the type_of_organization is 6, return "for-profit business";
if the type_of_organization is 7, return "arts/cultural organization";
if the type_of_organization is 8, return "sports/recreational organization";
if the type_of_organization is 9, return "other".
When listing the partners, list the name, email, organization, and type_of_organization,
and do not return the listing number in front of each contact name.
The question: {question}."""

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=100)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter a query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        ans = db_chain.run(
            PROMPT.format(question=prompt))  # return GPT response

        response = st.write(ans)  # writes the response to the streamlit app

    st.session_state.messages.append({"role": "assistant", "content": ans})
