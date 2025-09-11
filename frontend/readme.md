missing node_modules and env files.
In case the prototype frontend cannot be recreated using this repository, create a new REACT frontend using "npx create-react-app frontend".
Then copy and paste the contents of App.js (under the src folder) and Dockerfile into the new frontend directory.
App.js works with .env files. For local development, paste this into the env file:

REACT_APP_FAST_API_URL='http://localhost:8000'

For Ngrok hosting, replace the URL with ngrok link for the backend