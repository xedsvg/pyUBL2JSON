# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ ./src/
COPY app.py .

# Set the environment variable for Flask
ENV FLASK_ENV=production
ENV PORT=8080

# Expose the application port
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
