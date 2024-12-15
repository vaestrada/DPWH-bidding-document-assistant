# DPWH Bidding Assistant

An AI-powered document assistant that uses RAG (Retrieval Augmented Generation) to answer questions about DPWH bidding documents. Built with Llama 2, ChromaDB, and Flask.

## Features

- 📄 PDF document processing and analysis
- 🔍 Vector-based document retrieval using ChromaDB
- 🤖 LLM-powered question answering using Llama 2
- 💻 Interactive web interface
- ⚡ Real-time response streaming with typewriter effect
- 🎨 Modern, responsive UI design

## Prerequisites

- Python 3.8 or higher
- Ollama (with Llama 2 model installed)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dpwh-bidding-document-assistant.git
cd dpwh-bidding-document-assistant
```

2. Set up a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and run Ollama:
```bash
# Follow instructions at https://ollama.ai/download
# Then pull the Llama 2 model:
ollama run llama3.2
```

## Usage

1. Place your DPWH bidding document PDF in the root directory as 'bidding_document.pdf'

2. Start the application:
```bash
chmod +x start.sh  # Make start script executable (Unix/Linux only)
./start.sh
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
dpwh-document-assistant/
├── app.py                 # Flask application
├── rag_assistant.py       # RAG implementation
├── requirements.txt       # Project dependencies
├── start.sh              # Startup script
├── static/
│   └── style.css         # CSS styles
└── templates/
    └── index.html        # Web interface template
```

## Technology Stack

- **Backend Framework**: Flask
- **Language Model**: Llama 3.2 (via Ollama)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: HTML, CSS, JavaScript
- **PDF Processing**: PyPDF2

## Development

To contribute or modify:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. **PDF not loading**:
   - Ensure the PDF is named correctly as 'bidding_document.pdf'
   - Check file permissions

2. **Ollama connection error**:
   - Ensure Ollama is running
   - Check if Llama 3.2 model is properly installed

3. **ChromaDB errors**:
   - Clear the ChromaDB collection and restart
   - Check disk space for embeddings storage

## Support

For support, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed information about your problem
3. Include error messages and steps to reproduce
