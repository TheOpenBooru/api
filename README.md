# API

[API Link](https://api.openbooru.org)

The goals of Open Booru is to improve standardisation amongst boorus as well as seperating the GUI from the API so they can become application agnostic. This way sites such as https://r34.app can implement their own GUI for a booru.

It's been in production since November 2021

## Installation

Edit the config.yml, the config section contains the required settings.

### Requirements

- ubuntu
  - other platforms may work, but are untested
- python >= 3.9
- ffmpeg
- hcaptcha

### Ubuntu/Debian

```bash
# Install libraries
sudo apt-get install -y libmagic1 ffmpeg

# Create a virtualenv
python3.9 -m venv venv

# Install requirements
./venv/bin/pip install -r requirements.txt

# Start the app
./venv/bin/python app.py
```

### Windows

You must manually install ffmpeg and it add it to the PATH

```powershell
# Create a virtualenv
python3.9 -m venv venv

# Install requirements
.\venv\Scripts\pip.exe install python-magic-bin
.\venv\Scripts\pip.exe install -r requirements.txt

# Start the app
.\venv\Scripts\python.exe app.py
```

## Development

To run tests use this command:

```py
./venv/bin/python -m pytest"
```
