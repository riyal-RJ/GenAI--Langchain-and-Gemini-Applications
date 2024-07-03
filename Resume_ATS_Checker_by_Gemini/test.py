import streamlit as st

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
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the given job description. Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
"""

# Button actions
if submit1:
    if uploaded_file is not None:
        # Perform some action when submit1 button is clicked
        pass
    else:
        st.error("Please upload the resume before proceeding.")

elif submit2:
    # Perform some action when submit2 button is clicked
    pass

elif submit3:
    if uploaded_file is not None:
        # Perform some action when submit3 button is clicked
        pass
    else:
        st.error("Please upload the resume before proceeding.")
