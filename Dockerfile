# syntax=docker/dockerfile:1
FROM python:3.10-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 57255
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "57255"]