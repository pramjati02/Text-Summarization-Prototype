
Files for text summarization prototype. Developed using FastAPI for backend and REACT for frontend.

Model retrieved through HuggingFace repository (path found in backend/models files)

IMPORTANT FOR FRONTEND:
missing node_modules and env files.
In case the prototype frontend cannot be recreated using this repository, create a new REACT frontend using "npx create-react-app frontend".
Then copy and paste the contents of App.js (under the src folder) and Dockerfile into the new frontend directory.
App.js works with .env files. For local development, paste this into a ".env" file:

REACT_APP_FAST_API_URL='http://localhost:8000'

For deployment, Ngrok was used for deployment using a Docker Compose. Download Ngrok for Docker on Docker Desktop. Create a custom URL (free) for the backend and expose on port 8000. Create a new .env file called ".env.compose" for a Docker Compose. Copy and paste the ngrok bakcend url into the env file. Run "docker compose up" to initiate a build for a container containing both the backend and frontend. 