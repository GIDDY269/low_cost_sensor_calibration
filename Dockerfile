FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app


RUN apt update -y && apt install awscli -y


RUN pip install -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]