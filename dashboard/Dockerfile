FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# This is the corrected line - copy EVERYTHING from this folder
COPY . .

# Run the new Home.py file
CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]