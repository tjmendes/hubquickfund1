import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import data_storage as ds

def get_upcoming_airdrops():
    """Get upcoming cryptocurrency airdrops"""
    # In a real implementation, this would fetch data from airdrop tracking APIs
    return [
        {
            'project': 'DeFi Protocol X',
            'token': 'DPX',
            'category': 'DeFi',
            'estimated_value': 'Medium',
            'requirements': 'Interact with protocol, min 10 transactions',
            'deadline': '2023-07-15',
            'status': 'Upcoming',
            'snapshot_date': '2023-07-10',
            'difficulty': 'Medium'
        },
        {
            'project': 'ZK Layer 2',
            'token': 'ZKL',
            'category': 'Layer 2',
            'estimated_value': 'High',
            'requirements': 'Bridge assets, min $500 TVL',
            'deadline': '2023-07-25',
            'status': 'Upcoming',
            'snapshot_date': '2023-07-20',
            'difficulty': 'Medium'
        },
        {
            'project': 'NFT Marketplace Alpha',
            'token': 'NFTA',
            'category': 'NFT',
            'estimated_value': 'Medium',
            'requirements': 'List an NFT, make a purchase',
            'deadline': '2023-08-05',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-01',
            'difficulty': 'Easy'
        },
        {
            'project': 'GameFi World',
            'token': 'GAME',
            'category': 'GameFi',
            'estimated_value': 'Low',
            'requirements': 'Create account, complete tutorial',
            'deadline': '2023-08-10',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-08',
            'difficulty': 'Easy'
        },
        {
            'project': 'Cross-Chain Bridge',
            'token': 'CCB',
            'category': 'Infrastructure',
            'estimated_value': 'High',
            'requirements': 'Bridge at least 3 different assets, min $1000',
            'deadline': '2023-08-15',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-12',
            'difficulty': 'Hard'
        },
        {
            'project': 'DAO Governance',
            'token': 'DAOG',
            'category': 'DAO',
            'estimated_value': 'Medium',
            'requirements': 'Participate in voting, delegate tokens',
            'deadline': '2023-08-20',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-18',
            'difficulty': 'Medium'
        },
        {
            'project': 'Privacy Protocol',
            'token': 'PRIV',
            'category': 'Privacy',
            'estimated_value': 'High',
            'requirements': 'Use the protocol for at least 5 transactions',
            'deadline': '2023-08-25',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-22',
            'difficulty': 'Hard'
        },
        {
            'project': 'Social DApp',
            'token': 'SOCIAL',
            'category': 'Social',
            'estimated_value': 'Low',
            'requirements': 'Create profile, make 3 posts',
            'deadline': '2023-09-01',
            'status': 'Upcoming',
            'snapshot_date': '2023-08-30',
            'difficulty': 'Easy'
        }
    ]

def get_completed_airdrops():
    """Get user's completed airdrop tasks"""
    # In a real implementation, this would fetch from the user's history
    return [
        {
            'project': 'DeFi Lender',
            'token': 'LEND',
            'category': 'DeFi',
            'completion_date': '2023-05-15',
            'status': 'Completed',
            'tokens_received': 500,
            'value_at_receipt': 250,
            'current_value': 320
        },
        {
            'project': 'DEX Aggregator',
            'token': 'DEXAG',
            'category': 'DeFi',
            'completion_date': '2023-04-20',
            'status': 'Completed',
            'tokens_received': 100,
            'value_at_receipt': 150,
            'current_value': 80
        },
        {
            'project': 'Metaverse Project',
            'token': 'META',
            'category': 'Metaverse',
            'completion_date': '2023-03-10',
            'status': 'Completed',
            'tokens_received': 1000,
            'value_at_receipt': 300,
            'current_value': 450
        }
    ]

def get_active_tasks():
    """Get user's active airdrop tasks"""
    # In a real implementation, this would fetch from the user's current tasks
    return [
        {
            'project': 'ZK Layer 2',
            'token': 'ZKL',
            'category': 'Layer 2',
            'tasks': [
                {'name': 'Bridge ETH to ZK Layer 2', 'completed': True},
                {'name': 'Perform at least 3 swaps', 'completed': True},
                {'name': 'Provide liquidity (min $100)', 'completed': False},
                {'name': 'Stay in liquidity pool until snapshot', 'completed': False}
            ],
            'progress': 50,
            'deadline': '2023-07-25',
            'snapshot_date': '2023-07-20',
            'estimated_value': 'High'
        },
        {
            'project': 'NFT Marketplace Alpha',
            'token': 'NFTA',
            'category': 'NFT',
            'tasks': [
                {'name': 'Connect wallet', 'completed': True},
                {'name': 'List an NFT for sale', 'completed': False},
                {'name': 'Purchase an NFT', 'completed': False}
            ],
            'progress': 33,
            'deadline': '2023-08-05',
            'snapshot_date': '2023-08-01',
            'estimated_value': 'Medium'
        }
    ]

