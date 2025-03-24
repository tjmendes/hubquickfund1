import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import data_storage as ds
import utils

def get_futures_contracts():
    """Get available CME futures contracts"""
    # In a real implementation, this would fetch from CME Group API
    return [
        {
            'symbol': 'BTC',
            'name': 'Bitcoin Futures',
            'month': 'SEP2023',
            'price': 30150.50,
            'change': +1.2,
            'open_interest': 4820,
            'volume': 12450,
            'expiry': '2023-09-29'
        },
        {
            'symbol': 'BTC',
            'name': 'Bitcoin Futures',
            'month': 'DEC2023',
            'price': 30350.25,
            'change': +1.5,
            'open_interest': 2150,
            'volume': 5230,
            'expiry': '2023-12-29'
        },
        {
            'symbol': 'ETH',
            'name': 'Ether Futures',
            'month': 'SEP2023',
            'price': 1850.75,
            'change': -0.8,
            'open_interest': 3540,
            'volume': 9870,
            'expiry': '2023-09-29'
        },
        {
            'symbol': 'ETH',
            'name': 'Ether Futures',
            'month': 'DEC2023',
            'price': 1875.50,
            'change': -0.5,
            'open_interest': 1680,
            'volume': 4320,
            'expiry': '2023-12-29'
        },
        {
            'symbol': 'SOL',
            'name': 'Solana Futures',
            'month': 'SEP2023',
            'price': 24.85,
            'change': +2.3,
            'open_interest': 1240,
            'volume': 3560,
            'expiry': '2023-09-29'
        },
        {
            'symbol': 'ADA',
            'name': 'Cardano Futures',
            'month': 'SEP2023',
            'price': 0.32,
            'change': +1.8,
            'open_interest': 980,
            'volume': 2870,
            'expiry': '2023-09-29'
        },
        {
            'symbol': 'DOT',
            'name': 'Polkadot Futures',
            'month': 'SEP2023',
            'price': 5.15,
            'change': -1.2,
            'open_interest': 720,
            'volume': 1950,
            'expiry': '2023-09-29'
        },
        {
            'symbol': 'AVAX',
            'name': 'Avalanche Futures',
            'month': 'SEP2023',
            'price': 13.45,
            'change': +3.1,
            'open_interest': 580,
            'volume': 1680,
            'expiry': '2023-09-29'
        }
    ]

def get_user_positions():
    """Get user's current futures positions"""
    # In a real implementation, this would fetch from user's account
    return [
        {
            'symbol': 'BTC',
            'month': 'SEP2023',
            'position': 'Long',
            'quantity': 2,
            'entry_price': 29850.25,
            'current_price': 30150.50,
            'pnl': 600.50,
            'pnl_percent': 1.01,
            'margin': 5970.05,
            'liquidation_price': 28357.74
        },
        {
            'symbol': 'ETH',
            'month': 'SEP2023',
            'position': 'Short',
            'quantity': 5,
            'entry_price': 1880.50,
            'current_price': 1850.75,
            'pnl': 148.75,
            'pnl_percent': 1.58,
            'margin': 1880.50,
            'liquidation_price': 1974.53
        }
    ]

def get_historical_prices(symbol, start_date=None, end_date=None):
    """Get historical price data for futures contracts"""
    # In a real implementation, this would fetch from CME API
    
    # Default date range if not provided
    if not start_date:
        start_date = datetime.now() - timedelta(days=90)
    if not end_date:
        end_date = datetime.now()
    
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Base price and volatility for different assets
    base_prices = {
        'BTC': 30000,
        'ETH': 1800,
        'SOL': 25,
        'ADA': 0.3,
        'DOT': 5,
        'AVAX': 13
    }
    
    volatilities = {
        'BTC': 0.03,
        'ETH': 0.04,
        'SOL': 0.06,
        'ADA': 0.05,
        'DOT': 0.04,
        'AVAX': 0.07
    }
    
    base_price = base_prices.get(symbol, 100)
    volatility = volatilities.get(symbol, 0.05)
    
    # Generate price data with realistic movements
    np.random.seed(42)  # For reproducibility
    returns = np.random.normal(0, volatility, len(date_range))
    price_changes = np.cumprod(1 + returns)
    prices = base_price * price_changes
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'open': prices * (1 + np.random.normal(0, 0.005, len(date_range))),
        'high': prices * (1 + np.random.normal(0.005, 0.005, len(date_range))),
        'low': prices * (1 - np.random.normal(0.005, 0.005, len(date_range))),
        'close': prices,
        'volume': np.random.lognormal(10, 1, len(date_range))
    })
    
    return df

