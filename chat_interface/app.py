"""
Chat interface for the food knowledge RAG system.
"""
import chainlit as cl
from rag_system.rag import FoodRAGSystem, load_knowledge
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize RAG system
rag_system = FoodRAGSystem()

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    await cl.Message(
        content="Hello! I'm Chef Kamyar, your culinary expert. How can I help you today?\n\n"
                "You can ask me about:\n"
                "- Persian recipes\n"
                "- Cooking tips\n"
                "- Cooking methods\n"
                "- Nutritional information\n"
                "and any other food-related topics.",
        author="Chef Kamyar"
    ).send()

    # Initialize knowledge base
    await cl.Message(
        content="Preparing recipes...",
        author="Chef Kamyar"
    ).send()

    try:
        documents = load_knowledge()
        rag_system.create_vector_store(documents)
        rag_system.create_qa_chain()
        await cl.Message(
            content="✅ Recipes are ready! What would you like to know?",
            author="Chef Kamyar"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Sorry, there was an error preparing the recipes: {str(e)}",
            author="Chef Kamyar"
        ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    # Show thinking message
    thinking_msg = cl.Message(content="Checking recipes...", author="Chef Kamyar")
    await thinking_msg.send()

    try:
        # Get response from RAG system
        answer, sources = rag_system.query(message.content)
        
        # Create response message
        response = cl.Message(content=answer, author="Chef Kamyar")
        
        # Add source previews if available
        if sources:
            response.content += "\n\n**Sources:**"
            for i, source in enumerate(sources, 1):
                preview = source.page_content[:200] + "..." if len(source.page_content) > 200 else source.page_content
                response.content += f"\n\n{i}. {source.metadata.get('source', 'Unknown')}:\n{preview}"
        
        await response.send()
    except Exception as e:
        await cl.Message(
            content=f"❌ Sorry, there was an error answering your question: {str(e)}",
            author="Chef Kamyar"
        ).send()

if __name__ == "__main__":
    cl.run() 