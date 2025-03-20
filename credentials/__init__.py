#credentials/__init__.py

def load_secrets():
    """
    Load API secrets from either a .secrets file or environment variables.
    
    This function first attempts to load secrets from the credentials/.secrets
    file in the project root. If the file doesn't exist, it falls back to
    loading from environment variables.
    
    Returns
    -------
    dict
        Dictionary containing the following keys:
        - API_KEY : str
            Alpaca API key for authentication
        - SECRET_KEY : str
            Alpaca secret key for authentication
        - ENDPOINT_URL : str
            Alpaca API endpoint URL
    
    Notes
    -----
    The .secrets file should be formatted with KEY=VALUE pairs, one per line:
    API_KEY=your_api_key
    SECRET_KEY=your_secret_key
    ENDPOINT_URL=your_endpoint_url
    
    If using environment variables, they should be named:
    - ALPACA_API_KEY
    - ALPACA_SECRET_KEY
    - ALPACA_ENDPOINT_URL
    
    Examples
    --------
    >>> secrets = load_secrets()
    >>> api_key = secrets['API_KEY']
    >>> secret_key = secrets['SECRET_KEY']
    """
    # Get project root directory
    project_root = Path(__file__).parent.parent
    secrets_path = project_root / 'credentials' / '.secrets'
    
    if secrets_path.exists():
        # Load from .secrets file
        with open(secrets_path) as f:
            secrets = {}
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    secrets[key] = value
            return secrets
    else:
        # Fallback to environment variables
        return {
            'API_KEY': os.getenv('ALPACA_API_KEY'),
            'SECRET_KEY': os.getenv('ALPACA_SECRET_KEY'),
            'ENDPOINT_URL': os.getenv('ALPACA_ENDPOINT_URL')
        }