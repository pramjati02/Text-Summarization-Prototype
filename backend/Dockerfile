# import official python image
FROM python:3.10-slim

# set working directory in container
WORKDIR /app

# install dependencies 
COPY requirements.txt .
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# expose app port
EXPOSE 8000

# run app with uvicorn
CMD ["fastapi", "run"]
