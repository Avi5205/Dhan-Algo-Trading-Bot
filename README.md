# Dhan Automated Trading System

Dockerized algorithmic trading system for Dhan broker using Python.

## Features

- Automated order placement via Dhan API
- Market hours detection
- Security ID mapping
- Trade execution logging
- Docker-based deployment

## Setup

### Prerequisites

- Docker & Docker Compose
- Dhan trading account
- Dhan API credentials

### Installation

1. Clone repository
git clone https://github.com/YOUR_USERNAME/dhan-trading-system.git
cd dhan-trading-system

2. Configure credentials
cp config/credentials.env.example config/credentials.env
nano config/credentials.env

3. Build and run
docker compose build
docker compose up -d

### Configuration

Edit `config/credentials.env`:
- `DHAN_CLIENT_ID`: Your Dhan client ID
- `DHAN_ACCESS_TOKEN`: Your Dhan API access token

### Usage

Start system:
docker compose up -d

View logs:
docker compose logs -f penny-trader

Stop system:
docker compose down

### Project Structure

.
├── config/
│ ├── credentials.env.example
│ └── settings.yaml
├── core/
│ └── dhan_auth.py
├── scripts/
│ ├── download_security_master.py
│ ├── fundamentals.py
│ ├── penny_auto_trader.py
│ └── penny_reco_scheduler.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt


## Security

Never commit `config/credentials.env` or any files containing API credentials.

## License

MIT
