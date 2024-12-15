# Install requirements if not already installed
echo "Installing requirements..."
pip install flask pypdf2 chromadb langchain langchain-ollama sentence-transformers

# Start the Flask application
echo "Starting the application..."
python app.py