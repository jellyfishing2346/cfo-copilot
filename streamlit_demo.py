#!/usr/bin/env python3
"""
Streamlit App Demo for CFO Copilot - Shows how the error handling works
"""

import streamlit as st
import sys
import os

# Set page config
st.set_page_config(
    page_title="CFO Copilot", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def demo_streamlit_interface():
    """Demo the Streamlit interface without backend."""
    
    st.title("📊 CFO Copilot")
    st.markdown("*AI-powered financial analysis assistant*")
    
    # Sample Questions Sidebar
    with st.sidebar:
        st.header("💡 Sample Questions")
        st.write("Try asking:")
        sample_questions = [
            "What was June 2025 revenue vs budget?",
            "Show gross margin trend for last 3 months",
            "Break down Opex by category for June",
            "What is our EBITDA for June 2025?",
            "What is our cash runway right now?"
        ]
        
        for q in sample_questions:
            if st.button(f'"{q}"', key=q):
                st.session_state.selected_question = q
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your CFO Copilot. I can help you analyze financial data and answer questions about revenue, margins, expenses, and cash flow. What would you like to know?"
            }
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle selected question from sidebar
    if hasattr(st.session_state, 'selected_question'):
        prompt = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        prompt = st.chat_input("Ask me about your financial data...")
    
    # Process user input
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                response = get_demo_response(prompt)
                st.markdown(response['text'])
                
                # Show chart if applicable
                if response.get('chart'):
                    st.plotly_chart(response['chart'], use_container_width=True)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['text']
                })

def get_demo_response(query: str) -> dict:
    """Generate demo responses for different query types."""
    
    import plotly.graph_objects as go
    import plotly.express as px
    
    query_lower = query.lower()
    
    # Revenue vs Budget
    if 'revenue' in query_lower and 'budget' in query_lower:
        return {
            'text': """**Revenue Performance - Jun 2025**

• **Actual Revenue**: $2,449,000
• **Budgeted Revenue**: $2,293,500
• **Variance**: +$155,500 (+6.8%)

🟢 **Above budget** - performing well""",
            'chart': create_revenue_chart()
        }
    
    # Gross Margin Trend
    elif 'gross margin' in query_lower and ('trend' in query_lower or 'months' in query_lower):
        return {
            'text': """**Gross Margin Trend - Last 3 Months**

• **Apr 2025**: 58.1% ($1,325K gross profit)
• **May 2025**: 58.2% ($1,347K gross profit) 
• **Jun 2025**: 58.3% ($1,370K gross profit)

📈 **Steady improvement** - margin expanding consistently""",
            'chart': create_margin_chart()
        }
    
    # OPEX Breakdown
    elif 'opex' in query_lower or 'expense' in query_lower:
        return {
            'text': """**Operating Expenses Breakdown - Jun 2025**

• **Engineering**: $369,300 (40.8%)
• **Sales**: $244,900 (27.0%) 
• **Marketing**: $171,600 (18.9%)
• **General**: $119,900 (13.2%)
• **Total OPEX**: $905,700

💡 **Engineering** is the largest expense category""",
            'chart': create_opex_chart()
        }
    
    # EBITDA
    elif 'ebitda' in query_lower:
        return {
            'text': """**EBITDA Analysis - Jun 2025**

• **Revenue**: $2,449,000
• **COGS**: $979,800
• **OPEX**: $905,700
• **EBITDA**: $563,500
• **EBITDA Margin**: 23.0%

🎯 **Strong profitability** - healthy margin above 20%""",
            'chart': create_ebitda_chart()
        }
    
    # Cash Runway  
    elif 'cash' in query_lower or 'runway' in query_lower:
        return {
            'text': """**Cash Runway Analysis**

• **Current Cash**: $3,954,000
• **Avg Monthly Burn**: $85,000
• **Estimated Runway**: 46.5 months

🟢 **Excellent position** - very comfortable runway""",
            'chart': create_cash_chart()
        }
    
    # Default response
    else:
        return {
            'text': """I can help you analyze financial data! Try asking:

• "What was June 2025 revenue vs budget?"
• "Show gross margin trend for last 3 months"  
• "Break down OPEX by category"
• "What is our EBITDA?"
• "What is our cash runway?"

Click the sample questions in the sidebar to get started! 📊"""
        }

def create_revenue_chart():
    """Create revenue vs budget chart."""
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Actual',
        x=['Revenue'],
        y=[2449000],
        marker_color='#2E86AB'
    ))
    
    fig.add_trace(go.Bar(
        name='Budget',
        x=['Revenue'], 
        y=[2293500],
        marker_color='#A23B72'
    ))
    
    fig.update_layout(
        title="Revenue vs Budget - Jun 2025",
        yaxis_title="USD",
        barmode='group',
        height=400
    )
    
    return fig

def create_margin_chart():
    """Create gross margin trend chart."""
    import plotly.graph_objects as go
    
    months = ['Apr 2025', 'May 2025', 'Jun 2025']
    margins = [58.1, 58.2, 58.3]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=margins,
        mode='lines+markers',
        name='Gross Margin %',
        line=dict(color='#F18F01', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Gross Margin Trend",
        xaxis_title="Month",
        yaxis_title="Gross Margin %",
        height=400
    )
    
    return fig

def create_opex_chart():
    """Create OPEX breakdown pie chart."""
    import plotly.graph_objects as go
    
    categories = ['Engineering', 'Sales', 'Marketing', 'General']
    values = [369300, 244900, 171600, 119900]
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.3,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="OPEX Breakdown - Jun 2025",
        height=400
    )
    
    return fig

def create_ebitda_chart():
    """Create EBITDA waterfall chart."""
    import plotly.graph_objects as go
    
    categories = ['Revenue', 'COGS', 'OPEX', 'EBITDA']
    values = [2449000, -979800, -905700, 563500]
    
    fig = go.Figure(go.Waterfall(
        name="EBITDA Calculation",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"${v/1000:.0f}K" for v in values],
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="EBITDA Breakdown - Jun 2025",
        height=400
    )
    
    return fig

def create_cash_chart():
    """Create cash runway visualization."""
    import plotly.graph_objects as go
    
    months = ['Current', 'In 12 months', 'In 24 months', 'In 36 months']
    cash_levels = [3954000, 2934000, 1914000, 894000]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cash_levels,
        mode='lines+markers',
        name='Cash Balance',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Cash Runway Projection",
        xaxis_title="Timeline",
        yaxis_title="Cash Balance (USD)",
        height=400
    )
    
    return fig

if __name__ == "__main__":
    demo_streamlit_interface()