def calculate_margin_requirements(symbol, quantity, price, leverage=20):
    """Calculate margin requirements for a futures position"""
    contract_sizes = {
        'BTC': 5,  # 5 BTC per contract
        'ETH': 50,  # 50 ETH per contract
        'SOL': 500,  # 500 SOL per contract
        'ADA': 10000,  # 10000 ADA per contract
        'DOT': 1000,  # 1000 DOT per contract
        'AVAX': 500   # 500 AVAX per contract
    }
    
    contract_size = contract_sizes.get(symbol, 1)
    notional_value = quantity * price * contract_size
    required_margin = notional_value / leverage
    
    maintenance_margin = required_margin * 0.5
    liquidation_price_long = price * (1 - 1/leverage)
    liquidation_price_short = price * (1 + 1/leverage)
    
    return {
        'notional_value': notional_value,
        'required_margin': required_margin,
        'maintenance_margin': maintenance_margin,
        'liquidation_price_long': liquidation_price_long,
        'liquidation_price_short': liquidation_price_short,
        'max_leverage': leverage
    }

def execute_futures_trade(symbol, month, position_type, quantity, price):
    """Execute a futures trade (simulated)"""
    # In a real implementation, this would submit an order to the CME API
    
    # Calculate trade details
    trade_value = price * quantity
    fees = trade_value * 0.0004  # 0.04% fee
    
    # Create trade record
    trade = {
        'symbol': symbol,
        'month': month,
        'position_type': position_type,
        'quantity': quantity,
        'price': price,
        'trade_value': trade_value,
        'fees': fees,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'Executed'
    }
    
    # In a real implementation, this would return the actual trade confirmation from the exchange
    return trade

