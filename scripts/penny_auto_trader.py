import os
import sys
import logging
from datetime import datetime, date, time as dtime
from pathlib import Path
from typing import Set
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from core.dhan_auth import get_dhan_client, get_security_id, DhanAuthenticationError

DATA_DIR = Path(__file__).parent.parent / "data"
RECO_CSV = DATA_DIR / "penny_recommendations.csv"
EXEC_CSV = DATA_DIR / "penny_trades_executed.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_market_time(now=None) -> bool:
    now = now or datetime.now()
    
    if now.weekday() >= 5:
        return False
    
    current_time = now.time()
    market_open = dtime(9, 15)
    market_close = dtime(15, 30)
    
    return market_open <= current_time <= market_close

def load_recommendations() -> pd.DataFrame:
    if not RECO_CSV.exists():
        logger.warning(f"Recommendations file not found: {RECO_CSV}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(RECO_CSV)
        if df.empty:
            logger.info("Recommendations file is empty")
        return df
    except Exception as e:
        logger.error(f"Failed to read recommendations: {e}")
        return pd.DataFrame()

def load_executed_today() -> Set[str]:
    if not EXEC_CSV.exists():
        return set()
    
    try:
        df = pd.read_csv(EXEC_CSV)
        
        if 'executed_date' in df.columns:
            df['executed_date'] = pd.to_datetime(df['executed_date']).dt.date
            today = date.today()
            today_trades = df[df['executed_date'] == today]
            return set(today_trades['symbol'].unique())
        
        return set()
    
    except Exception as e:
        logger.error(f"Failed to load executed trades: {e}")
        return set()

def log_execution(symbol: str, order_id: str, qty: int, price: float, status: str):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    trade_data = {
        'executed_date': datetime.now().date(),
        'executed_time': datetime.now().time(),
        'symbol': symbol,
        'order_id': order_id,
        'qty': qty,
        'price': price,
        'status': status
    }
    
    df = pd.DataFrame([trade_data])
    
    if EXEC_CSV.exists():
        df.to_csv(EXEC_CSV, mode='a', header=False, index=False)
    else:
        df.to_csv(EXEC_CSV, index=False)

def place_order_dhan(dhan, symbol: str, qty: int, security_id: str) -> dict:
    logger.info(f"Placing BUY order: {symbol} (ID: {security_id}), Qty: {qty}")
    
    try:
        response = dhan.place_order(
            security_id=security_id,
            exchange_segment=dhan.NSE,
            transaction_type=dhan.BUY,
            quantity=qty,
            order_type=dhan.MARKET,
            product_type=dhan.INTRA,
            price=0
        )
        
        logger.info(f"✓ Order placed for {symbol}: {response}")
        return response
        
    except Exception as e:
        logger.error(f"✗ Order failed for {symbol}: {e}")
        return {"status": "error", "message": str(e)}

def run_auto_trader(poll_interval_sec: int = 60):
    logger.info("=== Starting Dhan Penny Auto-Trader ===")
    
    try:
        dhan = get_dhan_client()
    except DhanAuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        sys.exit(1)
    
    placed_symbols = set()
    
    while True:
        try:
            if not is_market_time():
                logger.info("Outside market hours. Sleeping...")
                import time
                time.sleep(poll_interval_sec)
                continue
            
            df_reco = load_recommendations()
            if df_reco.empty:
                logger.info("No recommendations available")
                import time
                time.sleep(poll_interval_sec)
                continue
            
            executed_today = load_executed_today()
            
            for _, row in df_reco.iterrows():
                symbol = str(row.get('symbol', '')).strip()
                qty = int(row.get('qty', 0))
                
                if symbol in placed_symbols:
                    continue
                
                if symbol in executed_today:
                    logger.info(f"⊗ {symbol}: Already executed today")
                    continue
                
                if qty <= 0:
                    logger.warning(f"⊗ {symbol}: Invalid quantity ({qty})")
                    continue
                
                security_id = get_security_id(symbol)
                if not security_id:
                    logger.warning(f"⊗ {symbol}: Security ID not found. Skipping.")
                    continue
                
                response = place_order_dhan(dhan, symbol, qty, security_id)
                
                if isinstance(response, dict) and response.get('orderId'):
                    order_id = response['orderId']
                    order_status = response.get('orderStatus', 'PENDING')
                    price = float(row.get('cmp', 0))
                    
                    log_execution(symbol, order_id, qty, price, order_status)
                    placed_symbols.add(symbol)
                    logger.info(f"✓ {symbol}: Order logged successfully")
                else:
                    logger.error(f"✗ {symbol}: Order placement failed")
            
            logger.info(f"Cycle complete. Sleeping {poll_interval_sec} seconds...")
            import time
            time.sleep(poll_interval_sec)
        
        except KeyboardInterrupt:
            logger.info("Auto-trader stopped by user")
            break
        
        except Exception as e:
            logger.exception(f"Error in auto-trader loop: {e}")
            import time
            time.sleep(poll_interval_sec)

if __name__ == "__main__":
    poll_interval = int(os.getenv("PENNY_TRADER_POLL_SEC", "60"))
    run_auto_trader(poll_interval_sec=poll_interval)
