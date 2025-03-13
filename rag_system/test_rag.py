from rag_system import FoodRAGSystem
from food_knowledge import FOOD_KNOWLEDGE

def test_rag_system():
    # Initialize the RAG system
    print("Initializing RAG system...")
    rag = FoodRAGSystem()
    
    # Create vector store
    print("\nCreating vector store...")
    rag.create_vector_store(FOOD_KNOWLEDGE)
    
    # Create QA chain
    print("Creating QA chain...")
    rag.create_qa_chain()
    
    # Test questions
    test_questions = [
        "What are the nutritional facts for pizza?",
        "How many calories are in a hamburger?",
        "What are some healthy eating tips?",
        "What are the different cooking methods?",
        "What are the recommended daily nutritional guidelines?"
    ]
    
    # Run tests
    print("\nRunning test questions...")
    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            result = rag.query(question)
            print(f"Answer: {result['result']}")
            print("\nSources:")
            for doc in result['source_documents']:
                print(f"- {doc.page_content[:200]}...")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_rag_system() 