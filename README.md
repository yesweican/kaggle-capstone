# Project Structure for MarketReportAgent
"""
market_report_agent/
│
├── main.py                          # Entry point with Runner
├── requirements.txt                 # Dependencies
├── pyproject.toml                   # Project configuration & Python version
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
│
├── market_report_agent/
│   ├── __init__.py
│   ├── agent.py                    # Root agent definition
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── portfolio_tools.py      # add/delete/list ticker functions
│   │   └── report_tools.py         # generate_report function
│   │
│   └── sub_agents/
│       ├── __init__.py
│       │
│       ├── price_update_agent/
│       │   ├── __init__.py
│       │   └── agent.py            # PriceUpdateAgent
│       │
│       ├── sector_performance_agent/
│       │   ├── __init__.py
│       │   └── agent.py            # SectorPerformanceAgent
│       │
│       └── market_news_agent/
│           ├── __init__.py
│           └── agent.py            # MarketNewsAgent
│
├── utils/
│   ├── __init__.py
│   └── constants.py                # GICS sectors, etc.
│
├── data/
│   └── sessions.db                 # SQLite database for sessions
│
└── deploy/
    ├── __init__.py
    ├── README.md                   # Deployment instructions
    ├── agent_engine_config.yaml    # Agent Engine configuration
    └── deploy.py                   # Deployment script
"""

### Prerequisite #1 - Python Version preferred 3.12

python --version

### Prerequisite #2 - Setup Virtual Environment

python -m venv .venv

### Prerequisite #3 - Activate virtual environment

.venv\scripts\activate

### Prerequisite #4 - Install Dependencies

pip install -r requirements.txt

### Running the Agent

To run the martket_report_agent:

```bash

python main.py

```
