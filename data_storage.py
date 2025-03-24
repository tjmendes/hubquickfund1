import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def initialize_user_data():
    """Initialize or retrieve user data from session state"""
    # Create basic user data structure if not already in session state
    user_data = {
        'portfolio': create_mock_portfolio(),
        'transactions': create_mock_transactions(),
        'opportunities': create_mock_opportunities(),
        'activity': create_mock_activity(),
        'notifications': create_mock_notifications()
    }
    
    return user_data

def create_mock_portfolio():
    """Create sample portfolio data for demonstration"""
    return [
        {'asset': 'Bitcoin (BTC)', 'amount': 0.5, 'value': 15000.00},
        {'asset': 'Ethereum (ETH)', 'amount': 5.0, 'value': 15000.00},
        {'asset': 'Solana (SOL)', 'amount': 100.0, 'value': 3500.00},
        {'asset': 'Cardano (ADA)', 'amount': 5000.0, 'value': 2000.00},
        {'asset': 'USD Coin (USDC)', 'amount': 10000.0, 'value': 10000.00},
        {'asset': 'Yield Farm LP Tokens', 'amount': 250.0, 'value': 4000.00},
        {'asset': 'Staked ETH', 'amount': 2.0, 'value': 6000.00}
    ]

def create_mock_transactions():
    """Create sample transactions for demonstration"""
    current_date = datetime.now()
    return [
        {
            'type': 'Arbitrage',
            'symbol': 'ETH/USDT',
            'buy_exchange': 'Binance',
            'sell_exchange': 'Coinbase',
            'amount': 1.0,
            'profit': 12.50,
            'timestamp': (current_date - timedelta(days=1, hours=6)).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'type': 'Staking',
            'asset': 'Ethereum (ETH)',
            'network': 'Lido',
            'amount': 0.1,
            'reward': 0.001,
            'timestamp': (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'type': 'Yield Farming',
            'protocol': 'Aave',
            'pool': 'USDC/USDT',
            'amount': 500.0,
            'reward': 0.35,
            'timestamp': (current_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'type': 'Mining',
            'coin': 'Bitcoin (BTC)',
            'hashrate': '10 TH/s',
            'amount': 0.00025,
            'value': 7.50,
            'timestamp': (current_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'type': 'Airdrop',
            'project': 'DeFi Lender',
            'token': 'LEND',
            'amount': 500,
            'value': 250.0,
            'timestamp': (current_date - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

def create_mock_opportunities():
    """Create sample profit opportunities for demonstration"""
    return [
        {
            'type': 'Arbitrage',
            'symbol': 'BTC/USDT',
            'buy_exchange': 'Kraken',
            'sell_exchange': 'Binance',
            'price_difference': 0.25,
            'potential_profit': '$25 per BTC',
            'risk_level': 'Low'
        },
        {
            'type': 'Yield Farming',
            'protocol': 'Compound',
            'pool': 'ETH/USDC',
            'apy': 6.2,
            'min_deposit': '$100',
            'risk_level': 'Low'
        },
        {
            'type': 'Staking',
            'asset': 'Solana (SOL)',
            'network': 'Solana',
            'apy': 7.5,
            'min_stake': '1 SOL',
            'risk_level': 'Medium'
        },
        {
            'type': 'Mining',
            'coin': 'Ethereum (ETH)',
            'profit_per_day': '$3.10 per 100 MH/s',
            'min_purchase': '10 MH/s',
            'risk_level': 'Medium'
        },
        {
            'type': 'Airdrop',
            'project': 'ZK Layer 2',
            'token': 'ZKL',
            'estimated_value': 'High',
            'deadline': '2023-07-25',
            'difficulty': 'Medium'
        }
    ]

def create_mock_activity():
    """Create sample activity data for chart visualization"""
    # Create date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create different activity types with realistic trends
    arbitrage_values = 10 + 5 * np.sin(np.linspace(0, 6, len(dates))) + np.random.normal(0, 1, len(dates))
    staking_values = 15 + np.random.normal(0, 0.5, len(dates)) + np.linspace(0, 5, len(dates))
    farming_values = 20 + 2 * np.sin(np.linspace(0, 8, len(dates))) + np.random.normal(0, 1.5, len(dates))
    mining_values = 12 + np.random.normal(0, 1, len(dates)) - np.linspace(0, 2, len(dates))
    
    # Ensure all values are positive
    arbitrage_values = np.maximum(arbitrage_values, 0)
    staking_values = np.maximum(staking_values, 0)
    farming_values = np.maximum(farming_values, 0)
    mining_values = np.maximum(mining_values, 0)
    
    # Create activity data
    activity_data = []
    
    for i, date in enumerate(dates):
        activity_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'value': arbitrage_values[i],
            'category': 'Arbitrage'
        })
        
        activity_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'value': staking_values[i],
            'category': 'Staking'
        })
        
        activity_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'value': farming_values[i],
            'category': 'Yield Farming'
        })
        
        activity_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'value': mining_values[i],
            'category': 'Mining'
        })
    
    return activity_data

