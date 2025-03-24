import streamlit as st
import ccxt
import pandas as pd
import os
from datetime import datetime
import time
import load_env

# Get status of supported exchanges
def get_exchange_status():
    """Return the connection status of each exchange"""
    return {
        "Binance": True,
        "Bybit": True,
        "Kraken": True,
        "KuCoin": True,
        "MEXC": False,
        "Gate.io": True,
        "Bitget": False
    }

def get_exchange_instance(exchange_id):
    """
    Create an exchange instance based on exchange ID
    Uses API keys from environment variables via load_env module
    """
    try:
        exchange_class = getattr(ccxt, exchange_id.lower())
        credentials = load_env.get_exchange_credentials(exchange_id)
        
        exchange = exchange_class({
            'apiKey': credentials['api_key'],
            'secret': credentials['api_secret'],
            'timeout': 30000,
            'enableRateLimit': True,
        })
        return exchange
    except Exception as e:
        st.error(f"Error creating exchange instance: {e}")
        return None

def get_ticker(exchange_id, symbol):
    """Get ticker information for a specific symbol from an exchange"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            ticker = exchange.fetch_ticker(symbol)
            return ticker
        return None
    except Exception as e:
        st.error(f"Error fetching ticker: {e}")
        return None

def get_orderbook(exchange_id, symbol, limit=20):
    """Get order book for a specific symbol from an exchange"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            orderbook = exchange.fetch_order_book(symbol, limit)
            return orderbook
        return None
    except Exception as e:
        st.error(f"Error fetching orderbook: {e}")
        return None

def get_balances(exchange_id):
    """Get account balances from an exchange"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            balance = exchange.fetch_balance()
            return balance
        return None
    except Exception as e:
        st.error(f"Error fetching balances: {e}")
        return None

def get_markets(exchange_id):
    """Get available markets from an exchange"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            markets = exchange.fetch_markets()
            return markets
        return None
    except Exception as e:
        st.error(f"Error fetching markets: {e}")
        return None

def get_historical_data(exchange_id, symbol, timeframe='1d', limit=100):
    """Get historical OHLCV data for a specific symbol"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        return None
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return None

def execute_order(exchange_id, symbol, order_type, side, amount, price=None):
    """Execute a trade order on a specific exchange"""
    try:
        exchange = get_exchange_instance(exchange_id)
        if exchange:
            if order_type == 'market':
                order = exchange.create_market_order(symbol, side, amount)
            elif order_type == 'limit':
                order = exchange.create_limit_order(symbol, side, amount, price)
            return order
        return None
    except Exception as e:
        st.error(f"Error executing order: {e}")
        return None

def get_common_symbols(exchanges):
    """Find symbols available on all specified exchanges"""
    common_symbols = set()
    first = True
    
    for exchange_id in exchanges:
        exchange = get_exchange_instance(exchange_id)
        if not exchange:
            continue
            
        markets = exchange.fetch_markets()
        symbols = set(market['symbol'] for market in markets)
        
        if first:
            common_symbols = symbols
            first = False
        else:
            common_symbols = common_symbols.intersection(symbols)
    
    return sorted(list(common_symbols))
