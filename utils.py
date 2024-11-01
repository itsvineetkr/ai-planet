from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from pathlib import Path
import os

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

template = """
Based only on the provided context, answer the question directly and concisely.
Do not add extra information, restate the question, or generate additional questions.
Start your response immediately with the answer.

<context>
{context}
</context>
Question: {input}
Answer:
"""


def make_pdf_content_vector_db(filename, filepath):
    """
    Processes a PDF file to create a vector database of its content.
    Args:
        filename (str): The name of the file to save the vector database.
        filepath (str): The path to the PDF file to be processed.
    Returns:
        None
    This function performs the following steps:
    1. Loads the PDF file from the given filepath using PyPDFLoader.
    2. Splits the document into chunks using RecursiveCharacterTextSplitter.
    3. Creates a vector database from the document chunks using FAISS and HuggingFaceEmbeddings.
    4. Saves the vector database locally in the specified directory.
    """
    loader = PyPDFLoader(filepath)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(document)
    db = FAISS.from_documents(documents, HuggingFaceEmbeddings())
    db.save_local(UPLOADS_DIR / "vec_db" / filename)


async def get_answer(question, filename):
    """
    Retrieves an answer to a question from a document.
    Args:
        question (str): The question to answer.
        filename (str): The name of the file containing the document.
    Returns:
        str: The answer to the question.
    This function performs the following steps:
    1. Loads the vector database from the specified file.
    2. Creates a retriever from the vector database.
    3. Initializes a HuggingFaceEndpoint for language model generation.
    4. Creates a document chain and a retrieval chain.
    5. Invokes the retrieval chain with the input question.
    6. Returns the answer generated by the retrieval chain.
    """
    
    db = FAISS.load_local(
        UPLOADS_DIR / "vec_db" / filename,
        embeddings=HuggingFaceEmbeddings(),
        allow_dangerous_deserialization=True,
    )
    retriver = db.as_retriever()
    endpoint_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    llm = HuggingFaceEndpoint(
        endpoint_url=endpoint_url, temperature=0.2, max_tokens=400
    )

    prompt = ChatPromptTemplate.from_template(template)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriver, document_chain)
    response = retrieval_chain.invoke({"input": question})
    return response["answer"]
