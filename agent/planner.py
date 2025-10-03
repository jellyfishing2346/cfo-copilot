"""Query interpretation and planning for CFO Copilot."""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime


class QueryPlanner:
    """Interprets user queries and creates execution plans."""
    
    def __init__(self):
        self.month_patterns = {
            'january': 'Jan 2025', 'jan': 'Jan 2025',
            'february': 'Feb 2025', 'feb': 'Feb 2025',
            'march': 'Mar 2025', 'mar': 'Mar 2025',
            'april': 'Apr 2025', 'apr': 'Apr 2025',
            'may': 'May 2025',
            'june': 'Jun 2025', 'jun': 'Jun 2025',
            'july': 'Jul 2025', 'jul': 'Jul 2025',
            'august': 'Aug 2025', 'aug': 'Aug 2025',
            'september': 'Sep 2025', 'sep': 'Sep 2025',
            'october': 'Oct 2025', 'oct': 'Oct 2025',
            'november': 'Nov 2025', 'nov': 'Nov 2025',
            'december': 'Dec 2025', 'dec': 'Dec 2025'
        }
        
        self.intent_patterns = {
            'revenue_vs_budget': [
                r'revenue.*vs.*budget',
                r'revenue.*budget',
                r'actual.*budget.*revenue',
                r'budget.*revenue'
            ],
            'gross_margin_trend': [
                r'gross\s+margin.*trend',
                r'margin.*trend',
                r'gross\s+margin.*last.*months?',
                r'margin.*last.*months?'
            ],
            'opex_breakdown': [
                r'opex.*breakdown',
                r'opex.*category',
                r'operating.*expense.*breakdown',
                r'break.*down.*opex'
            ],
            'ebitda': [
                r'ebitda',
                r'earnings.*before',
                r'operating.*profit'
            ],
            'cash_runway': [
                r'cash.*runway',
                r'runway',
                r'cash.*burn',
                r'how.*long.*cash'
            ]
        }
    
    def extract_month(self, query: str) -> Optional[str]:
        """Extract month from query."""
        query_lower = query.lower()
        
        for pattern, month in self.month_patterns.items():
            if pattern in query_lower:
                return month
        
        # Default to current month if not specified
        return 'Jun 2025'  # Using June as default for demo
    
    def extract_months_range(self, query: str) -> List[str]:
        """Extract range of months from query."""
        query_lower = query.lower()
        
        # Look for "last X months" pattern
        last_months_match = re.search(r'last\s+(\d+)\s+months?', query_lower)
        if last_months_match:
            num_months = int(last_months_match.group(1))
            # Return last N months ending at June 2025
            all_months = [
                'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025',
                'May 2025', 'Jun 2025', 'Jul 2025', 'Aug 2025',
                'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025'
            ]
            june_index = all_months.index('Jun 2025')
            start_index = max(0, june_index - num_months + 1)
            return all_months[start_index:june_index + 1]
        
        # Look for specific month mentioned
        month = self.extract_month(query)
        if month:
            return [month]
        
        # Default to last 3 months
        return ['Apr 2025', 'May 2025', 'Jun 2025']
    
    def classify_intent(self, query: str) -> str:
        """Classify the intent of the user query."""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        # Default to revenue analysis if unclear
        return 'revenue_vs_budget'
    
    def create_plan(self, query: str) -> Dict[str, Any]:
        """Create an execution plan for the query."""
        intent = self.classify_intent(query)
        month = self.extract_month(query)
        months_range = self.extract_months_range(query)
        
        plan = {
            'query': query,
            'intent': intent,
            'month': month,
            'months_range': months_range,
            'requires_chart': True,
            'function_calls': []
        }
        
        # Define function calls based on intent
        if intent == 'revenue_vs_budget':
            plan['function_calls'] = [
                {
                    'function': 'get_revenue_vs_budget',
                    'params': {'month': month}
                }
            ]
            plan['chart_type'] = 'bar'
            
        elif intent == 'gross_margin_trend':
            plan['function_calls'] = [
                {
                    'function': 'get_gross_margin_trend', 
                    'params': {'months': months_range}
                }
            ]
            plan['chart_type'] = 'line'
            
        elif intent == 'opex_breakdown':
            plan['function_calls'] = [
                {
                    'function': 'get_opex_breakdown',
                    'params': {'month': month}
                }
            ]
            plan['chart_type'] = 'pie'
            
        elif intent == 'ebitda':
            plan['function_calls'] = [
                {
                    'function': 'calculate_ebitda',
                    'params': {'month': month}
                }
            ]
            plan['chart_type'] = 'metric'
            
        elif intent == 'cash_runway':
            plan['function_calls'] = [
                {
                    'function': 'calculate_cash_runway',
                    'params': {}
                }
            ]
            plan['chart_type'] = 'runway'
        
        return plan
    
    def format_response(self, plan: Dict[str, Any], results: List[Any]) -> str:
        """Format the analysis results into a board-ready response."""
        intent = plan['intent']
        
        if intent == 'revenue_vs_budget' and results:
            result = results[0]
            response = f"""**Revenue Performance - {result['month']}**

• **Actual Revenue**: ${result['actual']:,.0f}
• **Budgeted Revenue**: ${result['budget']:,.0f}  
• **Variance**: ${result['variance']:+,.0f} ({result['variance_pct']:+.1f}%)

{'🟢 **Above budget**' if result['variance'] > 0 else '🔴 **Below budget**' if result['variance'] < 0 else '🟡 **On budget**'}
"""
            
        elif intent == 'gross_margin_trend' and results:
            # Handle both single list and list of results
            trend_data = results[0] if isinstance(results[0], list) else results
            
            month_breakdown = "\n".join([
                f"• **{item['month']}**: {item['gross_margin_pct']:.1f}% (${item['gross_profit']:,.0f} gross profit)"
                for item in trend_data
            ])
            
            # Determine trend direction
            if len(trend_data) > 1:
                first_margin = trend_data[0]['gross_margin_pct']
                last_margin = trend_data[-1]['gross_margin_pct']
                if last_margin > first_margin:
                    trend_insight = "📈 **Steady improvement** - margin expanding consistently"
                elif last_margin < first_margin:
                    trend_insight = "📉 **Margin decline** - requires attention"
                else:
                    trend_insight = "📊 **Stable margins** - consistent performance"
            else:
                trend_insight = "📊 **Current performance** - single month view"
            
            response = f"""**Gross Margin Trend - Last {len(trend_data)} Months**

{month_breakdown}

{trend_insight}"""
            
        elif intent == 'opex_breakdown' and results:
            result = results[0]
            breakdown_text = "\n".join([f"• **{cat}**: ${amt:,.0f}" for cat, amt in result['breakdown'].items()])
            
            response = f"""**OPEX Breakdown - {result['month']}**

{breakdown_text}

• **Total OPEX**: ${result['total']:,.0f}
"""
            
        elif intent == 'ebitda' and results:
            result = results[0]
            response = f"""**EBITDA Analysis - {result['month']}**

• **Revenue**: ${result['revenue']:,.0f}
• **COGS**: ${result['cogs']:,.0f}
• **OPEX**: ${result['opex']:,.0f}
• **EBITDA**: ${result['ebitda']:,.0f}
• **EBITDA Margin**: {result['ebitda_margin']:.1f}%

{'🟢 **Strong profitability**' if result['ebitda_margin'] > 20 else '🟡 **Moderate profitability**' if result['ebitda_margin'] > 10 else '🔴 **Low profitability**'}
"""
            
        elif intent == 'cash_runway' and results:
            result = results[0]
            runway_text = f"{result['runway_months']:.1f} months" if result['runway_months'] != float('inf') else "∞ (positive cash flow)"
            
            response = f"""**Cash Runway Analysis**

• **Current Cash**: ${result['current_cash_usd']:,.0f}
• **Avg Monthly Burn**: ${result['avg_monthly_burn_usd']:,.0f}
• **Estimated Runway**: {runway_text}

{'🟢 **Healthy cash position**' if result['runway_months'] > 12 else '🟡 **Moderate runway**' if result['runway_months'] > 6 else '🔴 **Low runway - action needed**'}
"""
        else:
            response = "I couldn't analyze that request. Please try asking about revenue, margins, expenses, or cash runway."
        
        return response


# Global planner instance
_planner = None

def get_planner() -> QueryPlanner:
    """Get the global query planner instance."""
    global _planner
    if _planner is None:
        _planner = QueryPlanner()
    return _planner