def create_mock_notifications():
    """Create sample notifications for demonstration"""
    current_date = datetime.now()
    return [
        {
            'title': 'Arbitrage Opportunity',
            'message': 'BTC price difference of 0.5% between Binance and Kraken',
            'date': current_date.strftime("%Y-%m-%d %H:%M"),
            'read': False,
            'category': 'Arbitrage'
        },
        {
            'title': 'Staking Reward',
            'message': 'Received 0.01 ETH from Lido staking',
            'date': (current_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            'read': True,
            'category': 'Staking'
        },
        {
            'title': 'New Yield Farm',
            'message': 'Balancer launched a new farm with 12.7% APY',
            'date': (current_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
            'read': False,
            'category': 'Yield Farming'
        },
        {
            'title': 'Airdrop Alert',
            'message': 'ZK Layer 2 airdrop qualification ends in 3 days',
            'date': (current_date - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
            'read': False,
            'category': 'Airdrop'
        },
        {
            'title': 'Mining Profit Increase',
            'message': 'BTC mining profitability increased by 5% today',
            'date': (current_date - timedelta(days=4)).strftime("%Y-%m-%d %H:%M"),
            'read': True,
            'category': 'Mining'
        }
    ]

def get_portfolio_data():
    """Get user's portfolio data"""
    if 'user_data' in st.session_state:
        return st.session_state.user_data['portfolio']
    else:
        return create_mock_portfolio()

def get_profit_opportunities():
    """Get current profit opportunities"""
    if 'user_data' in st.session_state:
        return st.session_state.user_data['opportunities']
    else:
        return create_mock_opportunities()

def get_activity_data():
    """Get user's activity data for charts"""
    if 'user_data' in st.session_state:
        return st.session_state.user_data['activity']
    else:
        return create_mock_activity()

def get_recent_transactions():
    """Get user's recent transactions"""
    if 'user_data' in st.session_state:
        return st.session_state.user_data['transactions']
    else:
        return create_mock_transactions()

def get_notifications():
    """Get user's notifications"""
    if 'user_data' in st.session_state:
        return st.session_state.user_data['notifications']
    else:
        return create_mock_notifications()

def add_transaction(transaction):
    """Add a new transaction to the user's history"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = initialize_user_data()
    
    # Add timestamp if not provided
    if 'timestamp' not in transaction:
        transaction['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add the transaction to the top of the list
    st.session_state.user_data['transactions'].insert(0, transaction)
    
    # Limit to the most recent 100 transactions
    if len(st.session_state.user_data['transactions']) > 100:
        st.session_state.user_data['transactions'] = st.session_state.user_data['transactions'][:100]
    
    return True

def add_notification(notification):
    """Add a new notification"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = initialize_user_data()
    
    # Add date if not provided
    if 'date' not in notification:
        notification['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Set as unread by default
    if 'read' not in notification:
        notification['read'] = False
    
    # Add the notification to the top of the list
    st.session_state.user_data['notifications'].insert(0, notification)
    
    # Limit to the most recent 50 notifications
    if len(st.session_state.user_data['notifications']) > 50:
        st.session_state.user_data['notifications'] = st.session_state.user_data['notifications'][:50]
    
    return True

def update_portfolio(asset, amount, value, operation='add'):
    """Update user's portfolio with a new asset or modify existing one"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = initialize_user_data()
    
    portfolio = st.session_state.user_data['portfolio']
    
    # Check if asset already exists
    existing_asset = next((item for item in portfolio if item['asset'] == asset), None)
    
    if existing_asset:
        if operation == 'add':
            existing_asset['amount'] += amount
            existing_asset['value'] += value
        elif operation == 'subtract':
            existing_asset['amount'] -= amount
            existing_asset['value'] -= value
            # Remove asset if amount becomes zero or negative
            if existing_asset['amount'] <= 0:
                portfolio.remove(existing_asset)
        elif operation == 'set':
            existing_asset['amount'] = amount
            existing_asset['value'] = value
    else:
        # Only add new asset if operation is 'add' or 'set'
        if operation in ['add', 'set'] and amount > 0:
            portfolio.append({
                'asset': asset,
                'amount': amount,
                'value': value
            })
    
    return True

def refresh_user_data():
    """Refresh user data with updated information"""
    # In a real implementation, this would fetch fresh data from APIs
    # For this demo, we'll just update the timestamps and add some random variations
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = initialize_user_data()
    
    # Update portfolio values with small random changes
    for asset in st.session_state.user_data['portfolio']:
        # Random price change between -2% and +2%
        price_change = np.random.uniform(-0.02, 0.02)
        asset['value'] = asset['value'] * (1 + price_change)
    
    # Update opportunities with small variations
    for opportunity in st.session_state.user_data['opportunities']:
        if 'apy' in opportunity:
            # Random APY change between -0.2% and +0.2%
            apy_change = np.random.uniform(-0.2, 0.2)
            opportunity['apy'] = opportunity['apy'] + apy_change
            if opportunity['apy'] < 0:
                opportunity['apy'] = 0.1
    
    # Refresh activity data with updated trends
    st.session_state.user_data['activity'] = create_mock_activity()
    
    # Add a new notification occasionally
    if np.random.random() < 0.3:  # 30% chance of new notification
        notification_types = [
            {
                'title': 'New Arbitrage Opportunity',
                'message': 'ETH price difference of 0.3% between Coinbase and Kraken',
                'category': 'Arbitrage'
            },
            {
                'title': 'Staking Rate Increase',
                'message': 'Cardano staking APY increased to 5.5%',
                'category': 'Staking'
            },
            {
                'title': 'Yield Farm Warning',
                'message': 'Impermanent loss risk in ETH/USDC pool due to volatility',
                'category': 'Yield Farming'
            },
            {
                'title': 'Mining Difficulty Change',
                'message': 'Bitcoin mining difficulty increased by 3.2%',
                'category': 'Mining'
            },
            {
                'title': 'Upcoming Airdrop',
                'message': 'New DeFi protocol announcing token airdrop next week',
                'category': 'Airdrop'
            }
        ]
        
        new_notification = np.random.choice(notification_types)
        add_notification(new_notification)
    
    return True
