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

input_docx = r'aws\Data_Creation.docx'
output_csv = r'aws\output.csv'

paragraphs = extract_paragraphs_from_docx(input_docx)
save_paragraphs_to_csv(paragraphs, output_csv)

dataset = load_dataset(output_csv)

chatbot = create_chatbot(dataset)

@app1.route("/predict", methods=["POST"])
def predict():
    try:
        text = request.get_json().get("message")
        if text:
            response = chatbot(text)
            if response:
                message = {"answer": response}
                return jsonify(message)
            else:
                return jsonify({"error": "No response found."}), 400
        else:
            return jsonify({"error": "No 'message' provided in the request."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app1.run(debug=True)
