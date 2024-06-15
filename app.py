#Import Flask and other necessary modules.
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not connect_str:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set in environment variables")

container_name = 'images'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    image = request.files['image']
    filename = secure_filename(image.filename)
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(image)

    # Construct the URL for the uploaded blob
    blob_url = blob_client.url

    return jsonify({'message': 'Image uploaded successfully', 'url': blob_url}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



