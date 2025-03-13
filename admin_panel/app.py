"""
Admin panel for managing the food knowledge base.
"""
import streamlit as st
import json
from pathlib import Path
from typing import List, Dict, Any
from langchain.schema import Document

# Set page config
st.set_page_config(
    page_title="Chef Kamyar - Admin Panel",
    page_icon="👨‍🍳",
    layout="wide"
)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
FOOD_KNOWLEDGE_FILE = PROJECT_ROOT / "data" / "food_knowledge.json"

def load_documents() -> List[Document]:
    """Load documents from the JSON file."""
    if not FOOD_KNOWLEDGE_FILE.exists():
        st.error(f"File not found: {FOOD_KNOWLEDGE_FILE}")
        return []
    
    try:
        with open(FOOD_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Document(**item) for item in data]
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")
        return []

def save_documents(documents: List[Document]):
    """Save documents to the JSON file."""
    try:
        data = []
        for doc in documents:
            data.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
            
        with open(FOOD_KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        st.error(f"Error saving documents: {str(e)}")

def create_document_form() -> Dict[str, Any]:
    """Create a form for adding/editing a document."""
    with st.form("document_form"):
        title = st.text_input("Title")
        
        # Recipe details
        ingredients = st.text_area("Ingredients (one per line)")
        instructions = st.text_area("Instructions (one per line)")
        
        # Nutritional information
        st.subheader("Nutritional Information (per 100g)")
        calories = st.number_input("Calories", min_value=0)
        protein = st.number_input("Protein (g)", min_value=0)
        carbs = st.number_input("Carbohydrates (g)", min_value=0)
        fat = st.number_input("Fat (g)", min_value=0)
        
        source = st.selectbox("Source", ["Persian Recipes", "International Recipes"])
        category = st.selectbox(
            "Category",
            ["Main Dish", "Soup", "Appetizer", "Dessert", "Tips", "Techniques"]
        )
        
        submitted = st.form_submit_button("Save Recipe")
        
        if submitted and title:
            # Format ingredients and instructions
            ingredients_list = ingredients.strip().split("\n")
            instructions_list = instructions.strip().split("\n")
            
            # Create the content
            content = f"{title}\n\nIngredients:\n"
            for ing in ingredients_list:
                if ing.strip():
                    content += f"- {ing.strip()}\n"
                    
            content += f"\nInstructions:\n"
            for i, inst in enumerate(instructions_list, 1):
                if inst.strip():
                    content += f"{i}. {inst.strip()}\n"
                    
            content += f"\nNutritional Information (per 100g):\n"
            content += f"- Calories: {calories}\n"
            content += f"- Protein: {protein}g\n"
            content += f"- Carbohydrates: {carbs}g\n"
            content += f"- Fat: {fat}g"
            
            return {
                "page_content": content,
                "metadata": {
                    "source": source,
                    "category": category
                }
            }
    return None

def main():
    st.title("👨‍🍳 Chef Kamyar - Admin Panel")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Persian Recipes", "International Recipes", "Add New Recipe"]
    )
    
    # Load all documents
    documents = load_documents()
    
    if page in ["Persian Recipes", "International Recipes"]:
        source = "Persian Recipes" if page == "Persian Recipes" else "International Recipes"
        st.header(page)
        
        # Filter recipes by source
        filtered_docs = [doc for doc in documents if doc.metadata.get("source") == source]
        
        if not filtered_docs:
            st.warning(f"No {page.lower()} found.")
        else:
            for i, doc in enumerate(filtered_docs):
                title = doc.page_content.split('\n')[0]
                with st.expander(f"Recipe {i+1}: {title}"):
                    edited_content = st.text_area("Content", doc.page_content, key=f"recipe_{i}", height=400)
                    st.json(doc.metadata)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save Changes", key=f"save_{i}"):
                            doc.page_content = edited_content
                            save_documents(documents)
                            st.success("Changes saved!")
                            
                    with col2:
                        if st.button("Delete", key=f"delete_{i}"):
                            documents.remove(doc)
                            save_documents(documents)
                            st.success("Recipe deleted!")
                            st.experimental_rerun()
    
    else:  # Add New Recipe
        st.header("Add New Recipe")
        
        # Create and handle the form
        new_doc = create_document_form()
        if new_doc:
            documents.append(Document(**new_doc))
            save_documents(documents)
            st.success("Recipe added successfully!")
            st.experimental_rerun()

if __name__ == "__main__":
    main() 