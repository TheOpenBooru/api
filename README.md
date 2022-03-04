# API

The goals of Open Booru is to improve standardisation amongst boorus as well as seperating the GUI from the API so they can become application agnostic

## Deployment

### Requirements

- linux
  - other platforms may work, but are untested
- python >= 3.10
- hcaptcha

### Instructions

Edit the config.yml, the config section contains the required settings.

```bash
# Create a virtualenv
python3.10 -m venv venv

# Install requirements
./venv/bin/pip install -r requirements.txt

# Start the app
./venv/bin/python app.py
```
