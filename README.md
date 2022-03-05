# API

The goals of Open Booru is to improve standardisation amongst boorus as well as seperating the GUI from the API so they can become application agnostic

## Installation

Edit the config.yml, the config section contains the required settings.

### Requirements

- linux
  - other platforms may work, but are untested
- python >= 3.10
- ffmpeg
- hcaptcha

### Ubuntu/Debian

```bash
# Install libraries
sudo apt-get install -y libmagic1 ffmpeg

# Create a virtualenv
python3.10 -m venv venv

# Install requirements
./venv/bin/pip install -r requirements.txt

# Start the app
./venv/bin/python app.py
```

### Windows

Sadly, you must manually install ffmpeg.

```powershell
# Create a virtualenv
python3.10 -m venv venv

# Install requirements
.\venv\Scripts\pip.exe install python-magic-bin
.\venv\Scripts\pip.exe install -r requirements.txt

# Start the app
.\venv\Scripts\python.exe app.py
```
