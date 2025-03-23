#credentials/__init__.py

from pathlib import Path

# Load secrets from credentials/.secrets
secrets_path = Path(__file__).parent / '.secrets'
secrets = {}
if secrets_path.exists():
    with open(secrets_path) as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                # Remove quotes from value (~"..." or '...')
                secrets[key] = value.strip('"').strip("'")
    if not all(k in secrets for k in ['ALPACA_API_KEY', 'ALPACA_SECRET_KEY', 'ALPAKA_ENDPOINT_URL']):
        raise ValueError("credentials/.secrets missing required keys (Key, Secret, Endpoint)—add your Alpaca API credentials!")
else:
    raise FileNotFoundError("credentials/.secrets not found—add your Alpaca API keys (Key, Secret, Endpoint)!")

# Export credentials
ALPACA_API_KEY = secrets['ALPACA_API_KEY']
ALPACA_SECRET_KEY = secrets['ALPACA_SECRET_KEY']
ALPAKA_ENDPOINT_URL = secrets['ALPAKA_ENDPOINT_URL']