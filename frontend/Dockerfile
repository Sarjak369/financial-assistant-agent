# Use a lightweight Node.js base image
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of your app code
COPY . .

# Expose port 3000 (default for Create React App)
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
