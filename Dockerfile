# syntax=docker/dockerfile:1
FROM python:3.10-buster
COPY . .
RUN pip install -r requirements.txt
EXPOSE 57255
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "57255"]