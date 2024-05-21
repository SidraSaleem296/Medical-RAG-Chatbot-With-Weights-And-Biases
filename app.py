import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import asyncio
import wandb

# Initialize Weights and Biases
wandb.init(project="medical-data-chatbot", name="chatbot-run")

# Loading the environment variables
load_dotenv()
os.getenv("GOOGLE_API_KEY")

# Function to extract text from PDF
def get_pdf_text(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

# Split text into manageable chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)

# Creating and saving the vector store
def create_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to load conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the following question based on the context provided:
    Question: {question}
    Context: {context}
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(llm=model, prompt=prompt)

# Asynchronous function to get answers
async def get_answer(question, context):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # Allow dangerous deserialization, assuming the source is trusted
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(context)
    
    chain = get_conversational_chain()
    # Pass the entire docs list as input_documents
    input_data = {"context": context, "question": question, "input_documents": docs}

    response = await chain.ainvoke(input_data)  # Using ainvoke method

    # Formatting the response
    formatted_response = format_response(response, context)
    return formatted_response

def format_response(response, context):
    # Assuming response['output_text'] contains the text we want to format
    output_text = response['output_text'] if 'output_text' in response else str(response)
    # Apply any additional formatting here as needed
    formatted_response = "\n".join(line.strip() for line in output_text.split("\n"))
    return f"Context: {context[:500]}...\nResponse: {formatted_response}"

# Main execution function
def main(question, pdf_path):
    print("Hi Sidra Saleem!")
    wandb.log({"Greeting": "Hi Sidra Saleem!"})
    
    raw_text = get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(raw_text)
    
    # Log text extraction
    wandb.log({"Raw Text Length": len(raw_text), "Number of Chunks": len(text_chunks)})
    
    create_vector_store(text_chunks)

    # Run the coroutine using the existing event loop
    response = asyncio.get_event_loop().run_until_complete(get_answer(question, raw_text))
    
    print(response)
    wandb.log({"Response": response, "Context": raw_text[:500]})

# Example usage
pdf_path = "/content/L1- Introduction To Orthopedics.pdf"  # Change this to your actual PDF file path
question = "What are the diseases discussed and their treatment?"
main(question, pdf_path)
