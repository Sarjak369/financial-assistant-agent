# Use a Debian-based Python image (Bullseye is a stable base)
FROM python:3.11-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Update package lists and install Java and procps (provides 'ps' command)
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    procps \
    && apt-get clean

# Set JAVA_HOME environment variable based on our inspection
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Verify Java installation (prints Java version)
RUN java -version

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your backend code into the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run the FastAPI app using Uvicorn. Using "sh -c" ensures environment variables are in effect.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
