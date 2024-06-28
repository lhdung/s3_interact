
import json
import os

from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request, send_file

from handler.file import S3Handler

app = Flask(__name__)

# Initialize the S3 handler

s3_handler = S3Handler(
    aws_access_key=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)


# List buckets
@app.route('/buckets', methods=['GET'])
def list_buckets():
    buckets = s3_handler.list_buckets()
    
    return jsonify(buckets)

# List objects in a bucket
@app.route('/buckets/<bucket_name>', methods=['GET'])
def list_objects(bucket_name):
    files = s3_handler.list_objects(bucket_name)
    return jsonify(files)


@app.route('/upload/<bucket_name>', methods=['POST'])
def upload_file(bucket_name):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    
    # Upload to S3
    if s3_handler.upload_file(bucket_name, file, filename):
        return jsonify({'message': f'File {filename} uploaded successfully to bucket {bucket_name}'}), 201
    else:
        return jsonify({'error': 'File upload failed. Duplicate file found or error occurred.'}), 409

# Delete file
@app.route('/bucket_name/file_name', methods=['Delete'])
def delete_file(bucket_name, file_name):
    filename = secure_filename(filename)
    s3_handler.delete_file(bucket_name, filename)
    return jsonify({'message': f'File {filename} deleted successfully from bucket {bucket_name}'}), 200


def main():
    app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()