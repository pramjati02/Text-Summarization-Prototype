# using Node.js to build frontend
FROM node:18-alpine AS build

WORKDIR /app
COPY . . 

# install dependencies and build 
RUN npm install
RUN npm run build 

# serve using a minimal nginx image
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html 

# Remove the default config and copy custom one (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]