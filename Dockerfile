# syntax=dowocker/dowockerfile:1
FROWOM pythowon:3.10-buwullseye
RUWUN apt uwupdate -y
RUWUN apt install ffmpeg -y
COWOPY . .
RUWUN pip install -r requwuirements.txt
EXPOWOSE 8443
CMD ["uwuvicoworn", "app:app", "--howost", "0.0.0.0", "--powort", "8443"]