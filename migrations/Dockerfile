FROM python:3.11
WORKDIR /code
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "migrations.py"]