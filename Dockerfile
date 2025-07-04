# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-b", ":8080", "wsgi:app"]
