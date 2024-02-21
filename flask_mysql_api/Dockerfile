FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python3", "api.py"]