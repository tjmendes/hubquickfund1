import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import data_storage as ds

def get_mining_options():
    """Get available cryptocurrency mining options"""
    # In a real implementation, this would fetch from mining services APIs
    return [
        {
            'coin': 'Bitcoin (BTC)',
            'algorithm': 'SHA-256',
            'hashrate': 'TH/s',
            'efficiency': 35,  # W/TH
            'cost_per_unit': 0.05,  # $ per TH/s per day
            'min_purchase': 1,  # TH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.0018  # $ per TH/s per day
        },
        {
            'coin': 'Ethereum (ETH)',
            'algorithm': 'Ethash',
            'hashrate': 'MH/s',
            'efficiency': 0.5,  # W/MH
            'cost_per_unit': 0.08,  # $ per MH/s per day
            'min_purchase': 10,  # MH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.002  # $ per MH/s per day
        },
        {
            'coin': 'Litecoin (LTC)',
            'algorithm': 'Scrypt',
            'hashrate': 'MH/s',
            'efficiency': 1.0,  # W/MH
            'cost_per_unit': 0.04,  # $ per MH/s per day
            'min_purchase': 100,  # MH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.0015  # $ per MH/s per day
        },
        {
            'coin': 'Dogecoin (DOGE)',
            'algorithm': 'Scrypt',
            'hashrate': 'MH/s',
            'efficiency': 1.0,  # W/MH
            'cost_per_unit': 0.035,  # $ per MH/s per day
            'min_purchase': 100,  # MH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.0014  # $ per MH/s per day
        },
        {
            'coin': 'Monero (XMR)',
            'algorithm': 'RandomX',
            'hashrate': 'KH/s',
            'efficiency': 1.2,  # W/KH
            'cost_per_unit': 0.1,  # $ per KH/s per day
            'min_purchase': 1,  # KH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.003  # $ per KH/s per day
        },
        {
            'coin': 'Dash (DASH)',
            'algorithm': 'X11',
            'hashrate': 'GH/s',
            'efficiency': 0.8,  # W/GH
            'cost_per_unit': 0.06,  # $ per GH/s per day
            'min_purchase': 1,  # GH/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.0025  # $ per GH/s per day
        },
        {
            'coin': 'ZCash (ZEC)',
            'algorithm': 'Equihash',
            'hashrate': 'KSol/s',
            'efficiency': 10.0,  # W/KSol
            'cost_per_unit': 0.09,  # $ per KSol/s per day
            'min_purchase': 0.1,  # KSol/s
            'contract_duration': 365,  # days
            'maintenance_fee': 0.0028  # $ per KSol/s per day
        }
    ]

def get_user_mining_contracts():
    """Get user's current mining contracts"""
    # In a real implementation, this would fetch from the user's account
    return [
        {
            'coin': 'Bitcoin (BTC)',
            'hashrate': 10,  # TH/s
            'daily_earnings': 0.00015,  # BTC
            'daily_revenue': 4.50,  # USD
            'daily_cost': 1.98,  # USD
            'daily_profit': 2.52,  # USD
            'contract_start': '2023-01-15',
            'contract_end': '2024-01-15',
            'status': 'Active'
        },
        {
            'coin': 'Ethereum (ETH)',
            'hashrate': 200,  # MH/s
            'daily_earnings': 0.0025,  # ETH
            'daily_revenue': 7.50,  # USD
            'daily_cost': 4.40,  # USD
            'daily_profit': 3.10,  # USD
            'contract_start': '2023-02-10',
            'contract_end': '2024-02-10',
            'status': 'Active'
        },
        {
            'coin': 'Litecoin (LTC)',
            'hashrate': 500,  # MH/s
            'daily_earnings': 0.03,  # LTC
            'daily_revenue': 3.00,  # USD
            'daily_cost': 2.25,  # USD
            'daily_profit': 0.75,  # USD
            'contract_start': '2023-03-05',
            'contract_end': '2024-03-05',
            'status': 'Active'
        }
    ]

