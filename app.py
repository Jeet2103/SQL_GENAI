import streamlit as st
import os
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import openai
openai.api_key= os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Langchain : Chat with SQL DB",page_icon="🦜")
st.title("🦜 Langchain : Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_option  = ["Use SQLLite 3 Database - Student.db","Connect to you MySQL Database"]
selected_option = st.sidebar.radio(label = "Choose the DB which you want to chat ",options= radio_option)

if radio_option.index(selected_option) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_username = st.sidebar.text_input("MySQL Username")
    mysql_password = st.sidebar.text_input("MySQL Password",type="password")
    mysql_database = st.sidebar.text_input("MySQL Database")
else :
    db_uri = LOCALDB

if not db_uri:
    st.info("Please enter the Database information and URI")

llm = ChatOpenAI(model="gpt-4o-mini", streaming= True)


@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")) 

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_username,mysql_password,mysql_database)
else:
    db=configure_db(db_uri)


## toolkit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)