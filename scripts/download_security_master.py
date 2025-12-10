import pandas as pd
import requests
from pathlib import Path

def download_security_master():
    url = "https://images.dhan.co/api-data/api-scrip-master.csv"
    
    print("Downloading Dhan security master...")
    df = pd.read_csv(url)
    
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = data_dir / "dhan_security_master.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✓ Downloaded {len(df)} securities to {output_path}")
    
    print("\nSample NSE stocks:")
    nse_stocks = df[df['SEM_EXCH_INSTRUMENT_TYPE'] == 'NSE'].head(10)
    print(nse_stocks[['SEM_TRADING_SYMBOL', 'SEM_SMST_SECURITY_ID', 'SEM_EXCH_INSTRUMENT_TYPE']])

if __name__ == "__main__":
    download_security_master()
