# CFO Copilot - Demo Video Script

## 30-60 Second Demo Video Script

### Setup (5 seconds)
- **Screen**: Show project structure in VS Code
- **Narration**: "I built a CFO Copilot that answers financial questions from CSV data using AI."

### Question 1 (15 seconds) 
- **Action**: Type "What was June 2025 revenue vs budget?"
- **Screen**: Show response with actual vs budget numbers and variance
- **Narration**: "Ask natural language questions about revenue performance..."

### Question 2 (15 seconds)
- **Action**: Type "Break down OPEX by category for June"  
- **Screen**: Show pie chart with OPEX breakdown by Sales, Marketing, Engineering, General
- **Narration**: "Get detailed expense breakdowns with automatic charts..."

### Question 3 (10 seconds)
- **Action**: Type "What is our cash runway?"
- **Screen**: Show cash runway calculation with burn rate
- **Narration**: "Calculate critical metrics like cash runway instantly..."

### Tests (10 seconds)
- **Action**: Run `python run_tests.py` 
- **Screen**: Show "ALL TESTS PASSED!" message
- **Narration**: "All tests pass - query planning, data processing, and financial calculations work perfectly."

### Closing (5 seconds)
- **Screen**: Show GitHub repo or deployed app
- **Narration**: "Ready for production - built in under 3 hours!"

## Key Features to Highlight

1. **Natural Language Processing**: Converts CFO questions into structured queries
2. **Multi-Entity Analysis**: Handles US and EU data with currency conversion  
3. **Key Financial Metrics**: Revenue vs Budget, Gross Margin, OPEX, EBITDA, Cash Runway
4. **Interactive Charts**: Bar charts, pie charts, line graphs using Plotly
5. **Agent Architecture**: Modular planner + tools design
6. **Board-Ready Output**: Professional formatting with insights

## Technical Architecture

### Agent Components
- **Planner** (`agent/planner.py`): Intent classification and query planning
- **Tools** (`agent/tools.py`): Financial data processing and calculations
- **App** (`app.py`): Streamlit interface with chat and charts

### Data Processing
- **CSV Loading**: Actuals, Budget, FX rates, Cash balances
- **Currency Conversion**: EUR to USD using monthly FX rates
- **Metric Calculation**: Automated variance analysis and KPI computation

### Sample Questions Supported
- "What was June 2025 revenue vs budget in USD?"
- "Show Gross Margin % trend for the last 3 months"
- "Break down Opex by category for June" 
- "What is our cash runway right now?"
- "What is our EBITDA for June 2025?"

## Repository Structure
```
cfo-copilot/
├── README.md              # Complete setup instructions
├── app.py                 # Main Streamlit application  
├── requirements.txt       # Python dependencies
├── agent/
│   ├── __init__.py
│   ├── planner.py        # Query interpretation & planning
│   └── tools.py          # Data analysis functions
├── fixtures/
│   ├── actuals.csv       # Monthly actuals by entity/account
│   ├── budget.csv        # Monthly budget by entity/account
│   ├── fx.csv           # Currency exchange rates
│   └── cash.csv         # Monthly cash balances
├── tests/
│   ├── __init__.py
│   ├── test_agent.py     # Comprehensive test suite
│   └── run_tests.py      # Simple test runner
├── demo.py               # Full feature demo
└── simple_demo.py        # Working demo without dependencies
```

## Deployment Options
- **Local**: `streamlit run app.py`
- **Streamlit Cloud**: Connect GitHub repo for instant deployment
- **Hugging Face Spaces**: Upload as Streamlit Space
- **Docker**: Containerized deployment ready

## Next Steps / Extensions
- **PDF Export**: Generate executive summaries  
- **Real-time Data**: Connect to ERP/accounting systems
- **Advanced Analytics**: Forecasting and trend analysis
- **Multi-company**: Support for multiple business entities
- **Custom Metrics**: User-defined KPIs and calculations
