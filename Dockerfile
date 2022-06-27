# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
RUN apt update -y && apt install ffmpeg -y
COPY . .
RUN pip install -r requirements.txt
EXPOSE 443
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "443"]