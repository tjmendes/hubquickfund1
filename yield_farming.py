import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import data_storage as ds

def get_yield_farming_opportunities():
    """Get current yield farming opportunities"""
    # In a real implementation, this would fetch data from DeFi protocols
    return [
        {
            'protocol': 'Aave',
            'pool': 'USDC/USDT',
            'apy': 4.5,
            'tvl': 230000000,
            'risk_level': 'Low',
            'min_deposit': 1
        },
        {
            'protocol': 'Compound',
            'pool': 'ETH/USDC',
            'apy': 6.2,
            'tvl': 180000000,
            'risk_level': 'Low',
            'min_deposit': 0.1
        },
        {
            'protocol': 'Curve',
            'pool': '3pool (DAI/USDC/USDT)',
            'apy': 3.8,
            'tvl': 310000000,
            'risk_level': 'Low',
            'min_deposit': 10
        },
        {
            'protocol': 'Uniswap',
            'pool': 'ETH/WBTC',
            'apy': 8.4,
            'tvl': 95000000,
            'risk_level': 'Medium',
            'min_deposit': 0.05
        },
        {
            'protocol': 'Balancer',
            'pool': 'BAL/ETH/USDC',
            'apy': 12.7,
            'tvl': 42000000,
            'risk_level': 'Medium',
            'min_deposit': 5
        },
        {
            'protocol': 'SushiSwap',
            'pool': 'SUSHI/ETH',
            'apy': 18.5,
            'tvl': 28000000,
            'risk_level': 'High',
            'min_deposit': 1
        },
        {
            'protocol': 'PancakeSwap',
            'pool': 'CAKE/BNB',
            'apy': 24.3,
            'tvl': 68000000,
            'risk_level': 'High',
            'min_deposit': 5
        },
        {
            'protocol': 'Yearn Finance',
            'pool': 'yUSDC',
            'apy': 7.8,
            'tvl': 155000000,
            'risk_level': 'Medium',
            'min_deposit': 100
        }
    ]

def calculate_yield_returns(principal, apy, days):
    """Calculate potential returns based on APY and time period"""
    # Convert APY to daily rate
    daily_rate = (1 + apy/100) ** (1/365) - 1
    
    # Initialize arrays for cumulative values
    dates = [datetime.now() + timedelta(days=i) for i in range(days)]
    balance = [principal * (1 + daily_rate) ** i for i in range(days)]
    
    # Calculate daily interest
    daily_interest = [balance[i] - (balance[i-1] if i > 0 else principal) for i in range(days)]
    
    # Calculate cumulative interest
    cumulative_interest = [sum(daily_interest[:i+1]) for i in range(days)]
    
    return {
        'dates': dates,
        'balance': balance,
        'daily_interest': daily_interest,
        'cumulative_interest': cumulative_interest
    }

def simulate_yield_farming(principal, apy, days, compound_frequency=1):
    """Simulate yield farming returns with different compounding frequencies"""
    # Frequencies: 1=daily, 7=weekly, 30=monthly
    periods = days // compound_frequency
    
    # Convert APY to the rate for the compounding period
    period_rate = (1 + apy/100) ** (compound_frequency/365) - 1
    
    # Initialize arrays
    dates = []
    balance = []
    
    current_date = datetime.now()
    current_balance = principal
    
    # Simulate compounding
    for i in range(periods + 1):
        dates.append(current_date + timedelta(days=i*compound_frequency))
        balance.append(current_balance)
        
        if i < periods:
            # Compound the balance
            current_balance *= (1 + period_rate)
    
    return {
        'dates': dates,
        'balance': balance
    }

def get_user_farms():
    """Get user's current yield farms"""
    # In a real implementation, this would fetch from the user's connected wallets
    return [
        {
            'protocol': 'Aave',
            'pool': 'USDC/USDT',
            'principal': 1000,
            'current_value': 1045.23,
            'apy': 4.5,
            'start_date': '2023-03-15',
            'earned': 45.23
        },
        {
            'protocol': 'Compound',
            'pool': 'ETH/USDC',
            'principal': 500,
            'current_value': 521.75,
            'apy': 6.2,
            'start_date': '2023-04-02',
            'earned': 21.75
        }
    ]

