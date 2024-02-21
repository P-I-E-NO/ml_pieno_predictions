FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
ENV FUEL Benzina
ENV MODE Web
CMD ["python3", "PREDICT.py"]