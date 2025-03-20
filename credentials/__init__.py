#credentials/__init__.py

from pathlib import Path

# Load secrets from credentials/.secrets (~relative to credentials/)
secrets_path = Path(__file__).parent / '.secrets'
secrets = {}
if secrets_path.exists():
    with open(secrets_path) as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                secrets[key] = value
    # Check if required keys are loaded
    if not all(k in secrets for k in ['Key', 'Secret', 'Endpoint']):
        raise ValueError("credentials/.secrets missing required keys (Key, Secret, Endpoint)—add your Alpaca API credentials!")
else:
    raise FileNotFoundError("credentials/.secrets not found—add your Alpaca API keys (Key, Secret, Endpoint)!")

# Export credentials (~for 'from credentials import ...')
API_KEY = secrets['Key']
SECRET_KEY = secrets['Secret']
ENDPOINT_URL = secrets['Endpoint']