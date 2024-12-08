# SecureAsk
SecureAsk: An open-source RAG-based AI tool providing secure, accurate answers from your uploaded documents with privacy in mind.

# SecureAsk: An Open-Source RAG-Based Q&A App

**SecureAsk** is an open-source Retrieval-Augmented Generation (RAG) app designed to answer questions based on uploaded documents securely and efficiently. Whether you’re handling customer queries, analyzing project data, or simplifying document-based insights, SecureAsk ensures your data remains private and your answers precise.

## Features

- **Document-Based Q&A**: Upload `.txt` files, and SecureAsk provides accurate answers derived from your data.  
- **Advanced AI Models**: Combines HuggingFace embeddings and GPT-2 for robust document understanding and response generation.  
- **Open-Source and Free**: Designed to be accessible and customizable for everyone.  
- **Privacy First**: Your uploaded data stays local, ensuring security and confidentiality.  

## Included Example Document

A sample document, `emailExample.txt`, is provided to help you test the app's functionality. It contains mock data to demonstrate how SecureAsk can handle inquiries and generate responses.

## Getting Started

1. **Install Dependencies**:  
   Ensure you have Python and the required packages installed. Run the following command 

2. **Set Environment Variables**:  
   Create a `.env` file to store any required API keys or configurations.

3. **Run the App**:  
   Launch the app locally:  
   ```bash
   python SecureAsk.py
   ```

4. **Test the Example**:  
   Upload `emailExample.txt` through the app interface to see how it processes and answers questions.

## How It Works

1. Upload `.txt` files containing the data you want to query.  
2. SecureAsk indexes the documents using FAISS and generates embeddings via Sentence Transformers.  
3. Enter your query to retrieve relevant document sections and generate a tailored response.


## License

This project is open-source.

Start exploring SecureAsk and experience the power of RAG for your document-based Q&A needs! 🚀
