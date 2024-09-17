import time
import sqlite3
import pandas as pd
from numpy import nan
from src.ansi import ANSI
from src.dataframe_handler import standardize
from src.dataframe_handler import separate_by_year

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
    sheets = []
    for page in pages:
        s = pd.read_excel(excel, page)
        s["SOURCE"] = path + " -- " + page
        s.replace(nan, None, inplace=True)
        sheets.append(s)
    
    results = [standardize(sheet, page) for sheet, page in zip(sheets, pages)]
    ANSI.success(f"    Complete.")
    return results

def write_years_as_pages_excel(years: dict | pd.DataFrame, path: str) -> None:
    ANSI.header(f"Writing to '{path}'")
    if type(years) is not dict:
        years = separate_by_year(years)
    with pd.ExcelWriter(path) as writer:
        for year, data in years.items():
            data.to_excel(writer, sheet_name=str(year)) 