def render_page():
    st.header("Yield Farming")
    
    st.markdown("""
    Yield farming allows you to earn interest on your cryptocurrency holdings by providing liquidity to DeFi protocols.
    Monitor opportunities, track your farms, and simulate potential returns.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Opportunities", "My Farms", "Simulator"])
    
    with tab1:
        st.subheader("Current Yield Farming Opportunities")
        
        # Filters for yield farming opportunities
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_apy = st.slider("Minimum APY (%)", 0.0, 30.0, 0.0, 0.5)
        
        with col2:
            risk_levels = st.multiselect(
                "Risk Level",
                ["Low", "Medium", "High"],
                default=["Low", "Medium", "High"]
            )
        
        with col3:
            min_tvl = st.select_slider(
                "Minimum TVL",
                options=[1000000, 5000000, 10000000, 50000000, 100000000, 200000000, 300000000],
                value=1000000,
                format_func=lambda x: f"${x/1000000:.0f}M"
            )
        
        # Get opportunities and filter them
        opportunities = get_yield_farming_opportunities()
        filtered_opps = [
            o for o in opportunities 
            if o['apy'] >= min_apy and o['risk_level'] in risk_levels and o['tvl'] >= min_tvl
        ]
        
        if not filtered_opps:
            st.warning("No opportunities match your criteria. Try adjusting the filters.")
        else:
            # Convert to DataFrame for display
            df = pd.DataFrame(filtered_opps)
            
            # Format columns
            df['tvl'] = df['tvl'].apply(lambda x: f"${x/1000000:.1f}M")
            df['apy'] = df['apy'].apply(lambda x: f"{x:.1f}%")
            df['min_deposit'] = df['min_deposit'].apply(lambda x: f"${x}" if x >= 1 else f"{x} ETH/BTC")
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # APY comparison chart
            st.subheader("APY Comparison")
            
            # Convert APY back to numeric for plotting
            chart_df = pd.DataFrame(filtered_opps).sort_values(by='apy', ascending=False)
            
            fig = px.bar(
                chart_df,
                x='protocol',
                y='apy',
                color='risk_level',
                hover_data=['pool', 'tvl'],
                labels={'apy': 'APY (%)', 'protocol': 'Protocol'},
                title='Yield Farming APY by Protocol'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # TVL chart
            st.subheader("Total Value Locked (TVL)")
            
            fig2 = px.pie(
                chart_df,
                values='tvl',
                names='protocol',
                title='TVL Distribution by Protocol',
                hover_data=['pool', 'apy']
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("My Yield Farms")
        
        # Get user's farms
        user_farms = get_user_farms()
        
        if not user_farms:
            st.info("You don't have any active yield farms. Start farming to see them here.")
        else:
            # Summary metrics
            total_principal = sum(farm['principal'] for farm in user_farms)
            total_current = sum(farm['current_value'] for farm in user_farms)
            total_earned = sum(farm['earned'] for farm in user_farms)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Principal", f"${total_principal:.2f}")
            
            with col2:
                st.metric("Current Value", f"${total_current:.2f}", f"+${total_earned:.2f}")
            
            with col3:
                roi_pct = (total_earned / total_principal) * 100
                st.metric("Overall ROI", f"{roi_pct:.2f}%")
            
            # Display farms table
            st.dataframe(pd.DataFrame(user_farms), use_container_width=True)
            
            # Farm performance chart
            st.subheader("Farm Performance")
            
            # Create performance chart data
            farm_df = pd.DataFrame(user_farms)
            
            fig = go.Figure()
            
            # Add principal bars
            fig.add_trace(go.Bar(
                x=farm_df['protocol'] + ' (' + farm_df['pool'] + ')',
                y=farm_df['principal'],
                name='Principal',
                marker_color='lightblue'
            ))
            
            # Add earned bars
            fig.add_trace(go.Bar(
                x=farm_df['protocol'] + ' (' + farm_df['pool'] + ')',
                y=farm_df['earned'],
                name='Earned',
                marker_color='lightgreen'
            ))
            
            fig.update_layout(
                title='Principal vs Earned by Farm',
                xaxis_title='Farm',
                yaxis_title='USD Value',
                barmode='stack',
                legend_title='Type'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add new farm button
            with st.expander("Add New Farm"):
                protocol = st.selectbox("Protocol", [o['protocol'] for o in get_yield_farming_opportunities()])
                
                # Filter pools based on selected protocol
                protocol_pools = [o['pool'] for o in get_yield_farming_opportunities() if o['protocol'] == protocol]
                pool = st.selectbox("Pool", protocol_pools)
                
                amount = st.number_input("Amount to Deposit", min_value=0.01, step=0.01, value=100.0)
                start_date = st.date_input("Start Date", value=datetime.now())
                
                if st.button("Add Farm"):
                    st.success(f"Farm added successfully: {protocol} {pool} with ${amount:.2f}")
                    # In a real implementation, this would add the farm to the user's portfolio
    
    with tab3:
        st.subheader("Yield Farming Simulator")
        st.markdown("Simulate potential returns from yield farming with different parameters.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            principal = st.number_input("Initial Deposit (USD)", min_value=1.0, value=1000.0, step=100.0)
            apy = st.slider("Annual Percentage Yield (APY %)", 0.1, 100.0, 5.0, 0.1)
        
        with col2:
            time_period = st.slider("Time Period (days)", 1, 365, 90)
            compound_freq = st.radio("Compounding Frequency", ["Daily", "Weekly", "Monthly"], horizontal=True)
            
            # Convert to days
            if compound_freq == "Daily":
                compound_days = 1
            elif compound_freq == "Weekly":
                compound_days = 7
            else:  # Monthly
                compound_days = 30
        
        # Calculate returns
        returns = simulate_yield_farming(principal, apy, time_period, compound_days)
        
        # Final metrics
        final_balance = returns['balance'][-1]
        total_interest = final_balance - principal
        roi_pct = (total_interest / principal) * 100
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Final Balance", f"${final_balance:.2f}", f"+${total_interest:.2f}")
        
        with col2:
            st.metric("Total Interest", f"${total_interest:.2f}")
        
        with col3:
            st.metric("Return on Investment", f"{roi_pct:.2f}%")
        
        # Plot the results
        df = pd.DataFrame({
            'Date': returns['dates'],
            'Balance': returns['balance']
        })
        
        fig = px.line(
            df,
            x='Date',
            y='Balance',
            title=f'Projected Balance over {time_period} Days ({apy}% APY, {compound_freq} Compounding)',
            labels={'Balance': 'USD Value', 'Date': 'Date'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Compare different compounding frequencies
        st.subheader("Compounding Frequency Comparison")
        
        # Calculate for different frequencies
        daily_returns = simulate_yield_farming(principal, apy, time_period, 1)
        weekly_returns = simulate_yield_farming(principal, apy, time_period, 7)
        monthly_returns = simulate_yield_farming(principal, apy, time_period, 30)
        
        # Create comparison dataframe
        comparison_df = pd.DataFrame({
            'Date': daily_returns['dates'],
            'Daily Compounding': np.nan,
            'Weekly Compounding': np.nan,
            'Monthly Compounding': np.nan
        })
        
        # Fill in values (interpolating for different frequencies)
        for i, date in enumerate(comparison_df['Date']):
            # Daily (has values for all dates)
            if i < len(daily_returns['balance']):
                comparison_df.loc[i, 'Daily Compounding'] = daily_returns['balance'][i]
            
            # Weekly (has values every 7 days, interpolate others)
            weekly_idx = i // 7
            if weekly_idx < len(weekly_returns['balance']):
                if i % 7 == 0:  # exact weekly point
                    comparison_df.loc[i, 'Weekly Compounding'] = weekly_returns['balance'][weekly_idx]
                else:  # interpolated point
                    next_weekly_idx = min(weekly_idx + 1, len(weekly_returns['balance']) - 1)
                    prev_value = weekly_returns['balance'][weekly_idx]
                    next_value = weekly_returns['balance'][next_weekly_idx]
                    # Simple linear interpolation
                    factor = (i % 7) / 7
                    comparison_df.loc[i, 'Weekly Compounding'] = prev_value + (next_value - prev_value) * factor
            
            # Monthly (has values every 30 days, interpolate others)
            monthly_idx = i // 30
            if monthly_idx < len(monthly_returns['balance']):
                if i % 30 == 0:  # exact monthly point
                    comparison_df.loc[i, 'Monthly Compounding'] = monthly_returns['balance'][monthly_idx]
                else:  # interpolated point
                    next_monthly_idx = min(monthly_idx + 1, len(monthly_returns['balance']) - 1)
                    prev_value = monthly_returns['balance'][monthly_idx]
                    next_value = monthly_returns['balance'][next_monthly_idx]
                    # Simple linear interpolation
                    factor = (i % 30) / 30
                    comparison_df.loc[i, 'Monthly Compounding'] = prev_value + (next_value - prev_value) * factor
        
        # Sample every 7 days for a cleaner chart
        sampled_df = comparison_df.iloc[::7].copy()
        
        # Melt the dataframe for plotting
        melted_df = pd.melt(
            sampled_df,
            id_vars=['Date'],
            value_vars=['Daily Compounding', 'Weekly Compounding', 'Monthly Compounding'],
            var_name='Compounding Frequency',
            value_name='Balance'
        )
        
        # Create the comparison chart
        fig = px.line(
            melted_df,
            x='Date',
            y='Balance',
            color='Compounding Frequency',
            title=f'Effect of Compounding Frequency on Returns ({apy}% APY)',
            labels={'Balance': 'USD Value', 'Date': 'Date'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison table
        st.subheader("Final Results Comparison")
        
        comparison_table = pd.DataFrame({
            'Compounding Frequency': ['Daily', 'Weekly', 'Monthly'],
            'Final Balance': [
                daily_returns['balance'][-1],
                weekly_returns['balance'][-1],
                monthly_returns['balance'][-1]
            ],
            'Total Interest': [
                daily_returns['balance'][-1] - principal,
                weekly_returns['balance'][-1] - principal,
                monthly_returns['balance'][-1] - principal
            ],
            'ROI (%)': [
                (daily_returns['balance'][-1] - principal) / principal * 100,
                (weekly_returns['balance'][-1] - principal) / principal * 100,
                (monthly_returns['balance'][-1] - principal) / principal * 100
            ]
        })
        
        # Format the table
        comparison_table['Final Balance'] = comparison_table['Final Balance'].apply(lambda x: f"${x:.2f}")
        comparison_table['Total Interest'] = comparison_table['Total Interest'].apply(lambda x: f"${x:.2f}")
        comparison_table['ROI (%)'] = comparison_table['ROI (%)'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(comparison_table, use_container_width=True)
