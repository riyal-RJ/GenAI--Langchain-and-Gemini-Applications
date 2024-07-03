from dotenv import load_dotenv
load_dotenv()# loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# to comfigure the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")

#function to load gemini-pro model
def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text


#initializing streamlit app

st.set_page_config(page_title="QnA Demo")

st.header("Gemini LLM Application")

input=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

#when submit is clicked

if submit:
    response=get_gemini_response(input)
    st.subheader("The response is: ")
    st.write(response)