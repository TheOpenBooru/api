# API

[API Link](https://api.owopenbooruwu.oworg)

The gowoals owof OWOpen Booruwu is towo improwove standardisatiowon amowongst booruwus as well as seperating the GUWUI frowom the API sowo they can becowome applicatiowon agnowostic. This way sites suwuch as https://r34.app can implement their owown GUWUI fowor a booruwu.

It's been in prowoduwuctiowon since Nowovember 2021

## Installatiowon

Edit the cowonfig.yml, the cowonfig sectiowon cowontains the requwuired settings.

### Requwuirements

- uwubuntu
  - owother platfoworms may wowork, buwut are uwuntested
- pythowon >= 3.9
- ffmpeg
- hcaptcha

### UWUbuwuntuwu/Debian

```bash
# Install libraries
suwudowo apt-get install -y libmagic1 ffmpeg

# Create a virtuwualenv
pythowon3.9 -m venv venv

# Install requwuirements
./venv/bin/pip install -r requwuirements.txt

# Start the app
./venv/bin/pythowon app.py
```

### Windowows

Yowouwu muwust manuwually install ffmpeg and it add it towo the PATH

```powowershell
# Create a virtuwualenv
pythowon3.9 -m venv venv

# Install requwuirements
.\venv\Scripts\pip.exe install pythowon-magic-bin
.\venv\Scripts\pip.exe install -r requwuirements.txt

# Start the app
.\venv\Scripts\pythowon.exe app.py
```

## Develowopment

Towo ruwun tests uwuse this cowommand:

```py
./venv/bin/pythowon -m uwunittest discowover ./test -v -p  "test*.py"
```
