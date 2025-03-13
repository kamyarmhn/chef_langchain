"""
RAG (Retrieval-Augmented Generation) system for food knowledge using Ollama.
"""
from typing import List, Dict, Any, Tuple
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import json
from pathlib import Path

class FoodRAGSystem:
    """
    A RAG system for answering food-related questions using local Ollama models.
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize the RAG system.
        
        Args:
            model_name: Name of the Ollama model to use (default: llama3.2)
        """
        # Initialize Ollama for both LLM and embeddings
        self.model_name = model_name
        self.llm = OllamaLLM(model=model_name)
        self.embeddings = OllamaEmbeddings(model=model_name)
        
        # Initialize text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize storage
        self.vector_store = None
        self.qa_chain = None
        
        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are Chef Kamyar, a professional chef. Please answer the following questions using the provided information.
            If the information is not sufficient, please say that you cannot answer the question.
            If a recipe is found in the text, provide it in complete detail.

            Context:
            {context}

            Question: {question}

            Answer:"""
        )

    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Create a vector store from documents.
        
        Args:
            documents: List of Document objects containing food knowledge
        """
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        
        # Create and persist vector store
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory="./food_knowledge_db"
        )
        self.vector_store.persist()

    def create_qa_chain(self) -> None:
        """
        Create the question-answering chain.
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
            
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={
                    "k": 3  # Retrieve more documents
                }
            ),
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Query the RAG system with a question.
        
        Args:
            question: The question to answer
            
        Returns:
            Tuple containing the answer and source documents
        """
        if not self.qa_chain:
            self.create_qa_chain()
            
        try:
            # Handle identity questions directly
            identity_questions = ["what's your name", "who are you", "what is your name", "who are you?", "what's your name?"]
            if any(q in question.lower() for q in identity_questions):
                return "I am Chef Kamyar, your personal culinary expert! I'm passionate about cooking and love sharing my knowledge about food, recipes, and cooking techniques. How can I assist you with your culinary questions today?", []
            
            # Clean and normalize the question
            question = question.strip().lower()
            
            # Handle recipe queries
            if any(word in question for word in ["recipe", "how to", "how do i", "ingredients", "cook"]):
                # Add context to the question
                question = f"recipe for {question}"
                
            # Handle regular food-related questions
            result = self.qa_chain.invoke({"query": question})
            return result["result"], result.get("source_documents", [])
        except Exception as e:
            return f"Sorry, there was an error answering your question: {str(e)}", []

def load_knowledge() -> List[Document]:
    """Load knowledge base from JSON file."""
    import json
    from pathlib import Path
    
    # Load JSON file
    json_path = Path(__file__).parent.parent / "data" / "food_knowledge.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Convert JSON data to Document objects
    documents = []
    for item in data:
        doc = Document(
            page_content=item["page_content"],
            metadata=item["metadata"]
        )
        documents.append(doc)
    
    return documents 