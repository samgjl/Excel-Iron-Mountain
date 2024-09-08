import time
import sqlite3
import pandas as pd
from numpy import nan
from ansi import ANSI
from dataframe_handler import standardize

def write_to_sqlite(df: pd.DataFrame, path: str) -> None:
    conn = sqlite3.connect(path)
    now = time.strftime("%Y-%m-%d")
    df.to_sql(f"theses-{now}", conn, if_exists="replace")
    conn.close()

def write_to_excel(df: pd.DataFrame, path: str) -> None:
    ANSI.header(f"Writing to '{path}'")
    df.to_excel(path)
    ANSI.success(f"    Complete.")

def get_spreadsheet_pages(path: str, pages: list[str] = ["Sheet1"]) -> list[pd.DataFrame]:
    ANSI.header(f"Reading '{path}'")
    excel = pd.ExcelFile(path)
    # sheets = [pd.read_excel(excel, page) for page in pages]
    sheets = []
    for page in pages:
        s = pd.read_excel(excel, page)
        s["SOURCE"] = path + " -- " + page
        s.replace(nan, None, inplace=True)
        sheets.append(s)
    
    results = [standardize(sheet, page) for sheet, page in zip(sheets, pages)]
    ANSI.success(f"    Complete.")
    return results


