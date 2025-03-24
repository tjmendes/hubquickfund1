import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import data_storage as ds

def get_staking_opportunities():
    """Get current staking opportunities"""
    # In a real implementation, this would fetch data from various blockchain networks
    return [
        {
            'asset': 'Ethereum (ETH)',
            'network': 'Ethereum',
            'type': 'PoS Staking',
            'apy': 4.0,
            'min_stake': 32,
            'lockup_period': 0,  # 0 = liquid staking
            'risk_level': 'Low'
        },
        {
            'asset': 'Ethereum (ETH)',
            'network': 'Lido',
            'type': 'Liquid Staking',
            'apy': 3.8,
            'min_stake': 0.01,
            'lockup_period': 0,
            'risk_level': 'Low'
        },
        {
            'asset': 'Cardano (ADA)',
            'network': 'Cardano',
            'type': 'PoS Staking',
            'apy': 5.2,
            'min_stake': 10,
            'lockup_period': 14,  # days
            'risk_level': 'Low'
        },
        {
            'asset': 'Polkadot (DOT)',
            'network': 'Polkadot',
            'type': 'Nominated PoS',
            'apy': 14.0,
            'min_stake': 120,
            'lockup_period': 28,
            'risk_level': 'Medium'
        },
        {
            'asset': 'Solana (SOL)',
            'network': 'Solana',
            'type': 'PoS Staking',
            'apy': 7.5,
            'min_stake': 1,
            'lockup_period': 3,
            'risk_level': 'Medium'
        },
        {
            'asset': 'Cosmos (ATOM)',
            'network': 'Cosmos',
            'type': 'PoS Staking',
            'apy': 11.0,
            'min_stake': 1,
            'lockup_period': 21,
            'risk_level': 'Medium'
        },
        {
            'asset': 'Algorand (ALGO)',
            'network': 'Algorand',
            'type': 'Pure PoS',
            'apy': 6.5,
            'min_stake': 1,
            'lockup_period': 0,
            'risk_level': 'Low'
        },
        {
            'asset': 'Tezos (XTZ)',
            'network': 'Tezos',
            'type': 'Liquid PoS',
            'apy': 5.8,
            'min_stake': 1,
            'lockup_period': 0,
            'risk_level': 'Low'
        },
        {
            'asset': 'Avalanche (AVAX)',
            'network': 'Avalanche',
            'type': 'PoS Staking',
            'apy': 9.2,
            'min_stake': 25,
            'lockup_period': 14,
            'risk_level': 'Medium'
        },
        {
            'asset': 'Binance Coin (BNB)',
            'network': 'BNB Chain',
            'type': 'DPoS Staking',
            'apy': 6.8,
            'min_stake': 1,
            'lockup_period': 7,
            'risk_level': 'Medium'
        }
    ]

def get_user_staking_positions():
    """Get user's current staking positions"""
    # In a real implementation, this would fetch from the user's connected wallets
    return [
        {
            'asset': 'Ethereum (ETH)',
            'network': 'Lido',
            'staked_amount': 2.5,
            'current_value': 7500,
            'apy': 3.8,
            'start_date': '2023-02-10',
            'earned': 105.23,
            'status': 'Active'
        },
        {
            'asset': 'Solana (SOL)',
            'network': 'Solana',
            'staked_amount': 50,
            'current_value': 1750,
            'apy': 7.5,
            'start_date': '2023-03-18',
            'earned': 42.86,
            'status': 'Active'
        },
        {
            'asset': 'Cardano (ADA)',
            'network': 'Cardano',
            'staked_amount': 2000,
            'current_value': 800,
            'apy': 5.2,
            'start_date': '2023-01-05',
            'earned': 18.33,
            'status': 'Active'
        }
    ]

