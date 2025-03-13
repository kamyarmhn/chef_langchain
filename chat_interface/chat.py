import chainlit as cl
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
import sys

# Add the parent directory to the Python path to import the food knowledge
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag_system.food_knowledge import FOOD_KNOWLEDGE

class FoodRAGSystem:
    def __init__(self):
        # Initialize the Ollama model
        self.llm = OllamaLLM(model="llama3.2")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings()
        
        # Initialize vector store and QA chain as None
        self.vector_store = None
        self.qa_chain = None

    def create_vector_store(self, documents):
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )

    def create_qa_chain(self):
        # Define prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )

    def query(self, question: str):
        if not self.qa_chain:
            self.create_qa_chain()
        return self.qa_chain.invoke({"query": question})

# Initialize RAG system
rag = FoodRAGSystem()

# Create vector store from food knowledge
rag.create_vector_store(FOOD_KNOWLEDGE)

@cl.on_chat_start
async def start():
    """
    Initializes the chat session
    """
    await cl.Message(
        content="Hello! I'm your food knowledge assistant. I can help you with questions about food, nutrition, and cooking methods. What would you like to know?",
        author="Assistant"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """
    Handles incoming messages
    """
    # Get the user's message
    question = message.content
    
    # Process the question using RAG system
    try:
        result = rag.query(question)
        
        # Create response message
        response = f"Answer: {result['result']}\n\nSources:"
        
        # Add source documents
        for doc in result['source_documents']:
            response += f"\n- {doc.metadata.get('source', 'Unknown source')}"
        
        # Send response
        await cl.Message(
            content=response,
            author="Assistant"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"I apologize, but I encountered an error: {str(e)}",
            author="Assistant"
        ).send()

if __name__ == "__main__":
    cl.run_async(main()) 