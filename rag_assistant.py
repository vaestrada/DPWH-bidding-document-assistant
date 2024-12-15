import os
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer
import textwrap
from PyPDF2 import PdfReader

class RAGAssistant:
    def __init__(self):
        # Initialize Ollama
        self.llm = OllamaLLM(model="llama3.2")
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.client = chromadb.Client()
        
        # Create collection with embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='all-MiniLM-L6-v2'
        )
        
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(
                name="dpwh_docs",
                embedding_function=self.embedding_function
            )
        except:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name="dpwh_docs",
                embedding_function=self.embedding_function
            )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        # Define RAG prompt template
        self.prompt_template = """
        You are a helpful assistant that answers questions about DPWH bidding documents.
        Answer the question based on the following context. If you cannot find the answer in the context, 
        say "I cannot find specific information about that in the provided documents."
        
        Provide specific references from the documents when possible.

        Context: {context}
        
        Question: {question}
        
        Answer: Let me help you with that.
        """
        
        self.rag_prompt = PromptTemplate.from_template(self.prompt_template)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
        
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None):
        """Add documents to the vector store"""
        # Split texts into chunks
        chunks = []
        for text in texts:
            chunks.extend(self.text_splitter.split_text(text))
            
        # Add documents to ChromaDB
        self.collection.add(
            documents=chunks,
            ids=[f"doc_{i}" for i in range(len(chunks))],
            metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunks))] if not metadatas else metadatas
        )
        
    def retrieve(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant documents for a query"""
        # Get total number of documents in collection
        total_docs = len(self.collection.get()['documents'])
        
        # Adjust n_results if it's greater than available documents
        actual_n_results = min(n_results, total_docs)
        
        results = self.collection.query(
            query_texts=[query],
            n_results=actual_n_results
        )
        return results['documents'][0]
        
    def get_answer(self, question: str) -> str:
        """Get answer for a question using RAG"""
        # Retrieve relevant contexts
        contexts = self.retrieve(question)
        context_text = "\n\n".join(contexts)
        
        # Create RAG chain
        rag_chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.rag_prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Get answer
        answer = rag_chain.invoke({"context": context_text, "question": question})
        return answer