# Dockerfile for Node.js backend
FROM node:14

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies by copying
# package.json and package-lock.json
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

# Your server might run on a different port, so make sure to expose it
EXPOSE 4000

CMD ["node", "server.js"]
