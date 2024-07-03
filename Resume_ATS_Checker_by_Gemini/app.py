from dotenv import load_dotenv

load_dotenv()# load the environment variables from .env file

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError,PDFPageCountError,PDFSyntaxError

#configure te api key so that we can interact gemini pro model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')#using vision model since we will convert the pdf to image
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to list of images. each page is converted into separate image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]#get the first page of the pdf

        # Convert to bytes
        img_byte_arr = io.BytesIO() #creates BytesIO object
        first_page.save(img_byte_arr, format='JPEG')#saves the first page of the pdf as jpeg image into image_byte_arr variable
        img_byte_arr = img_byte_arr.getvalue()#retrieves the bytes from the BytesIO object

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#streamlit UI
# Set page title and header
st.set_page_config(page_title="ATS Resume Expert", page_icon=":clipboard:", layout="wide")
st.title("Welcome to ATS Resume Expert")

# Job Description input
input_text = st.text_area("Job Description:", height=150, key="input")

# Resume upload
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")

# Layout for buttons
col1, col2, col3 = st.columns(3)

# Buttons
submit1 = col1.button("Tell Me About the Resume")
submit2 = col2.button("How Can I Improve My Skills")
submit3 = col3.button("Percentage Match")

# Input prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against
 the given job description. Please share your professional evaluation on whether the candidate's profile aligns
 with the role. Highlight the strengths and weaknesses of the applicant in relation to specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science
and ATS functionality. Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. First, the output should
 come as a percentage, then keywords missing, and lastly, final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        responses=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is : ")
        st.write(responses)
    else:
        st.write("Re-upload the Resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")




