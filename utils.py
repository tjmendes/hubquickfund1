import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import ccxt
import os

def format_currency(value, currency="$", decimals=2):
    """Format a number as currency with specified number of decimals"""
    if value is None:
        return "N/A"
    
    return f"{currency}{value:,.{decimals}f}"

def format_percentage(value, include_sign=True):
    """Format a number as percentage with + or - sign"""
    if value is None:
        return "N/A"
    
    sign = ""
    if include_sign and value > 0:
        sign = "+"
    elif include_sign and value < 0:
        sign = "-"
        value = abs(value)
    
    return f"{sign}{value:.2f}%"

def calculate_roi(initial_value, final_value):
    """Calculate Return on Investment (ROI) as percentage"""
    if initial_value == 0:
        return 0
    
    return ((final_value - initial_value) / initial_value) * 100

def calculate_apy_from_apr(apr, compounding_frequency=365):
    """Convert APR to APY based on compounding frequency
    
    Args:
        apr: Annual Percentage Rate (as decimal, e.g., 0.05 for 5%)
        compounding_frequency: Number of times compounded per year
            (1=annual, 12=monthly, 365=daily)
    
    Returns:
        APY as decimal
    """
    return (1 + apr / compounding_frequency) ** compounding_frequency - 1

def calculate_compound_interest(principal, rate, time, frequency=1):
    """Calculate compound interest
    
    Args:
        principal: Initial investment amount
        rate: Interest rate per period (as decimal)
        time: Number of time periods
        frequency: Compounding frequency (1=annual, 12=monthly, 365=daily)
    
    Returns:
        Final amount after compound interest
    """
    return principal * (1 + rate / frequency) ** (frequency * time)

def get_time_periods():
    """Get standard time periods for financial analysis"""
    today = datetime.now()
    
    periods = {
        "Today": {
            "start": today.replace(hour=0, minute=0, second=0),
            "end": today
        },
        "Yesterday": {
            "start": (today - timedelta(days=1)).replace(hour=0, minute=0, second=0),
            "end": (today - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        },
        "Last 7 Days": {
            "start": (today - timedelta(days=7)),
            "end": today
        },
        "Last 30 Days": {
            "start": (today - timedelta(days=30)),
            "end": today
        },
        "Month to Date": {
            "start": today.replace(day=1, hour=0, minute=0, second=0),
            "end": today
        },
        "Year to Date": {
            "start": today.replace(month=1, day=1, hour=0, minute=0, second=0),
            "end": today
        }
    }
    
    return periods

def timeframe_to_seconds(timeframe):
    """Convert a timeframe string to seconds
    
    Examples:
        "1m" -> 60
        "1h" -> 3600
        "1d" -> 86400
    """
    unit = timeframe[-1]
    value = int(timeframe[:-1])
    
    if unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 60 * 60
    elif unit == 'd':
        return value * 60 * 60 * 24
    elif unit == 'w':
        return value * 60 * 60 * 24 * 7
    elif unit == 'M':
        return value * 60 * 60 * 24 * 30
    else:
        return value

def resample_ohlcv(df, source_timeframe, target_timeframe):
    """Resample OHLCV data from one timeframe to another
    
    Args:
        df: DataFrame with 'timestamp', 'open', 'high', 'low', 'close', 'volume'
        source_timeframe: Source timeframe (e.g., "1m", "5m")
        target_timeframe: Target timeframe (e.g., "15m", "1h")
    
    Returns:
        Resampled DataFrame
    """
    # Ensure timestamp is datetime and set as index
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
    
    source_seconds = timeframe_to_seconds(source_timeframe)
    target_seconds = timeframe_to_seconds(target_timeframe)
    
    if target_seconds < source_seconds:
        st.error(f"Cannot resample from {source_timeframe} to {target_timeframe}. Target timeframe must be larger than source.")
        return df
    
    # Calculate the appropriate frequency string for pandas
    freq = None
    if 'm' in target_timeframe:
        freq = f"{target_timeframe[:-1]}T"
    elif 'h' in target_timeframe:
        freq = f"{target_timeframe[:-1]}H"
    elif 'd' in target_timeframe:
        freq = f"{target_timeframe[:-1]}D"
    
    # Resample using pandas
    resampled = pd.DataFrame()
    resampled['open'] = df['open'].resample(freq).first()
    resampled['high'] = df['high'].resample(freq).max()
    resampled['low'] = df['low'].resample(freq).min()
    resampled['close'] = df['close'].resample(freq).last()
    resampled['volume'] = df['volume'].resample(freq).sum()
    
    # Reset index to get timestamp as a column
    resampled = resampled.reset_index()
    
    return resampled

def create_exchange_instance(exchange_id, api_key=None, api_secret=None):
    """Create an instance of the specified exchange
    
    Args:
        exchange_id: ID of the exchange (e.g., 'binance', 'coinbase')
        api_key: Optional API key (if not provided, will check environment variables)
        api_secret: Optional API secret (if not provided, will check environment variables)
    
    Returns:
        Exchange instance from ccxt
    """
    # Try to get API credentials from parameters or environment variables
    if api_key is None:
        api_key = os.getenv(f"{exchange_id.upper()}_API_KEY", "")
    
    if api_secret is None:
        api_secret = os.getenv(f"{exchange_id.upper()}_API_SECRET", "")
    
    # Create exchange instance with error handling
    try:
        exchange_class = getattr(ccxt, exchange_id.lower())
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'timeout': 30000,
            'enableRateLimit': True,
        })
        return exchange
    except Exception as e:
        st.error(f"Error creating exchange instance: {e}")
        return None

def get_exchange_status(exchange_instance):
    """Check if an exchange API is working and authenticated
    
    Returns:
        dict with connection status and authentication status
    """
    status = {
        'connected': False,
        'authenticated': False,
        'message': None
    }
    
    if exchange_instance is None:
        status['message'] = "Exchange instance is None"
        return status
    
    try:
        # Test connection by fetching tickers
        exchange_instance.fetch_ticker('BTC/USDT')
        status['connected'] = True
        
        # Test authentication by fetching balance (requires API key)
        try:
            if exchange_instance.apiKey:
                exchange_instance.fetch_balance()
                status['authenticated'] = True
        except Exception as auth_error:
            status['message'] = f"API connection successful but authentication failed: {str(auth_error)}"
            return status
        
        status['message'] = "Connected and authenticated successfully"
        return status
    except Exception as e:
        status['message'] = f"Connection failed: {str(e)}"
        return status

def filter_dataframe(df, column, value, condition='equals'):
    """Filter a dataframe based on a condition
    
    Args:
        df: Pandas DataFrame
        column: Column name to filter on
        value: Value to compare against
        condition: One of 'equals', 'contains', 'greater_than', 'less_than', 'between'
        
    Returns:
        Filtered DataFrame
    """
    if condition == 'equals':
        return df[df[column] == value]
    elif condition == 'contains':
        return df[df[column].astype(str).str.contains(str(value), case=False)]
    elif condition == 'greater_than':
        return df[df[column] > value]
    elif condition == 'less_than':
        return df[df[column] < value]
    elif condition == 'between' and isinstance(value, (list, tuple)) and len(value) == 2:
        return df[(df[column] >= value[0]) & (df[column] <= value[1])]
    else:
        return df
