# app.py
from flask import Flask, render_template, request, jsonify
from rag_assistant import RAGAssistant
import os

app = Flask(__name__)
assistant = RAGAssistant()

# Initialize the assistant with PDF document
def init_assistant():
    pdf_path = "bidding_document.pdf"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print("Initializing assistant...")
    print("Processing PDF document...")
    pdf_text = assistant.extract_text_from_pdf(pdf_path)
    
    print("Adding document to vector store...")
    assistant.add_documents([pdf_text])
    
    print("Assistant initialization complete!")
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json['question']
        if question.strip().lower() == 'exit':
            return jsonify({'answer': 'Goodbye! Thanks for using the assistant.'})
        
        answer = assistant.get_answer(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_assistant()
    app.run(debug=True)