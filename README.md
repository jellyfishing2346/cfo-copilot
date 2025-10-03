# CFO Copilot

An AI-powered assistant that helps CFOs analyze financial data and answer questions about monthly performance, budget variance, and key financial metrics.

## Features

- **Interactive Chat Interface**: Ask natural language questions about financial data
- **Real-time Data Analysis**: Analyze revenue, expenses, cash flow, and margins
- **Visual Charts**: Automatic chart generation for trends and comparisons
- **Key Metrics**: Revenue vs Budget, Gross Margin %, OPEX breakdown, EBITDA, Cash Runway
- **Export Functionality**: Generate PDF reports (optional)

## Sample Questions

- "What was June 2025 revenue vs budget in USD?"
- "Show Gross Margin % trend for the last 3 months"
- "Break down Opex by category for June"
- "What is our cash runway right now?"

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd cfo-copilot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

```
cfo-copilot/
├── README.md
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── agent/
│   ├── __init__.py
│   ├── planner.py        # Query interpretation and planning
│   └── tools.py          # Data analysis functions
├── fixtures/
│   ├── actuals.csv       # Monthly actuals data
│   ├── budget.csv        # Monthly budget data
│   ├── fx.csv           # Currency exchange rates
│   └── cash.csv         # Monthly cash balances
└── tests/
    ├── __init__.py
    └── test_agent.py     # Unit tests
```

## Data Sources

The app analyzes financial data from CSV files:

- **actuals.csv**: Monthly actual financial data by entity/account
- **budget.csv**: Monthly budget data by entity/account  
- **fx.csv**: Currency exchange rates for USD conversion
- **cash.csv**: Monthly cash balances

## Key Metrics Calculated

1. **Revenue (USD)**: Actual vs Budget comparison
2. **Gross Margin %**: (Revenue - COGS) / Revenue
3. **OPEX Total**: Grouped by operational expense categories
4. **EBITDA**: Revenue - COGS - OPEX (proxy calculation)
5. **Cash Runway**: Cash ÷ Average monthly net burn (last 3 months)

## Testing

Run the test suite:
```bash
pytest tests/
```

## Demo

[Link to demo video - 30-60 seconds showing key functionality]

## Deployment

The app can be deployed to:
- Streamlit Cloud
- Hugging Face Spaces
- Any platform supporting Python web apps

## Contributing

This is a coding assignment project demonstrating AI agent design, data analysis, and UX integration for financial reporting automation.
