import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get API keys for exchanges
def get_exchange_credentials(exchange_name):
    """
    Get API key and secret for a specific exchange
    
    Args:
        exchange_name: Name of the exchange (e.g., 'binance', 'kucoin')
        
    Returns:
        dict with 'api_key' and 'api_secret'
    """
    exchange_name = exchange_name.upper()
    api_key = os.getenv(f"{exchange_name}_API_KEY", "")
    api_secret = os.getenv(f"{exchange_name}_API_SECRET", "")
    
    return {
        'api_key': api_key,
        'api_secret': api_secret
    }

# Function to check if API credentials are available for an exchange
def has_exchange_credentials(exchange_name):
    """
    Check if API credentials are available for a specific exchange
    
    Args:
        exchange_name: Name of the exchange (e.g., 'binance', 'kucoin')
        
    Returns:
        bool: True if both API key and secret are available
    """
    creds = get_exchange_credentials(exchange_name)
    return bool(creds['api_key'] and creds['api_secret'])