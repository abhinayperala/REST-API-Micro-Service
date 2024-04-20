# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set up a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which your Flask app runs
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]