def render_page():
    st.header("CME Futures Trading")
    
    st.markdown("""
    Access and trade cryptocurrency futures contracts on the CME Group exchange.
    Monitor your positions, analyze market data, and execute trades with advanced order types.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Market Overview", "My Positions", "Trade"])
    
    with tab1:
        st.subheader("Available Futures Contracts")
        
        # Get futures contracts
        contracts = get_futures_contracts()
        
        # Convert to DataFrame
        contracts_df = pd.DataFrame(contracts)
        
        # Format for display
        display_df = contracts_df.copy()
        display_df['price'] = display_df['price'].apply(lambda x: f"${x:,.2f}")
        display_df['change'] = display_df['change'].apply(lambda x: f"{x:+.2f}%")
        display_df['open_interest'] = display_df['open_interest'].apply(lambda x: f"{x:,}")
        display_df['volume'] = display_df['volume'].apply(lambda x: f"{x:,}")
        
        # Group by symbol for better organization
        symbols = sorted(list(set(contracts_df['symbol'])))
        
        for symbol in symbols:
            st.subheader(f"{symbol} Futures")
            symbol_contracts = display_df[display_df['symbol'] == symbol]
            st.dataframe(symbol_contracts, use_container_width=True)
        
        # Price comparison chart
        st.subheader("Futures Contracts Price Comparison")
        
        # Create comparison chart
        fig = px.bar(
            contracts_df,
            x='symbol',
            y='price',
            color='month',
            barmode='group',
            labels={'price': 'Price (USD)', 'symbol': 'Asset', 'month': 'Contract Month'},
            title='Futures Contract Prices by Asset and Month'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume and open interest
        st.subheader("Trading Activity")
        
        # Create activity chart
        fig2 = px.scatter(
            contracts_df,
            x='open_interest',
            y='volume',
            size='price',
            color='symbol',
            hover_name='month',
            log_x=True,
            log_y=True,
            labels={
                'open_interest': 'Open Interest (log scale)',
                'volume': 'Volume (log scale)',
                'symbol': 'Asset'
            },
            title='Trading Activity by Contract'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Historical price chart
        st.subheader("Historical Price Charts")
        
        # Select asset for historical data
        selected_symbol = st.selectbox("Select Asset", symbols)
        
        # Get historical data
        history = get_historical_prices(selected_symbol)
        
        # Create candlestick chart
        fig3 = go.Figure(data=[go.Candlestick(
            x=history['date'],
            open=history['open'],
            high=history['high'],
            low=history['low'],
            close=history['close'],
            name=selected_symbol
        )])
        
        fig3.update_layout(
            title=f'{selected_symbol} Futures Price History',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # Volume chart
        fig4 = px.bar(
            history,
            x='date',
            y='volume',
            title=f'{selected_symbol} Trading Volume',
            labels={'volume': 'Volume', 'date': 'Date'}
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab2:
        st.subheader("My Futures Positions")
        
        # Get user positions
        positions = get_user_positions()
        
        if not positions:
            st.info("You don't have any open futures positions. Use the Trade tab to open positions.")
        else:
            # Summary metrics
            total_margin = sum(position['margin'] for position in positions)
            total_pnl = sum(position['pnl'] for position in positions)
            pnl_percent = (total_pnl / total_margin) * 100 if total_margin > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Positions", len(positions))
            
            with col2:
                st.metric("Total Margin", f"${total_margin:,.2f}")
            
            with col3:
                st.metric("Total PnL", f"${total_pnl:,.2f}", f"{pnl_percent:+.2f}%")
            
            # Display positions table
            positions_df = pd.DataFrame(positions)
            
            # Format for display
            display_df = positions_df.copy()
            display_df['entry_price'] = display_df['entry_price'].apply(lambda x: f"${x:,.2f}")
            display_df['current_price'] = display_df['current_price'].apply(lambda x: f"${x:,.2f}")
            display_df['pnl'] = display_df['pnl'].apply(lambda x: f"${x:,.2f}")
            display_df['pnl_percent'] = display_df['pnl_percent'].apply(lambda x: f"{x:+.2f}%")
            display_df['margin'] = display_df['margin'].apply(lambda x: f"${x:,.2f}")
            display_df['liquidation_price'] = display_df['liquidation_price'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Position details and management
            st.subheader("Position Management")
            
            # Select position to manage
            position_options = [f"{p['symbol']} {p['month']} ({p['position']} {p['quantity']})" for p in positions]
            selected_position_idx = st.selectbox("Select Position", range(len(position_options)), format_func=lambda x: position_options[x])
            
            if selected_position_idx is not None:
                position = positions[selected_position_idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Asset:** {position['symbol']} {position['month']}")
                    st.markdown(f"**Position:** {position['position']} {position['quantity']}")
                    st.markdown(f"**Entry Price:** ${position['entry_price']:,.2f}")
                    st.markdown(f"**Current Price:** ${position['current_price']:,.2f}")
                
                with col2:
                    st.markdown(f"**PnL:** ${position['pnl']:,.2f} ({position['pnl_percent']:+.2f}%)")
                    st.markdown(f"**Margin:** ${position['margin']:,.2f}")
                    st.markdown(f"**Liquidation Price:** ${position['liquidation_price']:,.2f}")
                    
                    # Calculate distance to liquidation
                    if position['position'] == 'Long':
                        liquidation_distance = ((position['current_price'] - position['liquidation_price']) / position['current_price']) * 100
                    else:
                        liquidation_distance = ((position['liquidation_price'] - position['current_price']) / position['current_price']) * 100
                    
                    st.markdown(f"**Distance to Liquidation:** {liquidation_distance:.2f}%")
                
                # Position management options
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Close Position", key=f"close_{position['symbol']}_{position['month']}"):
                        st.success(f"Position closed at market price: ${position['current_price']:,.2f}")
                
                with col2:
                    # Add stop loss
                    stop_price = st.number_input(
                        "Stop Loss Price",
                        min_value=0.0,
                        value=position['liquidation_price'] * 1.05 if position['position'] == 'Long' else position['liquidation_price'] * 0.95,
                        step=0.01,
                        key=f"stop_{position['symbol']}_{position['month']}"
                    )
                    
                    if st.button("Set Stop Loss"):
                        st.success(f"Stop loss set at ${stop_price:,.2f}")
                
                with col3:
                    # Add take profit
                    take_profit = st.number_input(
                        "Take Profit Price",
                        min_value=0.0,
                        value=position['entry_price'] * 1.1 if position['position'] == 'Long' else position['entry_price'] * 0.9,
                        step=0.01,
                        key=f"tp_{position['symbol']}_{position['month']}"
                    )
                    
                    if st.button("Set Take Profit"):
                        st.success(f"Take profit set at ${take_profit:,.2f}")
                
                # Position chart
                st.subheader(f"{position['symbol']} {position['month']} Price Chart")
                
                # Get historical data
                history = get_historical_prices(position['symbol'])
                
                # Create candlestick chart with position markers
                fig = go.Figure(data=[go.Candlestick(
                    x=history['date'],
                    open=history['open'],
                    high=history['high'],
                    low=history['low'],
                    close=history['close'],
                    name=position['symbol']
                )])
                
                # Add entry price line
                fig.add_shape(
                    type="line",
                    x0=history['date'].min(),
                    y0=position['entry_price'],
                    x1=history['date'].max(),
                    y1=position['entry_price'],
                    line=dict(
                        color="blue",
                        width=2,
                        dash="dash",
                    ),
                    name="Entry Price"
                )
                
                # Add liquidation price line
                fig.add_shape(
                    type="line",
                    x0=history['date'].min(),
                    y0=position['liquidation_price'],
                    x1=history['date'].max(),
                    y1=position['liquidation_price'],
                    line=dict(
                        color="red",
                        width=2,
                        dash="dash",
                    ),
                    name="Liquidation Price"
                )
                
                # Add annotations
                fig.add_annotation(
                    x=history['date'].max(),
                    y=position['entry_price'],
                    text="Entry",
                    showarrow=True,
                    arrowhead=1
                )
                
                fig.add_annotation(
                    x=history['date'].max(),
                    y=position['liquidation_price'],
                    text="Liquidation",
                    showarrow=True,
                    arrowhead=1
                )
                
                fig.update_layout(
                    title=f'{position["symbol"]} {position["month"]} Price with Position',
                    xaxis_title='Date',
                    yaxis_title='Price (USD)',
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Open New Position")
        
        # Get available contracts
        contracts = get_futures_contracts()
        
        # Create selection options
        symbols = sorted(list(set(c['symbol'] for c in contracts)))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Select asset
            selected_symbol = st.selectbox("Select Asset", symbols, key="trade_symbol")
            
            # Filter months for selected asset
            months = [c['month'] for c in contracts if c['symbol'] == selected_symbol]
            selected_month = st.selectbox("Select Contract Month", months, key="trade_month")
            
            # Get selected contract details
            selected_contract = next((c for c in contracts if c['symbol'] == selected_symbol and c['month'] == selected_month), None)
            
            if selected_contract:
                st.info(f"Current Price: ${selected_contract['price']:,.2f} | Change: {selected_contract['change']:+.2f}%")
        
        with col2:
            # Position type
            position_type = st.radio("Position Type", ["Long", "Short"], horizontal=True)
            
            # Quantity
            quantity = st.number_input("Quantity (Contracts)", min_value=1, value=1, step=1)
            
            # Leverage
            leverage = st.slider("Leverage", min_value=1, max_value=20, value=10, step=1)
        
        # Calculate margin and order details
        if selected_contract:
            # Calculate margin requirements
            margin_details = calculate_margin_requirements(
                selected_symbol,
                quantity,
                selected_contract['price'],
                leverage
            )
            
            # Display order summary
            st.subheader("Order Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Asset:** {selected_symbol} {selected_month}")
                st.markdown(f"**Position:** {position_type}")
                st.markdown(f"**Quantity:** {quantity} contracts")
                st.markdown(f"**Price:** ${selected_contract['price']:,.2f}")
                st.markdown(f"**Notional Value:** ${margin_details['notional_value']:,.2f}")
            
            with col2:
                st.markdown(f"**Leverage:** {leverage}x")
                st.markdown(f"**Required Margin:** ${margin_details['required_margin']:,.2f}")
                st.markdown(f"**Maintenance Margin:** ${margin_details['maintenance_margin']:,.2f}")
                
                # Liquidation price based on position type
                if position_type == "Long":
                    liquidation_price = margin_details['liquidation_price_long']
                else:
                    liquidation_price = margin_details['liquidation_price_short']
                
                st.markdown(f"**Liquidation Price:** ${liquidation_price:,.2f}")
                
                # Calculate distance to liquidation
                if position_type == "Long":
                    liquidation_distance = ((selected_contract['price'] - liquidation_price) / selected_contract['price']) * 100
                else:
                    liquidation_distance = ((liquidation_price - selected_contract['price']) / selected_contract['price']) * 100
                
                st.markdown(f"**Distance to Liquidation:** {liquidation_distance:.2f}%")
            
            # Advanced order options
            with st.expander("Advanced Order Options"):
                order_type = st.radio("Order Type", ["Market", "Limit", "Stop", "Stop Limit"], horizontal=True)
                
                if order_type in ["Limit", "Stop Limit"]:
                    limit_price = st.number_input(
                        "Limit Price",
                        min_value=0.01,
                        value=selected_contract['price'],
                        step=0.01
                    )
                
                if order_type in ["Stop", "Stop Limit"]:
                    stop_price = st.number_input(
                        "Stop Price",
                        min_value=0.01,
                        value=selected_contract['price'] * 0.99 if position_type == "Long" else selected_contract['price'] * 1.01,
                        step=0.01
                    )
                
                # Time in force
                time_in_force = st.radio("Time in Force", ["Day", "GTC (Good Till Cancel)", "IOC (Immediate or Cancel)"], horizontal=True)
                
                # Post only
                post_only = st.checkbox("Post Only")
                
                # Reduce only
                reduce_only = st.checkbox("Reduce Only")
            
            # Submit order button
            if st.button("Place Order"):
                # In a real implementation, this would submit the order to the CME API
                # For this demo, we'll simulate a successful order execution
                trade_result = execute_futures_trade(
                    selected_symbol,
                    selected_month,
                    position_type,
                    quantity,
                    selected_contract['price']
                )
                
                if trade_result:
                    st.success(f"""
                    Trade executed successfully!
                    - {position_type} {quantity} {selected_symbol} {selected_month} @ ${selected_contract['price']:,.2f}
                    - Margin: ${margin_details['required_margin']:,.2f}
                    - Fees: ${trade_result['fees']:,.2f}
                    """)
                    
                    # Add to transaction history
                    transaction = {
                        'type': 'Futures',
                        'symbol': selected_symbol,
                        'contract': selected_month,
                        'action': position_type,
                        'quantity': quantity,
                        'price': selected_contract['price'],
                        'value': trade_result['trade_value'],
                        'fees': trade_result['fees'],
                        'timestamp': trade_result['timestamp']
                    }
                    
                    ds.add_transaction(transaction)
                    
                    # Display margin warning if close to liquidation
                    if liquidation_distance < 10:
                        st.warning(f"""
                        Warning: Your position is within 10% of the liquidation price.
                        Consider reducing leverage or adding more margin to avoid liquidation risk.
                        """)
                else:
                    st.error("Trade execution failed. Please try again.")
        
        # Risk management tips
        st.markdown("---")
        st.subheader("Risk Management Tips")
        
        st.markdown("""
        ### Best Practices for Futures Trading
        
        - **Start Small**: Begin with a small portion of your portfolio in futures.
        - **Use Reasonable Leverage**: Higher leverage means higher risk of liquidation.
        - **Set Stop Losses**: Always protect your position with stop losses.
        - **Monitor Funding Rates**: For perpetual futures, funding rates can significantly impact profitability.
        - **Watch Liquidation Price**: Keep your position well away from the liquidation price.
        - **Consider Hedging**: Use futures to hedge your spot portfolio against market downturns.
        """)
