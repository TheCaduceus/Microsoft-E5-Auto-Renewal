FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
