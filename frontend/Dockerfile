# Build and run React app in one container
FROM node:18-alpine

WORKDIR /app

# install dependenies
COPY package*.json ./
RUN npm install

# copy the env file for Docker
COPY .env.compose .env

# Copy source code
COPY . .

# Expose the port React runs on
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]