def calculate_staking_returns(principal, apy, days, price, token_amount=None):
    """Calculate potential returns from staking over time"""
    if token_amount is None:
        token_amount = principal / price
    
    # Convert APY to daily rate
    daily_rate = (1 + apy/100) ** (1/365) - 1
    
    # Initialize arrays for values
    dates = [datetime.now() + timedelta(days=i) for i in range(days + 1)]
    token_balance = [token_amount * (1 + daily_rate) ** i for i in range(days + 1)]
    usd_balance = [tb * price for tb in token_balance]
    
    # Calculate daily rewards
    daily_token_rewards = [token_balance[i] - (token_balance[i-1] if i > 0 else token_amount) for i in range(days + 1)]
    daily_usd_rewards = [dr * price for dr in daily_token_rewards]
    
    # Calculate cumulative rewards
    cumulative_token_rewards = [sum(daily_token_rewards[:i+1]) for i in range(days + 1)]
    cumulative_usd_rewards = [sum(daily_usd_rewards[:i+1]) for i in range(days + 1)]
    
    return {
        'dates': dates,
        'token_balance': token_balance,
        'usd_balance': usd_balance,
        'daily_token_rewards': daily_token_rewards,
        'daily_usd_rewards': daily_usd_rewards,
        'cumulative_token_rewards': cumulative_token_rewards,
        'cumulative_usd_rewards': cumulative_usd_rewards
    }