def render_page():
    st.header("Cryptocurrency Airdrops")
    
    st.markdown("""
    Airdrops are free token distributions by blockchain projects. Track upcoming opportunities,
    manage qualification tasks, and monitor your earnings from completed airdrops.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Upcoming Airdrops", "Active Tasks", "Completed Airdrops"])
    
    with tab1:
        st.subheader("Upcoming Airdrop Opportunities")
        
        # Filters for airdrops
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ["All Categories", "DeFi", "Layer 2", "NFT", "GameFi", "Infrastructure", "DAO", "Privacy", "Social"]
            selected_category = st.selectbox("Category", categories)
        
        with col2:
            difficulties = ["All Difficulties", "Easy", "Medium", "Hard"]
            selected_difficulty = st.selectbox("Difficulty", difficulties)
        
        with col3:
            estimated_values = ["All Values", "Low", "Medium", "High"]
            selected_value = st.selectbox("Estimated Value", estimated_values)
        
        # Get airdrops and filter them
        airdrops = get_upcoming_airdrops()
        filtered_airdrops = airdrops
        
        if selected_category != "All Categories":
            filtered_airdrops = [a for a in filtered_airdrops if a['category'] == selected_category]
        
        if selected_difficulty != "All Difficulties":
            filtered_airdrops = [a for a in filtered_airdrops if a['difficulty'] == selected_difficulty]
        
        if selected_value != "All Values":
            filtered_airdrops = [a for a in filtered_airdrops if a['estimated_value'] == selected_value]
        
        if not filtered_airdrops:
            st.warning("No airdrops match your criteria. Try adjusting the filters.")
        else:
            # Sort by deadline
            filtered_airdrops = sorted(filtered_airdrops, key=lambda x: x['deadline'])
            
            # Display airdrops
            for airdrop in filtered_airdrops:
                with st.expander(f"{airdrop['project']} ({airdrop['token']}) - {airdrop['category']}"):
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.markdown(f"**Requirements:** {airdrop['requirements']}")
                        st.markdown(f"**Deadline:** {airdrop['deadline']}")
                        st.markdown(f"**Snapshot Date:** {airdrop['snapshot_date']}")
                        st.markdown(f"**Difficulty:** {airdrop['difficulty']}")
                        st.markdown(f"**Estimated Value:** {airdrop['estimated_value']}")
                    
                    with col2:
                        # Calculate days remaining
                        deadline = datetime.strptime(airdrop['deadline'], "%Y-%m-%d")
                        days_remaining = (deadline - datetime.now()).days
                        
                        if days_remaining > 0:
                            st.metric("Days Remaining", days_remaining)
                        else:
                            st.metric("Days Remaining", "Expired", delta_color="inverse")
                        
                        # Track button
                        if st.button(f"Track {airdrop['token']} Airdrop", key=f"track_{airdrop['token']}"):
                            st.success(f"Now tracking {airdrop['project']} airdrop. Check Active Tasks tab for details.")
            
            # Timeline visualization
            st.subheader("Upcoming Airdrops Timeline")
            
            # Create dataframe for timeline
            timeline_data = []
            
            for airdrop in filtered_airdrops:
                snapshot_date = datetime.strptime(airdrop['snapshot_date'], "%Y-%m-%d")
                deadline = datetime.strptime(airdrop['deadline'], "%Y-%m-%d")
                
                timeline_data.append({
                    'project': airdrop['project'],
                    'token': airdrop['token'],
                    'start_date': datetime.now(),
                    'end_date': snapshot_date,
                    'stage': 'Qualification Period'
                })
                
                timeline_data.append({
                    'project': airdrop['project'],
                    'token': airdrop['token'],
                    'start_date': snapshot_date,
                    'end_date': deadline,
                    'stage': 'Distribution Period'
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            # Create Gantt chart
            fig = px.timeline(
                timeline_df,
                x_start='start_date',
                x_end='end_date',
                y='project',
                color='stage',
                hover_data=['token'],
                labels={'project': 'Project', 'stage': 'Stage'},
                title='Airdrop Timeline'
            )
            
            fig.update_yaxes(autorange="reversed")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Category breakdown
            st.subheader("Airdrop Categories Breakdown")
            
            # Count airdrops by category
            category_counts = {}
            for airdrop in airdrops:
                category = airdrop['category']
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # Create dataframe for pie chart
            category_df = pd.DataFrame({
                'Category': list(category_counts.keys()),
                'Count': list(category_counts.values())
            })
            
            # Create pie chart
            fig = px.pie(
                category_df,
                values='Count',
                names='Category',
                title='Upcoming Airdrops by Category'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("My Active Airdrop Tasks")
        
        # Get active tasks
        active_tasks = get_active_tasks()
        
        if not active_tasks:
            st.info("You don't have any active airdrop tasks. Start tracking airdrops from the Upcoming Airdrops tab.")
        else:
            # Display active tasks
            for task in active_tasks:
                with st.expander(f"{task['project']} ({task['token']}) - {task['progress']}% Complete", expanded=True):
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.markdown(f"**Category:** {task['category']}")
                        st.markdown(f"**Deadline:** {task['deadline']}")
                        st.markdown(f"**Snapshot Date:** {task['snapshot_date']}")
                        st.markdown(f"**Estimated Value:** {task['estimated_value']}")
                        
                        # Task checklist
                        st.subheader("Tasks")
                        for subtask in task['tasks']:
                            completed = subtask['completed']
                            st.checkbox(subtask['name'], value=completed, key=f"{task['token']}_{subtask['name']}")
                    
                    with col2:
                        # Progress meter
                        st.metric("Progress", f"{task['progress']}%")
                        st.progress(task['progress'] / 100)
                        
                        # Calculate days remaining
                        deadline = datetime.strptime(task['deadline'], "%Y-%m-%d")
                        days_remaining = (deadline - datetime.now()).days
                        
                        if days_remaining > 0:
                            st.metric("Days Remaining", days_remaining)
                        else:
                            st.metric("Days Remaining", "Expired", delta_color="inverse")
                        
                        # Additional actions
                        st.markdown("---")
                        if st.button("Mark All as Complete", key=f"complete_{task['token']}"):
                            st.success(f"All tasks for {task['project']} marked as complete!")
                        
                        if st.button("Remove from Tracking", key=f"remove_{task['token']}"):
                            st.warning(f"{task['project']} removed from tracking.")
            
            # Progress overview
            st.subheader("Airdrop Tasks Progress Overview")
            
            # Create progress data
            progress_data = []
            
            for task in active_tasks:
                progress_data.append({
                    'project': f"{task['project']} ({task['token']})",
                    'progress': task['progress']
                })
            
            progress_df = pd.DataFrame(progress_data)
            
            # Create progress bar chart
            fig = px.bar(
                progress_df,
                x='project',
                y='progress',
                labels={'project': 'Project', 'progress': 'Progress (%)'},
                title='Airdrop Tasks Progress',
                range_y=[0, 100]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Completed Airdrops")
        
        # Get completed airdrops
        completed = get_completed_airdrops()
        
        if not completed:
            st.info("You haven't completed any airdrops yet. Complete tasks from the Active Tasks tab to see them here.")
        else:
            # Summary metrics
            total_received = sum(airdrop['tokens_received'] for airdrop in completed)
            total_value_at_receipt = sum(airdrop['value_at_receipt'] for airdrop in completed)
            total_current_value = sum(airdrop['current_value'] for airdrop in completed)
            value_change = total_current_value - total_value_at_receipt
            value_change_pct = (value_change / total_value_at_receipt) * 100 if total_value_at_receipt > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Tokens Received", total_received)
            
            with col2:
                st.metric("Value at Receipt", f"${total_value_at_receipt:.2f}")
            
            with col3:
                st.metric("Current Value", f"${total_current_value:.2f}", f"{value_change_pct:+.2f}%")
            
            # Display completed airdrops table
            st.markdown("---")
            st.subheader("Airdrop History")
            
            for airdrop in completed:
                with st.expander(f"{airdrop['project']} ({airdrop['token']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Category:** {airdrop['category']}")
                        st.markdown(f"**Completion Date:** {airdrop['completion_date']}")
                        st.markdown(f"**Tokens Received:** {airdrop['tokens_received']} {airdrop['token']}")
                    
                    with col2:
                        value_change = airdrop['current_value'] - airdrop['value_at_receipt']
                        value_change_pct = (value_change / airdrop['value_at_receipt']) * 100 if airdrop['value_at_receipt'] > 0 else 0
                        
                        st.metric("Value at Receipt", f"${airdrop['value_at_receipt']:.2f}")
                        st.metric("Current Value", f"${airdrop['current_value']:.2f}", f"{value_change_pct:+.2f}%")
            
            # Value change visualization
            st.subheader("Airdrop Value Change")
            
            # Create value change dataframe
            value_df = pd.DataFrame(completed)
            
            # Add value change column
            value_df['value_change'] = value_df['current_value'] - value_df['value_at_receipt']
            value_df['value_change_pct'] = value_df.apply(
                lambda x: (x['value_change'] / x['value_at_receipt']) * 100 if x['value_at_receipt'] > 0 else 0,
                axis=1
            )
            
            # Create value change chart
            fig = go.Figure()
            
            # Add receipt value bars
            fig.add_trace(go.Bar(
                x=value_df['project'],
                y=value_df['value_at_receipt'],
                name='Value at Receipt',
                marker_color='lightblue'
            ))
            
            # Add current value bars
            fig.add_trace(go.Bar(
                x=value_df['project'],
                y=value_df['current_value'],
                name='Current Value',
                marker_color='lightgreen'
            ))
            
            fig.update_layout(
                title='Airdrop Value Comparison',
                xaxis_title='Project',
                yaxis_title='USD Value',
                barmode='group',
                legend_title='Value Type'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Value change percentage chart
            fig2 = px.bar(
                value_df.sort_values('value_change_pct', ascending=False),
                x='project',
                y='value_change_pct',
                color='value_change_pct',
                color_continuous_scale='RdYlGn',
                labels={'project': 'Project', 'value_change_pct': 'Value Change (%)'},
                title='Airdrop Value Change Percentage'
            )
            
            fig2.update_layout(coloraxis_colorbar=dict(title='Change (%)'))
            
            st.plotly_chart(fig2, use_container_width=True)
