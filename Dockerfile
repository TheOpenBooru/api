# syntax=docker/dockerfile:1
FROM python:3.10-buster
COPY . .
RUN sudo apt install ffmpeg
RUN pip install -r requirements.txt
EXPOSE 8443
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8443"]