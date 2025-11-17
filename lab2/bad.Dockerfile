FROM python

RUN pip install flask

COPY . .

ENV PORT=5003
ENV APP_NAME=Bad-App

CMD ["python", "app.py"]