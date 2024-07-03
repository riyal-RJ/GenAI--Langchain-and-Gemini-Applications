import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()


# to comfigure the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#function to get the text from each page of a pdf
def get_pdf_text(pdfs):
    text=""
    for pdf in pdfs: # Accessing each pdf 
        pdf_reader=PdfReader(pdf) # Reading each pdf
        for page in pdf_reader.pages: #Reading each page of the pdf
            text+=page.extract_text()# Extract the text from that page
    return text


#function returning the chunks of pdf 
def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000) # Splitting the text into to chunks of size 10000 and two chunks can have common 1000 words
    chunks=text_splitter.split_text(text)
    return chunks

def get_vector_stores(text_chunks):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store=FAISS.from_texts(text_chunks,embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conv_chain():
    prompt_template="""
        Answer the question as detailed as possible from the context, make sure to provide all the details, if the answer is not present in the provide context then say 
        just "Answer not present!", don't provide wrong answer\n\n
        Context:\n {context}?\n
        Question:\n {question}\n


        Answer:
    """
    model=ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.25)

    prompt=PromptTemplate(template=prompt_template,input_variables=["context","question"])
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)

    return chain

def user_input(user_question):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db=FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
    docs=new_db.similarity_search(user_question)
    chain=get_conv_chain()


    response=chain(
        
           { "input_documents":docs,
            "question":user_question},
            return_only_outputs=True
        
    )
    print(response)
    st.write("Reply: ",response["output_text"])




def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF📃 using Gemini 🤖")
    st.image('img.jpg')  # Adjust width as needed



    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_stores(text_chunks)
                st.success("Done")


if __name__=="__main__":
    main()