def calculate_mining_profitability(coin, hashrate, electricity_cost=0.1):
    """Calculate profitability of mining a specific coin with given hashrate"""
    # Coin price in USD (would be fetched from API in real implementation)
    coin_prices = {
        'Bitcoin (BTC)': 30000,
        'Ethereum (ETH)': 3000,
        'Litecoin (LTC)': 100,
        'Dogecoin (DOGE)': 0.08,
        'Monero (XMR)': 160,
        'Dash (DASH)': 35,
        'ZCash (ZEC)': 28
    }
    
    # Daily rewards per unit (would be calculated based on network difficulty in real implementation)
    rewards_per_unit = {
        'Bitcoin (BTC)': 0.000015,  # BTC per TH/s
        'Ethereum (ETH)': 0.000012,  # ETH per MH/s
        'Litecoin (LTC)': 0.00006,  # LTC per MH/s
        'Dogecoin (DOGE)': 0.08,  # DOGE per MH/s
        'Monero (XMR)': 0.0004,  # XMR per KH/s
        'Dash (DASH)': 0.0001,  # DASH per GH/s
        'ZCash (ZEC)': 0.0003  # ZEC per KSol/s
    }
    
    # Get mining option details
    mining_options = get_mining_options()
    selected_option = next((o for o in mining_options if o['coin'] == coin), None)
    
    if not selected_option:
        return None
    
    # Calculate daily mining rewards
    daily_coin_reward = rewards_per_unit[coin] * hashrate
    daily_usd_reward = daily_coin_reward * coin_prices[coin]
    
    # Calculate costs
    daily_maintenance_fee = selected_option['maintenance_fee'] * hashrate
    power_consumption = selected_option['efficiency'] * hashrate  # Watts
    daily_electricity_cost = (power_consumption / 1000) * 24 * electricity_cost  # kWh * cost per kWh
    total_daily_cost = daily_maintenance_fee + daily_electricity_cost
    
    # Calculate profit
    daily_profit = daily_usd_reward - total_daily_cost
    monthly_profit = daily_profit * 30
    annual_profit = daily_profit * 365
    
    # ROI calculation
    contract_cost = selected_option['cost_per_unit'] * hashrate * selected_option['contract_duration']
    roi_days = contract_cost / daily_profit if daily_profit > 0 else float('inf')
    
    return {
        'coin': coin,
        'hashrate': hashrate,
        'hashrate_unit': selected_option['hashrate'],
        'daily_coin_reward': daily_coin_reward,
        'daily_usd_reward': daily_usd_reward,
        'daily_maintenance_fee': daily_maintenance_fee,
        'daily_electricity_cost': daily_electricity_cost,
        'total_daily_cost': total_daily_cost,
        'daily_profit': daily_profit,
        'monthly_profit': monthly_profit,
        'annual_profit': annual_profit,
        'contract_cost': contract_cost,
        'roi_days': roi_days
    }

def project_mining_earnings(coin, hashrate, days):
    """Project mining earnings over a period of time"""
    # Calculate base profitability
    profitability = calculate_mining_profitability(coin, hashrate)
    
    if not profitability:
        return None
    
    # Initialize arrays for values
    dates = [datetime.now() + timedelta(days=i) for i in range(days)]
    
    # For simplicity, we'll assume difficulty increases and rewards decrease over time
    # This is a simplification - in reality, difficulty adjustments are more complex
    difficulty_factor = np.linspace(1.0, 1.5, days)  # Gradual difficulty increase
    
    # Calculate daily values with difficulty adjustment
    daily_rewards = [profitability['daily_coin_reward'] / difficulty_factor[i] for i in range(days)]
    daily_usd_rewards = [daily_rewards[i] * (profitability['daily_usd_reward'] / profitability['daily_coin_reward']) for i in range(days)]
    daily_costs = [profitability['total_daily_cost'] for _ in range(days)]
    daily_profits = [daily_usd_rewards[i] - daily_costs[i] for i in range(days)]
    
    # Calculate cumulative values
    cumulative_coin_rewards = np.cumsum(daily_rewards)
    cumulative_usd_rewards = np.cumsum(daily_usd_rewards)
    cumulative_costs = np.cumsum(daily_costs)
    cumulative_profits = np.cumsum(daily_profits)
    
    # Calculate ROI timeline
    roi_reached = np.searchsorted(cumulative_profits, profitability['contract_cost'], side='left')
    roi_day = roi_reached if roi_reached < days else None
    
    return {
        'dates': dates,
        'daily_rewards': daily_rewards,
        'daily_usd_rewards': daily_usd_rewards,
        'daily_costs': daily_costs,
        'daily_profits': daily_profits,
        'cumulative_coin_rewards': cumulative_coin_rewards,
        'cumulative_usd_rewards': cumulative_usd_rewards,
        'cumulative_costs': cumulative_costs,
        'cumulative_profits': cumulative_profits,
        'roi_day': roi_day
    }

