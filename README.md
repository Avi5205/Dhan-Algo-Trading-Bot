# Dhan Automated Trading System

A fully containerized, production-oriented algorithmic trading framework built for the Dhan broker using Python and Docker.  
The system automates order execution, manages symbol mapping, and enforces market-hour controls to ensure stable and reliable trading operations.

---

## Key Capabilities

- Automated order execution using the Dhan Trading API  
- Intelligent market-hours validation  
- Security master mapping for accurate symbol handling  
- Comprehensive execution and error logging  
- Dockerized deployment for consistent reproducibility  

---

## Prerequisites

Ensure the following are available:

- Docker & Docker Compose  
- Active Dhan trading account  
- Dhan API credentials (Client ID & Access Token)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Avi5205/Dhan-Algo-Trading-Bot.git

cd dhan-trading-system
```

### 2. Configure Environment Variables

```bash
cp config/credentials.env.example config/credentials.env
nano config/credentials.env
```

Populate:

- `DHAN_CLIENT_ID`
- `DHAN_ACCESS_TOKEN`

### 3. Build & Start Services

```bash
docker compose build
docker compose up -d
```

---

## Usage

### Start the System

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f penny-trader
```

### Stop Services

```bash
docker compose down
```

---

## Configuration

Main configuration file:

```
config/credentials.env
```

Never commit real credentials.  

---

## Project Structure

```
.
├── config/
│   ├── credentials.env.example
│   └── settings.yaml
├── core/
│   └── dhan_auth.py
├── scripts/
│   ├── download_security_master.py
│   ├── fundamentals.py
│   ├── penny_auto_trader.py
│   └── penny_reco_scheduler.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Security Notice

Do not store or commit live API keys, tokens, or confidential settings.  
Use the provided example environment files and load credentials at runtime.

---

## License

This project is licensed under the MIT License.
