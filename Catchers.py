import os
from dotenv import load_dotenv
import gradio as gr
import logging
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import pipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure settings for the application
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Use Sentence Transformers for embeddings
llm_model_name = "gpt2"  # Use GPT-2 for text generation

# Initialize global variables
vector_store = None
llm_pipeline = pipeline("text-generation", model=llm_model_name)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)

# Function to load documents and create the index
def load_documents(file_paths):
    global vector_store
    try:
        if not file_paths:
            logger.error("No files selected.")
            return "Error: No files selected."

        documents = []

        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path.endswith('.txt'):
                logger.info(f"Loading file: {file_path}")
                loader = TextLoader(file_path)
                doc = loader.load()
                chunks = text_splitter.split_documents(doc)
                documents.extend(chunks)

        if not documents:
            logger.warning("No documents found in the selected files.")
            return "No documents found in the selected files."

        logger.info(f"Total documents (chunks) loaded: {len(documents)}")

        # Create a vector store using FAISS
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        vector_store = FAISS.from_documents(documents, embeddings)

        logger.info("Documents successfully indexed.")
        return f"Successfully loaded {len(documents)} document chunks."

    except Exception as e:
        logger.exception("Error loading documents:")
        return f"Error loading documents: {str(e)}"

import re

# Function to handle chat interactions
def chat(message, history):
    global vector_store
    if vector_store is None:
        return history + [("Please load documents first.", None)]
    
    try:
        # Query the vector store for similar documents
        similar_docs = vector_store.similarity_search(message, k=5)

        # Extract relevant information from similar documents for response generation
        prices = {}
        delivery_times = {}

        for doc in similar_docs:
            content = doc.page_content

            # Use regex to find the pricing and delivery details in the previous responses
            price_match = re.search(r"price for (\d+) units of Product Y is \$(\d+)", content)
            delivery_match = re.search(r"deliver within (\d+) days", content)

            if price_match:
                units = int(price_match.group(1))
                price = int(price_match.group(2))
                prices[units] = price
            
            if delivery_match:
                delivery_time = int(delivery_match.group(1))
                delivery_times[units] = delivery_time

        # Extract the number of units requested in the message
        unit_request_match = re.search(r"(\d+) units of Product Y", message)
        if unit_request_match:
            requested_units = int(unit_request_match.group(1))

            # Determine the closest price and delivery information available
            if requested_units in prices:
                response_text = f"Thank you for your query. The price for {requested_units} units of Product Y is ${prices[requested_units]} and we can deliver within {delivery_times[requested_units]} days."
            else:
                # Fallback to find the closest available pricing
                closest_units = min(prices.keys(), key=lambda x: abs(x - requested_units))
                estimated_price = prices[closest_units] * (requested_units / closest_units)
                estimated_delivery = delivery_times[closest_units] + 5  # Adjust as necessary
                response_text = f"Thank you for your inquiry. The price for {requested_units} units of Product Y is approximately ${int(estimated_price)} and we can deliver within {estimated_delivery} days."

        else:
            response_text = "I'm sorry, but I couldn't determine the quantity you requested."

        return history + [(message, response_text)]
    
    except Exception as e:
        logger.exception("Error processing query:")
        return history + [(message, f"Error processing query: {str(e)}")]




# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# RAG Q&A Chatbot for Email Responses")
    
    file_input = gr.File(label="Upload .txt files with email requests/responses", file_count="multiple", type="filepath")
    load_btn = gr.Button("Load Documents")
    load_output = gr.Textbox(label="Load Status", interactive=False)

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask your question about email responses", interactive=True)
    clear = gr.Button("Clear")

    # Set up event handlers
    load_btn.click(load_documents, inputs=[file_input], outputs=[load_output])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[chatbot])
    msg.submit(lambda: "", outputs=[msg])  # Clear message box
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(share=True)
