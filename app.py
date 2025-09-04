import streamlit as st
import pandas as pd
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
# api_key = os.getenv("AZURE_OPENAI_API_KEYAZURE_OPENAI_ENDPOINT")
# openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  
# openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # e.g., 2023-07-01-preview
# openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")


# Initialize OpenAI client
# client = OpenAI(api_key=api_key)

endpoint = os.getenv("endpoint")
model_name = os.getenv("model_name")
deployment = os.getenv("deployment")

subscription_key =os.getenv("subscription_key")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Title of the app
st.title("Data Exploration and Insights Agent")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Load data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file, engine='openpyxl')

# Dataset summary
def summarize_dataset(df):
    st.subheader("Dataset Summary")
    st.write("**Shape:**", df.shape)
    st.write("**Columns and Data Types:**")
    st.write(df.dtypes)
    st.write("**Missing Values:**")
    st.write(df.isnull().sum())

# Descriptive statistics
def show_statistics(df):
    st.subheader("Descriptive Statistics")
    st.write(df.describe(include='all'))

# GPT-4 insights
# client = OpenAI(api_key = api_key)
def generate_insights(df, question):
    prompt = f"""
     You are a data analyst. Based on the following dataset summary and statistics, answer the question below:\n\n
    Dataset Columns: {df.columns.tolist()}\n
    Full dataset:\n{df.to_string(index=False)}\n\n
    Question: {question}\n
    Analyze the entire data, share the observations in a concise and insightful manner. If needed, create required charts."""
    
    response = client.chat.completions.create(
        # engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # your deployment name
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000
    )
    return response.choices[0].message.content
# def generate_insights(df, question):
#     prompt = f"""
#     You are a data analyst. Based on the following dataset summary and statistics, answer the question below:

#     Dataset Columns: {df.columns.tolist()}
#     First few rows:
#     {df.head().to_string()}

#     Question: {question}
#     Provide a concise and insightful answer.
#     """
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a helpful data analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=300
#     )
#     return response.choices[0].message.content

# Main logic
if uploaded_file:
    df = load_data(uploaded_file)
    summarize_dataset(df)
    show_statistics(df)

    st.subheader("Ask a Question About the Data")
    user_question = st.text_input("Enter your question (e.g., What are the top 5 products by sales?)")

    if user_question:
        with st.spinner("Generating insight..."):
            insight = generate_insights(df, user_question)
            st.markdown("### Insight")
            st.write(insight)
else:
    st.info("Please upload a CSV or Excel file to begin.")







