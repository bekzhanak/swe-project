# Use official Python image as a base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install netcat and other required tools
RUN apt-get update && apt-get install -y gcc netcat

# Copy project files to the container
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Copy the entrypoint script
COPY ./entrypoint.sh /app/entrypoint.sh

# Ensure the entrypoint script has the correct permissions
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]