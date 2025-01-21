# Flask ETL Pipeline

## Overview
This project is a Flask-based ETL (Extract, Transform, Load) pipeline that allows users to upload CSV files via a REST API, process the data, and store the processed files locally. The application uses Celery for background task processing and Redis as the message broker.

## Features
- Upload CSV files via REST API.
- Data transformation and validation.
- Local storage for processed data.
- Celery for asynchronous processing.
- Environment variable management using dotenv.

## Technologies Used
- Flask
- Pandas
- Celery
- Redis
- Python Dotenv
- Docker (optional)

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Redis server

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/stwins60/csv-etl-pipeline.git
   cd csv-etl-pipeline
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```env
   UPLOAD_FOLDER=uploads
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

5. Run Redis server:
   ```bash
   redis-server
   ```

6. Start the Celery worker:
   ```bash
   celery -A app.celery worker --loglevel=info
   ```

7. Run the Flask application:
   ```bash
   python app.py
   ```

## API Endpoints

| Method | Endpoint       | Description                |
|--------|---------------|----------------------------|
| POST   | /upload        | Upload a CSV file          |
| GET    | /status/<task_id> | Get processing status of a file |

## Testing
You can test the API endpoints using Postman or `curl`:

- Upload a file:
  ```bash
  curl -X POST -F "file=@sample.csv" http://localhost:5000/upload
  ```

- Check status:
  ```bash
  curl http://localhost:5000/status/<task_id>
  ```

## Logs
The application logs can be monitored in the Flask and Celery output.

## License
This project is licensed under the MIT License.

