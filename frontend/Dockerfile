# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the client application
COPY . .

# Build the app for production
RUN npm run build

# Install `serve` to serve the build directory on port 5000
RUN npm install -g serve

# Command to run the app
CMD ["serve", "-s", "build", "-l", "5000"]

# Expose port 5000 to the outside once the container is running
EXPOSE 5000
