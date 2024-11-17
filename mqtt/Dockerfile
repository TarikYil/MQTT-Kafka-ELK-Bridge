# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and scripts into the container
COPY requirements.txt .
COPY client/publisher.py .
COPY client/subscriber.py .

# Install necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run
CMD ["python", "publisher.py"]
