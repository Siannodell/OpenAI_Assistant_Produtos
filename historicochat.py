import streamlit as st
from pathlib import Path
from streamlit_chat import message
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

st.title('Faça perguntas sobre seu arquivo!')
OPENAI_API_KEY = st.text_input('Insira sua chave da OPEN AI', '')
DESTINATION_DIR= st.text_input('Selecione uma pasta para salvar o arquivo', '')
if st.button("Gravar chave"): 
    st.write("Salvo! Sua chave é" , OPENAI_API_KEY)
    os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY




csv_file_uploaded = st.file_uploader(label="Insira um arquivo aqui")


if csv_file_uploaded is not None:
    def save_file_to_folder(uploadedFile):
        # Save uploaded file to 'content' folder.
        save_folder = DESTINATION_DIR
        save_path = Path(save_folder, uploadedFile.name)
        with open(save_path, mode='wb') as w:
            w.write(uploadedFile.getvalue())

        if save_path.exists():
            st.success(f'Arquivo {uploadedFile.name} salvo!')
            
    save_file_to_folder(csv_file_uploaded)
    loader = CSVLoader(file_path=os.path.join(DESTINATION_DIR, csv_file_uploaded.name))

    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    # Create a question-answering chain using the index
    chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")





    #Creating the chatbot interface
    st.title("Pergunte algo sobre seu arquivo")

        # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []


    def generate_response(user_query):
        response = chain({"question": user_query})
        return response['result']
    
    
    # We will get the user's input by calling the get_text function
    def get_text():
        input_text = st.text_input("Você: ","Olá! pode me responder perguntas sobre meu arquivo?", key="input")
        return input_text
    user_input = get_text()

    if user_input:
        output = generate_response(user_input)
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')