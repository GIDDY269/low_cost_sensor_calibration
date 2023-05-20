FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app


RUN apt update -y && apt install awscli -y


RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]