import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

# Cache to store the token and its expiration time
_token_cache = {
    "access_token": None,
    "expires_at": None  # When the token will expire
}

def get_access_token():
    client_id = os.environ.get('BNET_CLIENT_ID')
    client_secret = os.environ.get('BNET_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise Exception("BNET_CLIENT_ID or BNET_CLIENT_SECRET is not set in the environment.")
    
    # Check if the cached token is still valid (within the 24-hour expiration window)
    if _token_cache["access_token"] and _token_cache["expires_at"] > datetime.now(timezone.utc):
        print("Using cached access token.")
        return _token_cache["access_token"]
    
    # Fetch a new token if the cache is empty or expired
    try:
        response = requests.post(
            'https://oauth.battle.net/token',
            auth=(client_id, client_secret),
            data={'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        data = response.json()
        
        # Cache the token and set expiration time 24 hours from now
        _token_cache["access_token"] = data["access_token"]
        _token_cache["expires_at"] = datetime.now(timezone.utc) + timedelta(hours=24)  # Explicit 24-hour expiration

        print("Fetched new access token.")
        return _token_cache["access_token"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to obtain access token: {e}")
