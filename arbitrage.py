import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import exchange_integration as exchanges
import data_storage as ds

def find_arbitrage_opportunities(exchanges_list, symbol):
    """Find price differences between exchanges for arbitrage opportunities"""
    prices = {}
    
    for exchange_id in exchanges_list:
        ticker = exchanges.get_ticker(exchange_id, symbol)
        if ticker:
            prices[exchange_id] = {
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'last': ticker['last']
            }
    
    opportunities = []
    
    if len(prices) < 2:
        return opportunities
        
    exchange_pairs = [(a, b) for a in prices.keys() for b in prices.keys() if a != b]
    
    for buy_exchange, sell_exchange in exchange_pairs:
        buy_price = prices[buy_exchange]['ask']
        sell_price = prices[sell_exchange]['bid']
        
        if sell_price > buy_price:
            profit_pct = (sell_price - buy_price) / buy_price * 100
            opportunities.append({
                'symbol': symbol,
                'buy_exchange': buy_exchange,
                'sell_exchange': sell_exchange,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit_pct': profit_pct,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return opportunities

def calculate_arbitrage_profit(buy_exchange, sell_exchange, symbol, amount):
    """Calculate potential profit from an arbitrage opportunity"""
    buy_ticker = exchanges.get_ticker(buy_exchange, symbol)
    sell_ticker = exchanges.get_ticker(sell_exchange, symbol)
    
    if not buy_ticker or not sell_ticker:
        return None
    
    buy_price = buy_ticker['ask']
    sell_price = sell_ticker['bid']
    
    # Calculate transaction fees (example: 0.1% fee on each exchange)
    buy_fee = amount * buy_price * 0.001
    sell_fee = amount * sell_price * 0.001
    
    # Calculate profit
    gross_profit = (sell_price - buy_price) * amount
    net_profit = gross_profit - buy_fee - sell_fee
    
    return {
        'symbol': symbol,
        'buy_exchange': buy_exchange,
        'sell_exchange': sell_exchange,
        'amount': amount,
        'buy_price': buy_price,
        'sell_price': sell_price,
        'buy_fee': buy_fee,
        'sell_fee': sell_fee,
        'gross_profit': gross_profit,
        'net_profit': net_profit,
        'profit_pct': (net_profit / (buy_price * amount)) * 100
    }

def execute_arbitrage(buy_exchange, sell_exchange, symbol, amount):
    """Execute an arbitrage opportunity by buying and selling simultaneously"""
    # In a real implementation, this would require careful timing and risk management
    buy_order = exchanges.execute_order(buy_exchange, symbol, 'market', 'buy', amount)
    
    if not buy_order:
        return {
            'success': False,
            'message': 'Failed to execute buy order'
        }
    
    sell_order = exchanges.execute_order(sell_exchange, symbol, 'market', 'sell', amount)
    
    if not sell_order:
        # In a real scenario, we would need to handle the case where we bought but failed to sell
        return {
            'success': False,
            'message': 'Bought successfully but failed to execute sell order'
        }
    
    # Calculate actual profit
    buy_price = buy_order['price']
    sell_price = sell_order['price']
    
    gross_profit = (sell_price - buy_price) * amount
    buy_fee = buy_order.get('fee', {}).get('cost', amount * buy_price * 0.001)
    sell_fee = sell_order.get('fee', {}).get('cost', amount * sell_price * 0.001)
    
    net_profit = gross_profit - buy_fee - sell_fee
    
    return {
        'success': True,
        'buy_order': buy_order,
        'sell_order': sell_order,
        'gross_profit': gross_profit,
        'net_profit': net_profit,
        'profit_pct': (net_profit / (buy_price * amount)) * 100
    }

def render_page():
    st.header("Cryptocurrency Arbitrage")
    
    st.markdown("""
    Arbitrage trading takes advantage of price differences between exchanges. 
    Buy low on one exchange and sell high on another for risk-free profit.
    """)
    
    # Select exchanges for arbitrage
    available_exchanges = ["Binance", "Coinbase", "Kraken", "KuCoin", "Huobi"]
    selected_exchanges = st.multiselect(
        "Select exchanges for arbitrage",
        available_exchanges,
        default=["Binance", "Coinbase"]
    )
    
    if len(selected_exchanges) < 2:
        st.warning("Please select at least two exchanges for arbitrage comparison.")
        return
    
    # Find common symbols across selected exchanges
    st.subheader("Find Arbitrage Opportunities")
    
    # Common symbols selector
    common_symbols = exchanges.get_common_symbols(selected_exchanges)
    
    if not common_symbols:
        st.warning("No common symbols found across the selected exchanges.")
        return
    
    selected_symbol = st.selectbox("Select trading pair", common_symbols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Find Opportunities"):
            with st.spinner("Analyzing price differences..."):
                opportunities = find_arbitrage_opportunities(selected_exchanges, selected_symbol)
                
                if opportunities:
                    # Store opportunities in session state for later access
                    st.session_state.arbitrage_opportunities = opportunities
                    
                    # Display opportunities
                    opportunities_df = pd.DataFrame(opportunities)
                    st.success(f"Found {len(opportunities)} arbitrage opportunities!")
                    st.dataframe(opportunities_df)
                    
                    # Select the best opportunity
                    best_opportunity = max(opportunities, key=lambda x: x['profit_pct'])
                    st.subheader("Best Opportunity")
                    
                    st.markdown(f"""
                    - **Symbol**: {best_opportunity['symbol']}
                    - **Buy from**: {best_opportunity['buy_exchange']} at {best_opportunity['buy_price']}
                    - **Sell to**: {best_opportunity['sell_exchange']} at {best_opportunity['sell_price']}
                    - **Profit**: {best_opportunity['profit_pct']:.2f}%
                    """)
                else:
                    st.warning("No arbitrage opportunities found at this time.")
    
    with col2:
        st.subheader("Profit Calculator")
        
        # Inputs for profit calculation
        amount = st.number_input("Trading amount (in base currency)", min_value=0.0, value=1.0)
        
        if amount > 0:
            if 'arbitrage_opportunities' in st.session_state and st.session_state.arbitrage_opportunities:
                opportunities = st.session_state.arbitrage_opportunities
                best_opportunity = max(opportunities, key=lambda x: x['profit_pct'])
                
                buy_exchange = best_opportunity['buy_exchange']
                sell_exchange = best_opportunity['sell_exchange']
                symbol = best_opportunity['symbol']
                
                profit_details = calculate_arbitrage_profit(buy_exchange, sell_exchange, symbol, amount)
                
                if profit_details:
                    st.info(f"Estimated profit for trading {amount} {symbol}: ${profit_details['net_profit']:.2f} ({profit_details['profit_pct']:.2f}%)")
                    
                    # Add arbitrage execution button (would require real API keys)
                    if st.button("Execute Arbitrage Trade"):
                        st.warning("This is a simulated execution. In a real environment, this would execute actual trades.")
                        
                        with st.spinner("Executing arbitrage trade..."):
                            # Simulate execution delay
                            import time
                            time.sleep(2)
                            
                            # In a real implementation, this would execute actual trades
                            # For this demo, we'll simulate a successful trade
                            result = {
                                'success': True,
                                'buy_order': {'price': profit_details['buy_price']},
                                'sell_order': {'price': profit_details['sell_price']},
                                'gross_profit': profit_details['gross_profit'],
                                'net_profit': profit_details['net_profit'],
                                'profit_pct': profit_details['profit_pct']
                            }
                            
                            if result['success']:
                                st.success(f"Arbitrage executed successfully! Net profit: ${result['net_profit']:.2f}")
                                
                                # Record transaction in history
                                transaction = {
                                    'type': 'Arbitrage',
                                    'symbol': symbol,
                                    'buy_exchange': buy_exchange,
                                    'sell_exchange': sell_exchange,
                                    'amount': amount,
                                    'profit': result['net_profit'],
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                ds.add_transaction(transaction)
                            else:
                                st.error(f"Failed to execute arbitrage: {result.get('message', 'Unknown error')}")
    
    # Historical arbitrage opportunities
    st.subheader("Historical Price Differences")
    
    # Placeholder for historical arbitrage chart
    # In a real application, this would show historical price differences
    # Here we'll create some sample data for visualization
    
    # Generate random historical data for demonstration
    timestamps = pd.date_range(start='2023-01-01', periods=30, freq='D')
    exchange_data = {}
    
    for exchange in selected_exchanges:
        base_price = np.random.uniform(10000, 30000)
        # Generate slightly different prices for each exchange
        prices = [base_price + np.random.normal(0, base_price * 0.01) for _ in range(len(timestamps))]
        exchange_data[exchange] = prices
    
    # Create dataframe for visualization
    historical_data = pd.DataFrame({
        'Date': timestamps
    })
    
    for exchange, prices in exchange_data.items():
        historical_data[exchange] = prices
    
    # Melt the dataframe for easier plotting
    melted_data = pd.melt(
        historical_data, 
        id_vars=['Date'], 
        value_vars=selected_exchanges,
        var_name='Exchange',
        value_name='Price'
    )
    
    # Plot historical prices
    fig = px.line(
        melted_data, 
        x='Date', 
        y='Price', 
        color='Exchange',
        title=f'Historical Prices for {selected_symbol}',
        labels={'Price': 'Price (USD)', 'Date': 'Date'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Arbitrage tips
    st.subheader("Arbitrage Tips")
    
    st.markdown("""
    ### Best Practices for Arbitrage Trading
    
    - **Account for Fees**: Always include exchange fees in your profit calculations.
    - **Transfer Times**: Remember that moving funds between exchanges takes time, which can affect profitability.
    - **Market Depth**: Check order book depth to ensure your trade won't significantly affect the price.
    - **Risk Management**: Start with smaller amounts to test your strategy.
    - **Automate Wisely**: Use automated trading with caution and proper testing.
    """)
