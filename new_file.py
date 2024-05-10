import docx
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from flask_cors import CORS

def extract_paragraphs_from_docx(docx_file):
    doc = docx.Document(docx_file)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return paragraphs

def save_paragraphs_to_csv(paragraphs, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Response'])
        for paragraph in paragraphs:
            writer.writerow([paragraph])

def load_dataset(csv_file):
    dataset = pd.read_csv(csv_file, header=0)
    return dataset

def create_chatbot(dataset):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(dataset['Response'])
    
    def get_response(user_input):
        user_input_vectorized = vectorizer.transform([user_input])
        similarities = cosine_similarity(user_input_vectorized, X)
        idx = similarities.argmax()
        response = dataset.loc[idx, 'Response']
        return response
    
    return get_response

app1 = Flask(__name__)
CORS(app1)

if __name__ == "__main__":
    # Replace 'input.docx' with the path to your Word document
    input_docx = r'aws\Data_Creation.docx'
    output_csv = r'aws\output.csv'
    output_csv

    # Extract paragraphs from DOCX and save to CSV
    paragraphs = extract_paragraphs_from_docx(input_docx)
    save_paragraphs_to_csv(paragraphs, output_csv)

    # Load dataset
    dataset = load_dataset(output_csv)

    # Create chatbot
    chatbot = create_chatbot(dataset)

    # Chatbot loop
    #print("Welcome! Ask me anything (type 'exit' to quit)")
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == 'exit':
    #         print("Goodbye!")
    #         break
    #     response = chatbot(user_input)
    #     print("Chatbot:", response)

@app1.route("/predict", methods=["POST"])
def predict():
    text = request.get_json().get("message")
    response = chatbot(text)
    message = {"answer": response}
    return jsonify(message)    
