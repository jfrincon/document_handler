# Document handler

This project implements a backend application leveraging Python, Django, and OpenAI to process and retrieve information from uploaded .docx documents.

## Functionality
The application offers two core functionalities accessible through RESTful APIs:

### 1.Process and Store Documents (.docx):

- Users upload .docx documents via a designated endpoint.
- The application utilizes the Langchain library to interact with the OpenAI API, extracting textual content and generating vector embeddings.
- Generated embeddings are stored efficiently within a chosen vector database (e.g., Qdrant, Weaviate, Vespa) configured and deployed using Docker.
### 2.Search and Retrieve Information:
- Users submit text queries through a separate endpoint.
- The application searches the vector database for documents with embeddings closest to the query embedding.
- Based on the retrieved documents, the application responds to the user's query.

## Installation
The application is containerized for ease of deployment. The only prerequisite is Docker itself.

### Prerequisites
- Docker installed on your system.

### Steps
- Clone the project repository locally and navigate to the project directory
```bash
$ git clone <repository_url>
$ cd document_handler
```
- To interact with the OpenAI API, create a file named config.py and add your OpenAI API key:
```bash
OPENAI_API_KEY = <your-api-key>
```

- Run docker-compose up to build and start the application with all its dependencies
```bash
$ docker compose up -d
```

## Usage

### Uploading Documents

Once the application is running, you can access the upload endpoint at http://localhost:8000/upload. Initially, the database will be empty. To populate it, you can upload your own .docx files or use the example files provided in the /test folder within this project.

### Searching for Information
After uploading documents, you can use the search endpoint at http://localhost:8000/search to search for relevant information within the uploaded .docx files. Simply submit a text query, and the application will retrieve the most fitting documents based on vector similarity.



