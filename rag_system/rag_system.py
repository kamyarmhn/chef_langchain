from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv
from food_knowledge import FOOD_KNOWLEDGE

# Load environment variables
load_dotenv()

class FoodRAGSystem:
    def __init__(self, model_name="llama2"):
        # Initialize Ollama model
        self.llm = Ollama(
            model=model_name,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize vector store
        self.vector_store = None
        
        # Initialize QA chain
        self.qa_chain = None

    def create_vector_store(self, documents):
        """Create a vector store from the provided documents."""
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        
        return self.vector_store

    def create_qa_chain(self):
        """Create a QA chain for querying the knowledge base."""
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
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        return self.qa_chain

    def query(self, question):
        """Query the knowledge base with a question."""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call create_qa_chain() first.")
        
        result = self.qa_chain({"query": question})
        return result

def main():
    # Initialize the RAG system
    rag_system = FoodRAGSystem()
    
    # Create vector store and QA chain
    print("Creating vector store...")
    rag_system.create_vector_store(FOOD_KNOWLEDGE)
    
    print("Creating QA chain...")
    rag_system.create_qa_chain()
    
    # Interactive query loop
    print("\nFood Knowledge RAG System")
    print("Ask questions about food, nutrition, or cooking (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        question = input("\nYour question: ")
        if question.lower() == 'quit':
            break
            
        try:
            result = rag_system.query(question)
            print("\nAnswer:", result['result'])
            print("\nSources:")
            for doc in result['source_documents']:
                print(f"- {doc.page_content[:200]}...")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 