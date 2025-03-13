# Chef Kamyar - Culinary Assistant

A bilingual (Persian/English) culinary assistant powered by RAG (Retrieval-Augmented Generation) technology. The system provides detailed recipes, cooking tips, and culinary knowledge in both Persian and English.

## Features

- Bilingual support (Persian/English)
- Detailed recipes from both Persian and international cuisines
- Cooking tips and techniques
- Nutritional information
- Interactive chat interface
- Admin panel for managing the knowledge base
- Docker support for easy deployment

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Ollama installed locally or running in a container
- NVIDIA GPU (recommended for better performance)

## Project Structure

```
.
├── chat_interface/          # Chat interface using Chainlit
│   ├── app.py              # Main chat application
│   └── requirements.txt    # Chat interface dependencies
├── admin_panel/           # Admin panel using Streamlit
│   ├── app.py            # Admin panel application
│   ├── Dockerfile        # Admin panel Dockerfile
│   └── requirements.txt  # Admin panel dependencies
├── rag_system/           # RAG system implementation
│   ├── rag.py           # RAG system core
│   ├── food_knowledge.py # International recipes
│   └── persian_recipes.py # Persian recipes
├── Dockerfile           # Main application Dockerfile
├── docker-compose.yml   # Docker Compose configuration
└── README.md           # This file
```

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chef-kamyar.git
cd chef-kamyar
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
# Install chat interface dependencies
cd chat_interface
pip install -r requirements.txt

# Install admin panel dependencies
cd ../admin_panel
pip install -r requirements.txt
```

4. Start Ollama (if not already running):
```bash
ollama serve
```

5. Run the applications:
```bash
# Terminal 1 - Chat Interface
cd chat_interface
chainlit run app.py

# Terminal 2 - Admin Panel
cd admin_panel
streamlit run app.py
```

### Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chef-kamyar.git
cd chef-kamyar
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The applications will be available at:
- Chat Interface: http://localhost:8000
- Admin Panel: http://localhost:8501
- Ollama API: http://localhost:11434

## Usage

### Chat Interface

1. Open http://localhost:8000 in your browser
2. Start chatting with Chef Kamyar in Persian or English
3. Ask questions about recipes, cooking techniques, or nutritional information

### Admin Panel

1. Open http://localhost:8501 in your browser
2. Navigate between Persian and International recipes
3. Add, edit, or delete recipes
4. Manage the knowledge base

## Development

### Adding New Recipes

1. Access the admin panel
2. Click "Add New Recipe"
3. Select the recipe type (Persian or International)
4. Fill in the recipe details
5. Save the recipe

### Modifying the Knowledge Base

The knowledge base is stored in two files:
- `rag_system/persian_recipes.py`: Persian recipes
- `rag_system/food_knowledge.py`: International recipes

You can modify these files directly or use the admin panel.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
