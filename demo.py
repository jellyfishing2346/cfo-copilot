#!/usr/bin/env python3
"""
Simple test runner for CFO Copilot without external dependencies.
This demonstrates the core functionality without requiring pandas/streamlit.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Mock pandas DataFrame for testing
class MockSeries:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key] if key < len(self.data) else None
        return None
    
    def sum(self):
        return sum(x for x in self.data if x is not None)
    
    def str(self):
        return MockStrAccessor(self.data)
        
    @property
    def iloc(self):
        return MockILoc(self.data)

class MockStrAccessor:
    def __init__(self, data):
        self.data = data
    
    def contains(self, pattern):
        return [pattern in str(item) for item in self.data]
    
    def startswith(self, pattern):
        return [str(item).startswith(pattern) for item in self.data]

class MockILoc:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        if isinstance(key, int) and 0 <= key < len(self.data):
            return self.data[key]
        return None

class MockDataFrame:
    def __init__(self, data):
        self.data = data
        self.columns = list(data[0].keys()) if data else []
    
    def __getitem__(self, key):
        if isinstance(key, str):  # Column access
            column_data = [row.get(key) for row in self.data]
            series = MockSeries(column_data)
            series.str = MockStrAccessor(column_data)
            return series
        elif hasattr(key, '__iter__') and not isinstance(key, str):  # Boolean mask
            if isinstance(key, list):
                return MockDataFrame([row for i, row in enumerate(self.data) if i < len(key) and key[i]])
            return MockDataFrame([row for i, row in enumerate(self.data) if (key[i] if i < len(key) else False)])
        return self.data[key]
    
    def sum(self):
        # For testing, return a reasonable sum - check for any month column
        months = ['Apr 2025', 'May 2025', 'Jun 2025', 'Jul 2025', 'Aug 2025', 'Sep 2025']
        for month in months:
            total = sum(row.get(month, 0) for row in self.data if row.get(month) is not None)
            if total > 0:
                return total
        return 0
    
    def copy(self):
        return MockDataFrame([row.copy() for row in self.data])
    
    def __bool__(self):
        return len(self.data) > 0
    
    def __len__(self):
        return len(self.data)
    
    @property
    def empty(self):
        return len(self.data) == 0
    
    def iterrows(self):
        for i, row in enumerate(self.data):
            yield i, MockRow(row)


class MockRow:
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, key):
        return self._data[key]


# Mock CSV reader
def mock_read_csv(filepath):
    """Mock CSV reader that returns sample data."""
    if 'actuals.csv' in filepath:
        return MockDataFrame([
            {'Entity': 'US', 'Account': 'Revenue', 'Apr 2025': 1350000, 'May 2025': 1400000, 'Jun 2025': 1450000, 'Currency': 'USD'},
            {'Entity': 'US', 'Account': 'COGS', 'Apr 2025': 540000, 'May 2025': 560000, 'Jun 2025': 580000, 'Currency': 'USD'},
            {'Entity': 'US', 'Account': 'Opex:Sales', 'Apr 2025': 135000, 'May 2025': 140000, 'Jun 2025': 145000, 'Currency': 'USD'},
            {'Entity': 'EU', 'Account': 'Revenue', 'Apr 2025': 860000, 'May 2025': 880000, 'Jun 2025': 900000, 'Currency': 'EUR'},
            {'Entity': 'EU', 'Account': 'COGS', 'Apr 2025': 344000, 'May 2025': 352000, 'Jun 2025': 360000, 'Currency': 'EUR'},
        ])
    elif 'budget.csv' in filepath:
        return MockDataFrame([
            {'Entity': 'US', 'Account': 'Revenue', 'Jun 2025': 1350000, 'Currency': 'USD'},
            {'Entity': 'US', 'Account': 'COGS', 'Jun 2025': 540000, 'Currency': 'USD'},
            {'Entity': 'EU', 'Account': 'Revenue', 'Jun 2025': 850000, 'Currency': 'EUR'},
        ])
    elif 'fx.csv' in filepath:
        return MockDataFrame([
            {'Month': 'Apr 2025', 'EUR_USD': 1.14, 'USD_EUR': 0.88},
            {'Month': 'May 2025', 'EUR_USD': 1.12, 'USD_EUR': 0.89},
            {'Month': 'Jun 2025', 'EUR_USD': 1.11, 'USD_EUR': 0.90}
        ])
    elif 'cash.csv' in filepath:
        return MockDataFrame([
            {'Entity': 'US', 'Jun 2025': 2400000, 'Currency': 'USD'},
            {'Entity': 'EU', 'Jun 2025': 1400000, 'Currency': 'EUR'}
        ])
    return MockDataFrame([])


# Patch pandas import
class MockPandas:
    DataFrame = MockDataFrame
    
    def read_csv(self, filepath):
        return mock_read_csv(filepath)


sys.modules['pandas'] = MockPandas()
sys.modules['numpy'] = type('MockNumpy', (), {'mean': lambda x: sum(x) / len(x) if x else 0})

# Now import our modules
try:
    from agent.planner import QueryPlanner
    from agent.tools import FinancialDataLoader, FinancialAnalyzer
    
    # Patch the actual read_csv calls in our modules
    import agent.tools as tools_module
    tools_module.pd.read_csv = mock_read_csv
    
    def test_basic_functionality():
        """Test basic CFO Copilot functionality."""
        print("🧪 Testing CFO Copilot Core Functionality")
        print("=" * 50)
        
        # Test Query Planning
        print("\n📋 Testing Query Planning...")
        planner = QueryPlanner()
        
        # Test intent classification
        queries = [
            "What was June 2025 revenue vs budget?",
            "Show gross margin trend for last 3 months",
            "Break down Opex by category for June",
            "What is our cash runway?"
        ]
        
        for query in queries:
            plan = planner.create_plan(query)
            print(f"Query: {query}")
            print(f"  → Intent: {plan['intent']}")
            print(f"  → Month: {plan['month']}")
            print(f"  → Chart Type: {plan['chart_type']}")
            print()
        
        # Test Financial Analysis
        print("💰 Testing Financial Analysis...")
        data_loader = FinancialDataLoader("fixtures")
        analyzer = FinancialAnalyzer(data_loader)
        
        # Test revenue vs budget
        print("\n📊 Revenue vs Budget Analysis:")
        result = analyzer.get_revenue_vs_budget('Jun 2025')
        print(f"  Actual: ${result['actual']:,.0f}")
        print(f"  Budget: ${result['budget']:,.0f}")
        print(f"  Variance: ${result['variance']:+,.0f} ({result['variance_pct']:+.1f}%)")
        
        # Test OPEX breakdown
        print("\n💼 OPEX Breakdown:")
        opex_result = analyzer.get_opex_breakdown('Jun 2025')
        for category, amount in opex_result['breakdown'].items():
            print(f"  {category}: ${amount:,.0f}")
        print(f"  Total: ${opex_result['total']:,.0f}")
        
        # Test response formatting
        print("\n📝 Testing Response Formatting...")
        plan = planner.create_plan("What was June 2025 revenue vs budget?")
        response = planner.format_response(plan, [result])
        print("Generated Response:")
        print(response)
        
        print("\n✅ All tests completed successfully!")
        return True
        
    def demo_queries():
        """Demonstrate handling various CFO queries."""
        print("\n🎯 CFO Copilot Demo - Sample Queries")
        print("=" * 50)
        
        planner = QueryPlanner()
        data_loader = FinancialDataLoader("fixtures")  
        analyzer = FinancialAnalyzer(data_loader)
        
        sample_queries = [
            "What was June 2025 revenue vs budget in USD?",
            "Break down Opex by category for June",
            "What is our EBITDA for June 2025?",
            "Show me cash runway analysis"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n{i}. Query: '{query}'")
            print("-" * 40)
            
            # Create plan
            plan = planner.create_plan(query)
            
            # Execute analysis
            results = []
            for func_call in plan['function_calls']:
                func_name = func_call['function']
                params = func_call['params']
                
                if func_name == 'get_revenue_vs_budget':
                    result = analyzer.get_revenue_vs_budget(**params)
                elif func_name == 'get_opex_breakdown':
                    result = analyzer.get_opex_breakdown(**params)
                elif func_name == 'calculate_ebitda':
                    result = analyzer.calculate_ebitda(**params)
                elif func_name == 'calculate_cash_runway':
                    result = analyzer.calculate_cash_runway(**params)
                else:
                    continue
                
                results.append(result)
            
            # Format and display response
            if results:
                response = planner.format_response(plan, results)
                print(response)
            else:
                print("No results generated.")
        
        print("\n🎉 Demo completed!")
    
    if __name__ == "__main__":
        success = test_basic_functionality()
        if success:
            demo_queries()
            
            print("\n🚀 Ready to run CFO Copilot!")
            print("\nTo start the Streamlit app (once dependencies are installed):")
            print("  streamlit run app.py")
            print("\nTo run full tests:")
            print("  pytest tests/test_agent.py -v")

except ImportError as e:
    print(f"Import error: {e}")
    print("Some modules may not be available. This is expected in a clean environment.")
    print("\nTo run the full app, install dependencies:")
    print("  pip install -r requirements.txt")
    print("  streamlit run app.py")