def render_page():
    st.header("Cryptocurrency Staking")
    
    st.markdown("""
    Staking allows you to earn passive income by participating in blockchain networks' consensus mechanisms.
    Stake your assets, earn rewards, and contribute to network security.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Staking Opportunities", "My Staking Positions", "Staking Calculator"])
    
    with tab1:
        st.subheader("Current Staking Opportunities")
        
        # Filters for staking opportunities
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_apy = st.slider("Minimum APY (%)", 0.0, 15.0, 0.0, 0.5)
        
        with col2:
            risk_levels = st.multiselect(
                "Risk Level",
                ["Low", "Medium", "High"],
                default=["Low", "Medium"]
            )
        
        with col3:
            max_lockup = st.slider("Maximum Lockup Period (days)", 0, 30, 30)
        
        # Get opportunities and filter them
        opportunities = get_staking_opportunities()
        filtered_opps = [
            o for o in opportunities 
            if o['apy'] >= min_apy and o['risk_level'] in risk_levels and o['lockup_period'] <= max_lockup
        ]
        
        if not filtered_opps:
            st.warning("No opportunities match your criteria. Try adjusting the filters.")
        else:
            # Convert to DataFrame for display
            df = pd.DataFrame(filtered_opps)
            
            # Format columns for display
            display_df = df.copy()
            display_df['apy'] = display_df['apy'].apply(lambda x: f"{x:.1f}%")
            display_df['min_stake'] = display_df['min_stake'].apply(lambda x: f"{x} tokens")
            
            # Add lockup period description
            display_df['lockup_period'] = display_df['lockup_period'].apply(
                lambda x: "No lockup (liquid)" if x == 0 else f"{x} days"
            )
            
            # Display table
            st.dataframe(display_df, use_container_width=True)
            
            # APY comparison chart
            st.subheader("APY Comparison")
            
            # Create chart
            fig = px.bar(
                df.sort_values(by='apy', ascending=False),
                x='asset',
                y='apy',
                color='risk_level',
                hover_data=['network', 'lockup_period'],
                labels={'apy': 'APY (%)', 'asset': 'Asset'},
                title='Staking APY by Asset'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Lockup comparison
            st.subheader("Lockup Period Comparison")
            
            # Create chart
            fig2 = px.bar(
                df.sort_values(by='lockup_period'),
                x='asset',
                y='lockup_period',
                color='network',
                labels={'lockup_period': 'Lockup Period (days)', 'asset': 'Asset'},
                title='Staking Lockup Period by Asset'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("My Staking Positions")
        
        # Get user's staking positions
        positions = get_user_staking_positions()
        
        if not positions:
            st.info("You don't have any active staking positions. Start staking to see them here.")
        else:
            # Summary metrics
            total_value = sum(position['current_value'] for position in positions)
            total_earned = sum(position['earned'] for position in positions)
            avg_apy = sum(position['apy'] * position['current_value'] for position in positions) / total_value
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Staked Value", f"${total_value:,.2f}")
            
            with col2:
                st.metric("Total Earnings", f"${total_earned:.2f}")
            
            with col3:
                st.metric("Average APY", f"{avg_apy:.2f}%")
            
            # Display positions table
            display_df = pd.DataFrame(positions)
            
            # Format columns
            display_df['apy'] = display_df['apy'].apply(lambda x: f"{x:.1f}%")
            display_df['current_value'] = display_df['current_value'].apply(lambda x: f"${x:,.2f}")
            display_df['earned'] = display_df['earned'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Staking positions chart
            st.subheader("Staking Positions Breakdown")
            
            # Create pie chart for value distribution
            positions_df = pd.DataFrame(positions)
            
            fig = px.pie(
                positions_df,
                values='current_value',
                names='asset',
                title='Staked Value Distribution',
                hover_data=['network', 'apy', 'earned']
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Staking rewards chart
            st.subheader("Staking Rewards")
            
            # Create bar chart for rewards
            fig2 = go.Figure()
            
            # Add bars for current value
            fig2.add_trace(go.Bar(
                x=positions_df['asset'],
                y=positions_df['current_value'],
                name='Current Value',
                marker_color='lightblue'
            ))
            
            # Add bars for earned rewards
            fig2.add_trace(go.Bar(
                x=positions_df['asset'],
                y=positions_df['earned'],
                name='Earned Rewards',
                marker_color='lightgreen'
            ))
            
            fig2.update_layout(
                title='Current Value vs Earned Rewards',
                xaxis_title='Asset',
                yaxis_title='USD Value',
                barmode='group',
                legend_title='Type'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Add new staking position
            with st.expander("Add New Staking Position"):
                # Get opportunities for selection
                opportunities = get_staking_opportunities()
                assets = sorted(set(o['asset'] for o in opportunities))
                
                asset = st.selectbox("Asset", assets)
                
                # Filter networks based on selected asset
                networks = [o['network'] for o in opportunities if o['asset'] == asset]
                network = st.selectbox("Network/Provider", networks)
                
                # Get selected opportunity details
                selected_opportunity = next((o for o in opportunities if o['asset'] == asset and o['network'] == network), None)
                
                if selected_opportunity:
                    st.info(f"APY: {selected_opportunity['apy']}% | Lockup: {selected_opportunity['lockup_period']} days | Minimum Stake: {selected_opportunity['min_stake']} tokens")
                
                amount = st.number_input("Amount to Stake", min_value=float(selected_opportunity['min_stake']) if selected_opportunity else 0.01, step=0.01)
                start_date = st.date_input("Start Date", value=datetime.now())
                
                if st.button("Add Staking Position"):
                    if selected_opportunity and amount >= selected_opportunity['min_stake']:
                        st.success(f"Staking position added successfully: {amount} {asset} on {network}")
                        # In a real implementation, this would add the position to the user's portfolio
                    else:
                        st.error(f"Amount must be at least {selected_opportunity['min_stake']} tokens")
    
    with tab3:
        st.subheader("Staking Calculator")
        st.markdown("Simulate potential returns from staking different assets.")
        
        # Asset selection
        opportunities = get_staking_opportunities()
        assets = sorted(set(o['asset'] for o in opportunities))
        
        asset = st.selectbox("Select Asset", assets)
        
        # Filter networks based on selected asset
        networks = [o['network'] for o in opportunities if o['asset'] == asset]
        network = st.selectbox("Select Network/Provider", networks)
        
        # Get selected opportunity details
        selected_opportunity = next((o for o in opportunities if o['asset'] == asset and o['network'] == network), None)
        
        if selected_opportunity:
            # Define asset price (would be fetched from API in real implementation)
            asset_prices = {
                'Ethereum (ETH)': 3000,
                'Cardano (ADA)': 0.4,
                'Polkadot (DOT)': 6.5,
                'Solana (SOL)': 35,
                'Cosmos (ATOM)': 8.2,
                'Algorand (ALGO)': 0.15,
                'Tezos (XTZ)': 0.9,
                'Avalanche (AVAX)': 12.8,
                'Binance Coin (BNB)': 240,
            }
            
            asset_price = asset_prices.get(asset, 1.0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                input_type = st.radio("Input Type", ["USD Amount", "Token Amount"])
                
                if input_type == "USD Amount":
                    usd_amount = st.number_input("USD Amount to Stake", min_value=1.0, value=1000.0, step=100.0)
                    token_amount = usd_amount / asset_price
                    st.info(f"Equivalent to {token_amount:.6f} {asset.split(' ')[0]}")
                else:
                    token_amount = st.number_input("Token Amount to Stake", min_value=float(selected_opportunity['min_stake']), value=float(selected_opportunity['min_stake']) * 2, step=float(selected_opportunity['min_stake']))
                    usd_amount = token_amount * asset_price
                    st.info(f"Equivalent to ${usd_amount:.2f}")
            
            with col2:
                apy = st.slider("APY (%)", 0.1, 20.0, selected_opportunity['apy'], 0.1)
                time_period = st.slider("Staking Period (days)", 30, 365, 90)
                
                # Display lockup information
                if selected_opportunity['lockup_period'] > 0:
                    st.warning(f"Note: This asset has a lockup period of {selected_opportunity['lockup_period']} days")
            
            # Calculate returns
            if input_type == "USD Amount":
                returns = calculate_staking_returns(usd_amount, apy, time_period, asset_price)
            else:
                returns = calculate_staking_returns(0, apy, time_period, asset_price, token_amount)
            
            # Display summary metrics
            final_token_balance = returns['token_balance'][-1]
            final_usd_balance = returns['usd_balance'][-1]
            total_token_rewards = returns['cumulative_token_rewards'][-1]
            total_usd_rewards = returns['cumulative_usd_rewards'][-1]
            
            # Summary row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Final Token Balance", f"{final_token_balance:.6f} {asset.split(' ')[0]}", f"+{total_token_rewards:.6f}")
            
            with col2:
                st.metric("Final USD Value", f"${final_usd_balance:.2f}", f"+${total_usd_rewards:.2f}")
            
            with col3:
                roi_pct = (total_usd_rewards / usd_amount) * 100 if usd_amount > 0 else 0
                st.metric("ROI", f"{roi_pct:.2f}%")
            
            # Visualization tabs
            viz_tab1, viz_tab2 = st.tabs(["Token Balance", "USD Value"])
            
            with viz_tab1:
                # Create dataframe for token balance visualization
                token_df = pd.DataFrame({
                    'Date': returns['dates'],
                    'Token Balance': returns['token_balance'],
                    'Cumulative Rewards': returns['cumulative_token_rewards']
                })
                
                # Plot token balance
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=token_df['Date'],
                    y=token_df['Token Balance'],
                    name='Token Balance',
                    mode='lines',
                    line=dict(color='blue')
                ))
                
                fig.add_trace(go.Scatter(
                    x=token_df['Date'],
                    y=token_df['Cumulative Rewards'],
                    name='Cumulative Rewards',
                    mode='lines',
                    line=dict(color='green')
                ))
                
                fig.update_layout(
                    title=f'Projected Token Balance over {time_period} Days',
                    xaxis_title='Date',
                    yaxis_title=f'Amount ({asset.split(" ")[0]})',
                    legend_title='Type'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with viz_tab2:
                # Create dataframe for USD value visualization
                usd_df = pd.DataFrame({
                    'Date': returns['dates'],
                    'USD Balance': returns['usd_balance'],
                    'Cumulative USD Rewards': returns['cumulative_usd_rewards']
                })
                
                # Plot USD value
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=usd_df['Date'],
                    y=usd_df['USD Balance'],
                    name='USD Balance',
                    mode='lines',
                    line=dict(color='blue')
                ))
                
                fig.add_trace(go.Scatter(
                    x=usd_df['Date'],
                    y=usd_df['Cumulative USD Rewards'],
                    name='Cumulative Rewards',
                    mode='lines',
                    line=dict(color='green')
                ))
                
                fig.update_layout(
                    title=f'Projected USD Value over {time_period} Days',
                    xaxis_title='Date',
                    yaxis_title='USD Value',
                    legend_title='Type'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Compare different APYs
            st.subheader("APY Comparison")
            
            # Calculate for different APYs
            apy_values = [apy/2, apy, apy*1.5]
            apy_returns = []
            
            for test_apy in apy_values:
                if input_type == "USD Amount":
                    apy_return = calculate_staking_returns(usd_amount, test_apy, time_period, asset_price)
                else:
                    apy_return = calculate_staking_returns(0, test_apy, time_period, asset_price, token_amount)
                apy_returns.append(apy_return)
            
            # Create comparison dataframe
            comparison_df = pd.DataFrame({
                'Date': apy_returns[0]['dates'],
                f'APY {apy_values[0]:.1f}%': np.nan,
                f'APY {apy_values[1]:.1f}%': np.nan,
                f'APY {apy_values[2]:.1f}%': np.nan
            })
            
            # Fill in USD values
            for i, date in enumerate(comparison_df['Date']):
                for j, test_apy in enumerate(apy_values):
                    if i < len(apy_returns[j]['usd_balance']):
                        comparison_df.loc[i, f'APY {test_apy:.1f}%'] = apy_returns[j]['usd_balance'][i]
            
            # Sample every 7 days for a cleaner chart
            sampled_df = comparison_df.iloc[::7].copy()
            
            # Melt the dataframe for plotting
            melted_df = pd.melt(
                sampled_df,
                id_vars=['Date'],
                value_vars=[f'APY {apy:.1f}%' for apy in apy_values],
                var_name='APY Rate',
                value_name='USD Value'
            )
            
            # Create the comparison chart
            fig = px.line(
                melted_df,
                x='Date',
                y='USD Value',
                color='APY Rate',
                title=f'Effect of Different APY Rates on Returns',
                labels={'USD Value': 'USD Value', 'Date': 'Date'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Comparison table
            st.subheader("Final Results Comparison")
            
            comparison_table = pd.DataFrame({
                'APY Rate': [f'{apy:.1f}%' for apy in apy_values],
                'Final Token Balance': [
                    apy_returns[i]['token_balance'][-1] for i in range(len(apy_values))
                ],
                'Token Rewards': [
                    apy_returns[i]['cumulative_token_rewards'][-1] for i in range(len(apy_values))
                ],
                'Final USD Value': [
                    apy_returns[i]['usd_balance'][-1] for i in range(len(apy_values))
                ],
                'USD Rewards': [
                    apy_returns[i]['cumulative_usd_rewards'][-1] for i in range(len(apy_values))
                ],
                'ROI (%)': [
                    (apy_returns[i]['cumulative_usd_rewards'][-1] / usd_amount) * 100 if usd_amount > 0 else 0
                    for i in range(len(apy_values))
                ]
            })
            
            # Format the table
            comparison_table['Final Token Balance'] = comparison_table['Final Token Balance'].apply(lambda x: f"{x:.6f}")
            comparison_table['Token Rewards'] = comparison_table['Token Rewards'].apply(lambda x: f"{x:.6f}")
            comparison_table['Final USD Value'] = comparison_table['Final USD Value'].apply(lambda x: f"${x:.2f}")
            comparison_table['USD Rewards'] = comparison_table['USD Rewards'].apply(lambda x: f"${x:.2f}")
            comparison_table['ROI (%)'] = comparison_table['ROI (%)'].apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(comparison_table, use_container_width=True)
