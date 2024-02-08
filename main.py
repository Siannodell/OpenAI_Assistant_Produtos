import streamlit as st
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType


def main():


    load_dotenv()

    st.set_page_config(page_title="Faça uma pergunta ")
    st.header("Faça uma pergunta")

    user_csv = st.file_uploader("subir arquivo csv", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Pergunte algo sobre seu arquivo: ")

        ##llm = OpenAI(temperature=0)
        ##agent = create_csv_agent(llm, user_csv, verbose=True)
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106"),
                user_csv,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
            )

        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            st.write(response)



if __name__ == "__main__":
    main()
