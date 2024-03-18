
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
# ENV PYTHONUNBUFFERED 1  # Uncomment if needed for debugging

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Expose port (usually Django runs on port 8000)
EXPOSE 8000

# Command to run the Django application (running with waitress)
CMD ["python", "server.py"]
