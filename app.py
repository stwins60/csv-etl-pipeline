from flask import Flask, request, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename
from celery import Celery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Celery configuration
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        process_csv.delay(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@celery.task
def process_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        # Perform data transformation
        df['processed'] = True
        processed_filepath = filepath.replace('.csv', '_processed.csv')
        df.to_csv(processed_filepath, index=False)
        return {'message': 'File processed successfully', 'processed_file': processed_filepath}
    except Exception as e:
        return {'error': str(e)}

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_csv.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Task is pending'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
