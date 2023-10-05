# Autor: Florian Merlau

FROM python:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN apt-get update && \
    apt-get install -y curl gnupg vim && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point
CMD ["python", "-u", "main.py"]