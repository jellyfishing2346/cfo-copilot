"""Tests for CFO Copilot agent functionality."""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.planner import QueryPlanner
from agent.tools import FinancialDataLoader, FinancialAnalyzer


class TestQueryPlanner:
    """Test cases for the QueryPlanner class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.planner = QueryPlanner()
    
    def test_extract_month(self):
        """Test month extraction from queries."""
        # Test explicit month mentions
        assert self.planner.extract_month("What was June revenue?") == "Jun 2025"
        assert self.planner.extract_month("Show me May data") == "May 2025"
        assert self.planner.extract_month("February results") == "Feb 2025"
        
        # Test default behavior
        assert self.planner.extract_month("Show revenue") == "Jun 2025"
    
    def test_classify_intent(self):
        """Test intent classification."""
        # Revenue vs budget
        assert self.planner.classify_intent("What was June revenue vs budget?") == "revenue_vs_budget"
        assert self.planner.classify_intent("revenue budget comparison") == "revenue_vs_budget"
        
        # Gross margin trend
        assert self.planner.classify_intent("Show gross margin trend") == "gross_margin_trend"
        assert self.planner.classify_intent("margin trend last 3 months") == "gross_margin_trend"
        
        # OPEX breakdown
        assert self.planner.classify_intent("Break down opex by category") == "opex_breakdown"
        assert self.planner.classify_intent("opex breakdown june") == "opex_breakdown"
        
        # EBITDA
        assert self.planner.classify_intent("What is our EBITDA?") == "ebitda"
        assert self.planner.classify_intent("show ebitda") == "ebitda"
        
        # Cash runway
        assert self.planner.classify_intent("What is our cash runway?") == "cash_runway"
        assert self.planner.classify_intent("cash runway analysis") == "cash_runway"
    
    def test_create_plan(self):
        """Test plan creation."""
        # Test revenue vs budget plan
        plan = self.planner.create_plan("What was June 2025 revenue vs budget?")
        assert plan['intent'] == 'revenue_vs_budget'
        assert plan['month'] == 'Jun 2025'
        assert len(plan['function_calls']) == 1
        assert plan['function_calls'][0]['function'] == 'get_revenue_vs_budget'
        
        # Test gross margin trend plan
        plan = self.planner.create_plan("Show gross margin trend last 3 months")
        assert plan['intent'] == 'gross_margin_trend'
        assert plan['chart_type'] == 'line'
        assert len(plan['months_range']) >= 3


class TestFinancialAnalyzer:
    """Test cases for the FinancialAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.data_loader = FinancialDataLoader("fixtures")
        self.analyzer = FinancialAnalyzer(self.data_loader)
    
    def test_data_loading(self):
        """Test that data files load correctly."""
        # Test actuals data
        actuals = self.data_loader.load_actuals()
        assert not actuals.empty
        assert 'Entity' in actuals.columns
        assert 'Account' in actuals.columns
        assert 'Jun 2025' in actuals.columns
        
        # Test budget data  
        budget = self.data_loader.load_budget()
        assert not budget.empty
        assert 'Entity' in budget.columns
        
        # Test FX data
        fx = self.data_loader.load_fx()
        assert not fx.empty
        assert 'Month' in fx.columns
        
        # Test cash data
        cash = self.data_loader.load_cash()
        assert not cash.empty
        assert 'Entity' in cash.columns
    
    def test_revenue_vs_budget(self):
        """Test revenue vs budget calculation."""
        result = self.analyzer.get_revenue_vs_budget('Jun 2025')
        
        assert 'actual' in result
        assert 'budget' in result
        assert 'variance' in result
        assert 'variance_pct' in result
        assert result['month'] == 'Jun 2025'
        
        # Check that numbers are reasonable
        assert result['actual'] > 0
        assert result['budget'] > 0
    
    def test_gross_margin_trend(self):
        """Test gross margin calculation."""
        months = ['Apr 2025', 'May 2025', 'Jun 2025']
        results = self.analyzer.get_gross_margin_trend(months)
        
        assert len(results) == 3
        for result in results:
            assert 'month' in result
            assert 'revenue' in result
            assert 'cogs' in result
            assert 'gross_margin_pct' in result
            
            # Check that margin percentage is calculated correctly
            expected_margin = ((result['revenue'] - result['cogs']) / result['revenue'] * 100)
            assert abs(result['gross_margin_pct'] - expected_margin) < 0.01
    
    def test_opex_breakdown(self):
        """Test OPEX breakdown calculation."""
        result = self.analyzer.get_opex_breakdown('Jun 2025')
        
        assert 'breakdown' in result
        assert 'total' in result
        assert 'month' in result
        
        # Check that breakdown contains expected categories
        breakdown = result['breakdown']
        expected_categories = ['Sales', 'Marketing', 'Engineering', 'General']
        for category in expected_categories:
            assert category in breakdown
            assert breakdown[category] > 0
        
        # Check that total equals sum of breakdown
        calculated_total = sum(breakdown.values())
        assert abs(result['total'] - calculated_total) < 1  # Allow for rounding
    
    def test_ebitda_calculation(self):
        """Test EBITDA calculation."""
        result = self.analyzer.calculate_ebitda('Jun 2025')
        
        assert 'revenue' in result
        assert 'cogs' in result
        assert 'opex' in result
        assert 'ebitda' in result
        assert 'ebitda_margin' in result
        
        # Check calculation
        expected_ebitda = result['revenue'] - result['cogs'] - result['opex']
        assert abs(result['ebitda'] - expected_ebitda) < 1
        
        # Check margin calculation
        expected_margin = (result['ebitda'] / result['revenue'] * 100)
        assert abs(result['ebitda_margin'] - expected_margin) < 0.01
    
    def test_cash_runway(self):
        """Test cash runway calculation."""
        result = self.analyzer.calculate_cash_runway()
        
        assert 'current_cash_usd' in result
        assert 'avg_monthly_burn_usd' in result
        assert 'runway_months' in result
        assert 'cash_balances' in result
        
        # Check that calculations are reasonable
        assert result['current_cash_usd'] > 0
        assert isinstance(result['runway_months'], (int, float))


def test_integration():
    """Test integration between planner and analyzer."""
    planner = QueryPlanner()
    data_loader = FinancialDataLoader("fixtures")
    analyzer = FinancialAnalyzer(data_loader)
    
    # Test a complete workflow
    query = "What was June 2025 revenue vs budget?"
    plan = planner.create_plan(query)
    
    # Execute the plan (simplified)
    if plan['function_calls']:
        func_call = plan['function_calls'][0]
        if func_call['function'] == 'get_revenue_vs_budget':
            result = analyzer.get_revenue_vs_budget(**func_call['params'])
            
            # Format response
            response = planner.format_response(plan, [result])
            
            # Check that response contains key information
            assert 'Revenue Performance' in response
            assert 'Actual Revenue' in response
            assert 'Budgeted Revenue' in response
            assert 'Variance' in response


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
