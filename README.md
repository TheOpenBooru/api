# API

## Deployment

### Requirements

- linux
  - other platforms may work, but are untested
- python >= 3.10
- hcaptcha

### Instructions

Configure the config.yml, the config section contains the required settings.

```bash
# Create a virtualenv
python3.10 -m venv venv

# Install requirements
./venv/bin/pip install -r requirements.txt

# Start the app
./venv/bin/python main.py
```
