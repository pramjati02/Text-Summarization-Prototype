
Files for text summarization prototype. Developed using FastAPI for backend and REACT for frontend. Model retrieved through HuggingFace repository (path found in backend/models files)

INSTRUCTIONS

Clone this repository

Install Nodejs: https://nodejs.org/en

Create a virtual environment (for safety reasons), then navigate to the frontend folder, and run "npm install".

Make sure that Docker is installed in your system so that you can use it in your terminal. I also have Docker Desktop so that I can come back to the containers whenever I want to.

Once you had done that, create a file called ".env.compose" and then paste the following (for development):
REACT_APP_FAST_API_URL='http://localhost:8000'

Once you have done this, in your terminal run "docker compose up"

This will create a Docker container for the frontend and backend. You can then access the prototype if you click on the localhost link for the frontend. If this does not work, this is likely due to the frontend missing some components. Refer to the following instructions below.

IMPORTANT FOR FRONTEND:
The frontend is usually missing node_modules and env files before "npm install", this is normal. Run this command one more time, then run "docker compose up"

In case the prototype frontend still cannot be recreated using this repository, create a new REACT frontend using "npx create-react-app frontend".
Then copy and paste the contents of App.js (under the src folder) and Dockerfile into the new frontend directory. Then delete the old frontend directory. 
Then create a ".env.compose" file with the contents:

REACT_APP_FAST_API_URL='http://localhost:8000'

For deployment, Ngrok was used for deployment using a Docker Compose. Download Ngrok for Docker on Docker Desktop. Create a custom URL (free) for the backend and expose on port 8000. Copy and paste the ngrok backend url into the .env file. Run "docker compose up" to initiate a build for a container containing both the backend and frontend. 