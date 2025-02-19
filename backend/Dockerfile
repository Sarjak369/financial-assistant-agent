# Use a lightweight Python image
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /app

# Install Java 11 and required dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    procps \
    && apt-get clean

# Set Java environment variables to the correct path
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Verify Java installation
RUN java -version

# Copy dependency files first (for better Docker caching)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the backend port
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