def render_page():
    st.header("Cryptocurrency Mining")
    
    st.markdown("""
    Cloud mining allows you to mine cryptocurrencies without owning hardware.
    Compare mining contracts, calculate profitability, and manage your mining operations.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Mining Options", "My Mining Contracts", "Profitability Calculator"])
    
    with tab1:
        st.subheader("Available Mining Contracts")
        
        # Get mining options
        mining_options = get_mining_options()
        
        # Display options in a table
        options_df = pd.DataFrame(mining_options)
        
        # Format columns for display
        display_df = options_df.copy()
        display_df['cost_per_unit'] = display_df.apply(
            lambda x: f"${x['cost_per_unit']:.4f} per {x['hashrate']} per day", axis=1
        )
        display_df['maintenance_fee'] = display_df.apply(
            lambda x: f"${x['maintenance_fee']:.4f} per {x['hashrate']} per day", axis=1
        )
        display_df['min_purchase'] = display_df.apply(
            lambda x: f"{x['min_purchase']} {x['hashrate']}", axis=1
        )
        display_df['contract_duration'] = display_df['contract_duration'].apply(
            lambda x: f"{x} days" if x < 365*2 else f"{x//365} years"
        )
        
        # Drop the hashrate column as it's redundant now
        display_df = display_df.drop(columns=['hashrate'])
        
        st.dataframe(display_df, use_container_width=True)
        
        # Mining contract comparison
        st.subheader("Contract Comparison")
        
        # Calculate daily costs and estimated profits for each option
        comparison_data = []
        
        for option in mining_options:
            # Use minimum purchase amount for comparison
            hashrate = option['min_purchase']
            coin = option['coin']
            
            profitability = calculate_mining_profitability(coin, hashrate)
            
            if profitability:
                comparison_data.append({
                    'coin': coin,
                    'hashrate': f"{hashrate} {option['hashrate']}",
                    'daily_cost': profitability['total_daily_cost'],
                    'daily_revenue': profitability['daily_usd_reward'],
                    'daily_profit': profitability['daily_profit'],
                    'monthly_profit': profitability['monthly_profit'],
                    'roi_days': profitability['roi_days']
                })
        
        # Create comparison dataframe
        comparison_df = pd.DataFrame(comparison_data)
        
        # Create profitability chart
        fig = px.bar(
            comparison_df.sort_values(by='daily_profit', ascending=False),
            x='coin',
            y=['daily_revenue', 'daily_cost'],
            barmode='group',
            labels={'value': 'USD per Day', 'coin': 'Cryptocurrency', 'variable': 'Type'},
            title='Daily Revenue vs Cost (Minimum Purchase)',
            color_discrete_map={'daily_revenue': 'green', 'daily_cost': 'red'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create ROI comparison chart
        roi_df = comparison_df[comparison_df['roi_days'] < float('inf')].copy()
        
        if not roi_df.empty:
            fig2 = px.bar(
                roi_df.sort_values(by='roi_days'),
                x='coin',
                y='roi_days',
                labels={'roi_days': 'Days to ROI', 'coin': 'Cryptocurrency'},
                title='Days to Return on Investment (ROI)',
                color='roi_days',
                color_continuous_scale='Viridis_r'  # Reversed scale (lower is better)
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No contracts have a positive ROI with current market conditions.")
        
        # Purchase a mining contract
        with st.expander("Purchase Mining Contract"):
            # Select coin
            selected_coin = st.selectbox("Select Cryptocurrency", [o['coin'] for o in mining_options])
            
            # Get selected option details
            selected_option = next((o for o in mining_options if o['coin'] == selected_coin), None)
            
            if selected_option:
                # Display selected option details
                st.markdown(f"""
                ### {selected_coin} Mining Details
                - Algorithm: {selected_option['algorithm']}
                - Minimum Purchase: {selected_option['min_purchase']} {selected_option['hashrate']}
                - Contract Duration: {selected_option['contract_duration']} days
                - Cost: ${selected_option['cost_per_unit']} per {selected_option['hashrate']} per day
                - Maintenance Fee: ${selected_option['maintenance_fee']} per {selected_option['hashrate']} per day
                """)
                
                # Input hashrate
                hashrate = st.number_input(
                    f"Hashrate ({selected_option['hashrate']})",
                    min_value=float(selected_option['min_purchase']),
                    step=float(selected_option['min_purchase']),
                    value=float(selected_option['min_purchase']) * 10
                )
                
                # Calculate profitability
                profitability = calculate_mining_profitability(selected_coin, hashrate)
                
                if profitability:
                    # Display profitability summary
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Daily Revenue", f"${profitability['daily_usd_reward']:.2f}")
                        st.metric("Daily Cost", f"${profitability['total_daily_cost']:.2f}")
                    
                    with col2:
                        st.metric("Daily Profit", f"${profitability['daily_profit']:.2f}")
                        st.metric("Monthly Profit", f"${profitability['monthly_profit']:.2f}")
                    
                    # Display contract cost and ROI
                    st.metric("Contract Cost", f"${profitability['contract_cost']:.2f}")
                    
                    if profitability['daily_profit'] > 0:
                        st.metric("Days to ROI", f"{profitability['roi_days']:.0f}")
                    else:
                        st.error("This contract is not profitable with current market conditions.")
                    
                    # Purchase button
                    if st.button("Purchase Mining Contract"):
                        st.success(f"Mining contract purchased: {hashrate} {selected_option['hashrate']} of {selected_coin}")
                        # In a real implementation, this would process the purchase
    
    with tab2:
        st.subheader("My Mining Contracts")
        
        # Get user's mining contracts
        contracts = get_user_mining_contracts()
        
        if not contracts:
            st.info("You don't have any active mining contracts. Purchase a contract to see it here.")
        else:
            # Summary metrics
            total_daily_revenue = sum(contract['daily_revenue'] for contract in contracts)
            total_daily_cost = sum(contract['daily_cost'] for contract in contracts)
            total_daily_profit = sum(contract['daily_profit'] for contract in contracts)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Daily Revenue", f"${total_daily_revenue:.2f}")
            
            with col2:
                st.metric("Total Daily Cost", f"${total_daily_cost:.2f}")
            
            with col3:
                st.metric("Total Daily Profit", f"${total_daily_profit:.2f}")
            
            # Display contracts table
            display_df = pd.DataFrame(contracts)
            
            # Format columns
            display_df['daily_earnings'] = display_df.apply(
                lambda x: f"{x['daily_earnings']} {x['coin'].split(' ')[0]}", axis=1
            )
            display_df['daily_revenue'] = display_df['daily_revenue'].apply(lambda x: f"${x:.2f}")
            display_df['daily_cost'] = display_df['daily_cost'].apply(lambda x: f"${x:.2f}")
            display_df['daily_profit'] = display_df['daily_profit'].apply(lambda x: f"${x:.2f}")
            
            # Add hashrate unit to hashrate column
            mining_options = get_mining_options()
            
            def get_hashrate_with_unit(row):
                option = next((o for o in mining_options if o['coin'] == row['coin']), None)
                unit = option['hashrate'] if option else ''
                return f"{row['hashrate']} {unit}"
            
            display_df['hashrate'] = display_df.apply(get_hashrate_with_unit, axis=1)
            
            st.dataframe(display_df, use_container_width=True)
            
            # Visualization of mining contracts
            st.subheader("Mining Profits Breakdown")
            
            # Create profit breakdown chart
            contracts_df = pd.DataFrame(contracts)
            
            fig = go.Figure()
            
            # Add revenue bars
            fig.add_trace(go.Bar(
                x=contracts_df['coin'],
                y=contracts_df['daily_revenue'],
                name='Daily Revenue',
                marker_color='green'
            ))
            
            # Add cost bars
            fig.add_trace(go.Bar(
                x=contracts_df['coin'],
                y=contracts_df['daily_cost'],
                name='Daily Cost',
                marker_color='red'
            ))
            
            # Add profit bars
            fig.add_trace(go.Bar(
                x=contracts_df['coin'],
                y=contracts_df['daily_profit'],
                name='Daily Profit',
                marker_color='blue'
            ))
            
            fig.update_layout(
                title='Daily Mining Economics by Coin',
                xaxis_title='Cryptocurrency',
                yaxis_title='USD per Day',
                barmode='group',
                legend_title='Type'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Mining contract expiry timeline
            st.subheader("Contract Expiry Timeline")
            
            # Create expiry timeline
            timeline_data = []
            
            for contract in contracts:
                start_date = datetime.strptime(contract['contract_start'], "%Y-%m-%d")
                end_date = datetime.strptime(contract['contract_end'], "%Y-%m-%d")
                duration = (end_date - start_date).days
                days_left = (end_date - datetime.now()).days
                
                timeline_data.append({
                    'coin': contract['coin'],
                    'start_date': start_date,
                    'end_date': end_date,
                    'duration': duration,
                    'days_left': days_left,
                    'progress': (duration - days_left) / duration * 100
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            # Create timeline chart
            fig2 = px.timeline(
                timeline_df,
                x_start='start_date',
                x_end='end_date',
                y='coin',
                color='progress',
                color_continuous_scale='Viridis',
                labels={'progress': 'Progress (%)'},
                title='Mining Contract Timeline'
            )
            
            fig2.update_yaxes(autorange="reversed")
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("Mining Profitability Calculator")
        st.markdown("Calculate and project potential earnings from cryptocurrency mining.")
        
        # Select coin and input parameters
        col1, col2 = st.columns(2)
        
        with col1:
            mining_options = get_mining_options()
            selected_coin = st.selectbox("Select Cryptocurrency", [o['coin'] for o in mining_options])
            
            # Get selected option details
            selected_option = next((o for o in mining_options if o['coin'] == selected_coin), None)
            
            # Input hashrate
            hashrate = st.number_input(
                f"Hashrate ({selected_option['hashrate']})",
                min_value=float(selected_option['min_purchase']),
                step=float(selected_option['min_purchase']),
                value=float(selected_option['min_purchase']) * 10
            )
        
        with col2:
            electricity_cost = st.slider("Electricity Cost ($/kWh)", 0.01, 0.50, 0.10, 0.01)
            time_period = st.slider("Projection Period (days)", 30, 365, 180)
        
        # Calculate initial profitability
        profitability = calculate_mining_profitability(selected_coin, hashrate, electricity_cost)
        
        if profitability:
            # Display profitability summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Daily Revenue", f"${profitability['daily_usd_reward']:.2f}")
                st.metric("Daily Coin Reward", f"{profitability['daily_coin_reward']:.8f} {selected_coin.split(' ')[0]}")
            
            with col2:
                st.metric("Daily Cost", f"${profitability['total_daily_cost']:.2f}")
                st.metric("Monthly Cost", f"${profitability['total_daily_cost'] * 30:.2f}")
            
            with col3:
                st.metric("Daily Profit", f"${profitability['daily_profit']:.2f}")
                st.metric("Monthly Profit", f"${profitability['monthly_profit']:.2f}")
            
            # Project earnings
            earnings_projection = project_mining_earnings(selected_coin, hashrate, time_period)
            
            if earnings_projection:
                # Display ROI details
                st.subheader("Return on Investment")
                
                if earnings_projection['roi_day'] is not None:
                    roi_date = earnings_projection['dates'][earnings_projection['roi_day']]
                    roi_days = earnings_projection['roi_day']
                    st.success(f"Expected to reach ROI in {roi_days} days (approximately {roi_date.strftime('%Y-%m-%d')})")
                else:
                    st.warning("ROI not reached within the projected period. Consider a longer timeframe or different parameters.")
                
                # Create projection dataframe
                projection_df = pd.DataFrame({
                    'Date': earnings_projection['dates'],
                    'Daily Profit': earnings_projection['daily_profits'],
                    'Cumulative Profit': earnings_projection['cumulative_profits'],
                    'Cumulative Revenue': earnings_projection['cumulative_usd_rewards'],
                    'Cumulative Cost': earnings_projection['cumulative_costs'],
                    f"Cumulative {selected_coin.split(' ')[0]}": earnings_projection['cumulative_coin_rewards']
                })
                
                # Plot cumulative profit
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=projection_df['Date'],
                    y=projection_df['Cumulative Revenue'],
                    name='Cumulative Revenue',
                    mode='lines',
                    line=dict(color='green')
                ))
                
                fig.add_trace(go.Scatter(
                    x=projection_df['Date'],
                    y=projection_df['Cumulative Cost'],
                    name='Cumulative Cost',
                    mode='lines',
                    line=dict(color='red')
                ))
                
                fig.add_trace(go.Scatter(
                    x=projection_df['Date'],
                    y=projection_df['Cumulative Profit'],
                    name='Cumulative Profit',
                    mode='lines',
                    line=dict(color='blue')
                ))
                
                # Add horizontal line at contract cost
                fig.add_shape(
                    type="line",
                    x0=projection_df['Date'].min(),
                    y0=profitability['contract_cost'],
                    x1=projection_df['Date'].max(),
                    y1=profitability['contract_cost'],
                    line=dict(
                        color="orange",
                        width=2,
                        dash="dash",
                    ),
                    name="Contract Cost"
                )
                
                fig.add_annotation(
                    x=projection_df['Date'].min(),
                    y=profitability['contract_cost'],
                    text="Contract Cost",
                    showarrow=True,
                    arrowhead=1,
                    ax=50,
                    ay=-20
                )
                
                # Add vertical line at ROI date if applicable
                if earnings_projection['roi_day'] is not None:
                    roi_date = earnings_projection['dates'][earnings_projection['roi_day']]
                    
                    fig.add_shape(
                        type="line",
                        x0=roi_date,
                        y0=0,
                        x1=roi_date,
                        y1=max(projection_df['Cumulative Revenue'].max(), profitability['contract_cost'] * 1.1),
                        line=dict(
                            color="green",
                            width=2,
                            dash="dash",
                        )
                    )
                    
                    fig.add_annotation(
                        x=roi_date,
                        y=profitability['contract_cost'],
                        text="ROI Date",
                        showarrow=True,
                        arrowhead=1,
                        ax=-50,
                        ay=0
                    )
                
                fig.update_layout(
                    title=f'Projected Mining Economics over {time_period} Days',
                    xaxis_title='Date',
                    yaxis_title='USD',
                    legend_title='Metric'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Plot daily profit trend
                fig2 = px.line(
                    projection_df,
                    x='Date',
                    y='Daily Profit',
                    title='Projected Daily Profit Trend',
                    labels={'Daily Profit': 'USD per Day', 'Date': 'Date'}
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Show accumulated coins
                st.subheader(f"Projected {selected_coin.split(' ')[0]} Accumulation")
                
                fig3 = px.line(
                    projection_df,
                    x='Date',
                    y=f"Cumulative {selected_coin.split(' ')[0]}",
                    title=f'Projected {selected_coin.split(" ")[0]} Accumulation',
                    labels={f"Cumulative {selected_coin.split(' ')[0]}": selected_coin.split(' ')[0], 'Date': 'Date'}
                )
                
                st.plotly_chart(fig3, use_container_width=True)
                
                # Profitability comparison with different electricity costs
                st.subheader("Electricity Cost Sensitivity Analysis")
                
                # Calculate profitability for different electricity costs
                electricity_costs = [0.05, 0.10, 0.15, 0.20, 0.25]
                sensitivity_data = []
                
                for cost in electricity_costs:
                    prof = calculate_mining_profitability(selected_coin, hashrate, cost)
                    
                    if prof:
                        sensitivity_data.append({
                            'Electricity Cost': f"${cost:.2f}/kWh",
                            'Daily Profit': prof['daily_profit'],
                            'Monthly Profit': prof['monthly_profit'],
                            'Annual Profit': prof['annual_profit'],
                            'ROI Days': prof['roi_days']
                        })
                
                sensitivity_df = pd.DataFrame(sensitivity_data)
                
                # Create sensitivity chart
                fig4 = px.bar(
                    sensitivity_df,
                    x='Electricity Cost',
                    y=['Daily Profit', 'Monthly Profit'],
                    barmode='group',
                    title='Profit Sensitivity to Electricity Cost',
                    labels={'value': 'Profit (USD)', 'variable': 'Profit Metric'}
                )
                
                st.plotly_chart(fig4, use_container_width=True)
                
                # Display ROI sensitivity
                roi_df = sensitivity_df[['Electricity Cost', 'ROI Days']].copy()
                
                # Filter out infinite ROI
                roi_df = roi_df[roi_df['ROI Days'] < float('inf')]
                
                if not roi_df.empty:
                    fig5 = px.bar(
                        roi_df,
                        x='Electricity Cost',
                        y='ROI Days',
                        title='ROI Days Sensitivity to Electricity Cost',
                        labels={'ROI Days': 'Days to Breakeven', 'Electricity Cost': 'Electricity Cost'}
                    )
                    
                    st.plotly_chart(fig5, use_container_width=True)
                else:
                    st.warning("ROI cannot be reached with the tested electricity costs.")
