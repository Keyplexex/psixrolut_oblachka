FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=5003
ENV APP_NAME=Good-App

EXPOSE 5003

USER nobody

CMD ["python", "app.py"]