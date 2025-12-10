import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

@dataclass
class FundamentalRecord:
    symbol: str
    name: str
    cmp: float
    pe: Optional[float]
    marcap_cr: Optional[float]
    divyld_pct: Optional[float]
    npqtr_cr: Optional[float]
    qtr_profit_var_pct: Optional[float]
    sales_qtr_cr: Optional[float]
    qtr_sales_var_pct: Optional[float]
    roce_pct: Optional[float]
    debt_eq: Optional[float]
    yf_symbol: Optional[str]
    dhan_security_id: Optional[str]
    exchange: str = "NSE"

class FundamentalsRepository:
    def __init__(self, csv_path: Path = Path("data/penny_fundamentals.csv")):
        self.path = Path(csv_path)
        self.records: Dict[str, FundamentalRecord] = {}

    def load(self) -> List[FundamentalRecord]:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Fundamentals file not found: {self.path}. "
                f"Expected columns: symbol,name,cmp,pe,marcap_cr,divyld_pct,"
                f"npqtr_cr,qtr_profit_var_pct,sales_qtr_cr,qtr_sales_var_pct,"
                f"roce_pct,debt_eq,yf_symbol,dhan_security_id"
            )
        
        df = pd.read_csv(self.path)
        
        def safe_float(v):
            try:
                if v == '' or v is None:
                    return None
                return float(v)
            except:
                return None
        
        records: List[FundamentalRecord] = []
        
        for _, row in df.iterrows():
            symbol = str(row.get('symbol', '')).strip().upper()
            if not symbol:
                continue
            
            name = str(row.get('name', '')).strip()
            cmp_val = safe_float(row.get('cmp'))
            
            if cmp_val is None:
                logging.warning(f"Skipping {symbol} because CMP is missing/invalid in fundamentals.")
                continue
            
            dhan_security_id = str(row.get('dhan_security_id') or '').strip() or None
            yf_symbol = str(row.get('yf_symbol') or '').strip() or None
            
            exchange = str(row.get('exchange') or '').strip().upper()
            if not exchange:
                if dhan_security_id and dhan_security_id.upper().startswith("NSE"):
                    exchange = "NSE"
                elif dhan_security_id and dhan_security_id.upper().startswith("BSE"):
                    exchange = "BSE"
                elif yf_symbol:
                    if yf_symbol.upper().endswith(".NS"):
                        exchange = "NSE"
                    elif yf_symbol.upper().endswith(".BO"):
                        exchange = "BSE"
            
            if not exchange:
                exchange = "NSE"
            
            rec = FundamentalRecord(
                symbol=symbol,
                name=name,
                cmp=cmp_val,
                pe=safe_float(row.get('pe')),
                marcap_cr=safe_float(row.get('marcap_cr')),
                divyld_pct=safe_float(row.get('divyld_pct')),
                npqtr_cr=safe_float(row.get('npqtr_cr')),
                qtr_profit_var_pct=safe_float(row.get('qtr_profit_var_pct')),
                sales_qtr_cr=safe_float(row.get('sales_qtr_cr')),
                qtr_sales_var_pct=safe_float(row.get('qtr_sales_var_pct')),
                roce_pct=safe_float(row.get('roce_pct')),
                debt_eq=safe_float(row.get('debt_eq')),
                yf_symbol=yf_symbol,
                dhan_security_id=dhan_security_id,
                exchange=exchange,
            )
            
            records.append(rec)
        
        self.records = {r.symbol: r for r in records}
        logging.info(f"Loaded {len(records)} fundamental records from {self.path}")
        return records

    def get_all(self) -> List[FundamentalRecord]:
        if not self.records:
            return self.load()
        return list(self.records.values())

    def get(self, symbol: str) -> Optional[FundamentalRecord]:
        if not self.records:
            self.load()
        return self.records.get(symbol.upper())
