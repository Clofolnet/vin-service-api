# Base Image
FROM python:3.8.10

# Prohibit writing pyc files, prohibit buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN mkdir /vin_service
# Set the /vin_service directory as the working directory
WORKDIR /vin_service

# Copies from your local machine's current directory to the project folder 
# in the Docker image
COPY . .

# Install the requirements.txt file in Docker image
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt