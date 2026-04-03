# Fetch Works

[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-purple)](https://fetch.ai)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)

A collection of example uAgents demonstrating core Fetch.ai capabilities — from basic agent creation and inter-agent communication to gas price monitoring, token transfers, and vehicle detail retrieval.

## Examples

### 1. Basic Agent (`agent.py`)

A simple agent that maintains a persistent counter using `ctx.storage`, logging the count on a 1-second interval.

```python
python agent.py
```

### 2. Agent Communication (`agents_communication.py`)

Two agents (Sigmar and Slaanesh) exchanging messages through a `Bureau`, demonstrating the uAgents messaging protocol.

```python
python agents_communication.py
```

### 3. Gas Price Monitor (`gasprice.py`)

Queries the Infura API for suggested gas fees across different priority levels (low, medium, high) for any EVM chain.

- **API:** Infura Gas API
- **Input:** Chain ID
- **Output:** Formatted gas price summary

### 4. Vehicle Details Micro Agent (`vehicle_details_micro_agent.py`)

A two-agent system (Alice & Bob) where Alice requests vehicle registration details and pays Bob with testnet FET tokens in exchange.

- **API:** RTO Vehicle Information API (RapidAPI)
- **Blockchain:** Fetch.ai testnet (atestfet)
- **Features:** On-chain payments, agent-to-agent transactions

### 5. Token Transfer (`sending_tokens.py`)

Demonstrates Fetch.ai testnet token transfers between two agents, with wallet funding, payment requests, and transaction verification.

### 6. Geocode Agent (`geocode/`)

Geocoding utility agent for location-based services.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | Fetch.ai uAgents |
| Blockchain | Fetch.ai Ledger (testnet) |
| Gas Data | Infura API |
| Vehicle Data | RTO Vehicle Info API (RapidAPI) |

## Project Structure

```
├── agent.py                          # Basic agent with storage
├── agents_communication.py           # Two-agent messaging
├── gasprice.py                       # Gas price protocol
├── vehicle_details_micro_agent.py    # Vehicle lookup + token payment
├── sending_tokens.py                 # FET token transfers
├── geocode/                          # Geocoding agent
├── agent1qww3ju3h6k_data.json       # Agent data storage
└── private_keys.json                 # Agent private keys
```

## Getting Started

### Prerequisites

- Python 3.8+
- Fetch.ai testnet account (auto-funded via `fund_agent_if_low`)

### Installation

```bash
git clone https://github.com/gautammanak1/fetch-works.git
cd fetch-works
pip install uagents requests
```

### Run Any Example

```bash
python agent.py                         # Basic agent
python agents_communication.py          # Agent messaging
python sending_tokens.py                # Token transfer
python vehicle_details_micro_agent.py   # Vehicle details + payment
```

## License

MIT
