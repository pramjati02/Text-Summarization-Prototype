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

# run app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
