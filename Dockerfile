# Dockerfile
FROM python:3.9-alpine

RUN apk update && apk add ffmpeg

RUN pip install youtube_dl requests

RUN mkdir app
ADD https://raw.githubusercontent.com/SebastianMoyano/LidarrYoutube-Docker/main/Lidarr.py /app/

RUN cat /app/Lidarr.py

WORKDIR /app
CMD ["python", "Lidarr.py"]

