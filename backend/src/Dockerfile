FROM python:3.12

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app files
COPY . .

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Run Uvicorn when the container starts
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]