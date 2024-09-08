import time
import pandas as pd
from ansi import ANSI
import sqlite3

def get_spreadsheet_pages(path: str, pages: list[str] = ["Sheet1"]) -> list[pd.DataFrame]:
    ANSI.header(f"Reading '{path}'")
    excel = pd.ExcelFile(path)
    sheets = [pd.read_excel(excel, page) for page in pages]
    results = [standardize(sheet, page) for sheet, page in zip(sheets, pages)]
    ANSI.success(f"    Complete.")
    return results

# Standardize column names for the dataframe
def standardize(df: pd.DataFrame, page: str) -> pd.DataFrame:
    ANSI.info(f"    Standardizing '{page}'")
    # rename columns to official names:
    official_names = ["BARCODE", "TITLE", "TITLE OVERFLOW", "AUTHOR", "YEAR"]
    for name in official_names:
        for col in df.columns:
            if name.upper() in col.upper():
                df = df.rename(columns={col: name})
                break # hard-coding for TITLE/TITLE OVERFLOW
    check_columns(df)

    # remove unneccessary columns:
    for col in df.columns:
        if col not in official_names:
            df = df.drop(columns=[col])

    df = unify_title(df)

    return df

# Combine the TITLE and TITLE OVERFLOW columns
def unify_title(df: pd.DataFrame) -> pd.DataFrame:
    if "TITLE OVERFLOW" in df.columns:
        df["TITLE"] = df["TITLE"].astype(str) + " " + df["TITLE OVERFLOW"].astype(str)
        df = df.drop(columns=["TITLE OVERFLOW"])
    return df

# Sanity checking to make sure everything's there
def check_columns(df: pd.DataFrame) -> None | IndexError:
    standard_columns = ["BARCODE", "TITLE", "AUTHOR", "YEAR"]
    errors = []
    for standard in standard_columns:
        if standard not in df.columns:
            errors.append(standard)
    if errors:
        error = f"Error: missing columns {errors} (found {", ".join(df.columns.tolist())}).\nPlease ensure the spreadsheet contains the correct column names."
        ANSI.error(error)


def concatenate_dfs(dfs: list[pd.DataFrame], dedupe: bool = False) -> pd.DataFrame:
    # Change the index to be the barcode field for each dataframe
    for df in dfs:
        df.set_index("BARCODE", inplace=True)

    df = pd.concat(dfs)
    # TODO: If these dupes are found, we need to MERGE THEM, not just drop the last ones
    if dedupe:
        df = df[~df.index.duplicated(keep="first")]
    return df

def write_to_sqlite(df: pd.DataFrame, path: str) -> None:
    conn = sqlite3.connect(path)
    now = time.strftime("%Y-%m-%d")
    df.to_sql(f"theses-{now}", conn, if_exists="replace")
    conn.close()

            
if __name__ == "__main__":
    spreadsheets = {
        "./extra/THESES in IM - Additional Theses Audit.xlsx": ["Sheet3"],
        "./extra/THESES IN IM - Last-First author order 22X2Z MYSTERY BOXES.xlsx": ["L4263713-file", "Additional theses audit"],
        "./extra/Theses in IM - no titles.xlsx": ["L2484789-file", "new barcodes"],
        "./extra/Theses in Iron Mountain 22X2Z File Report.xlsx": ["L2484789-file", "L2484789-file", "174 theses - barcodes 0 inTIND", "barcodes-only no-title theses", "new barcodes"],
    }

    for path, pages in spreadsheets.items():
        pages = get_spreadsheet_pages(path, pages)

    df = concatenate_dfs(pages, dedupe=False)
    # Check the final dataframe for duplications:
    sqlite3_path = "./extra/theses.db"
    write_to_sqlite(df, sqlite3_path)

    # Checking for dupes
    conn = sqlite3.connect(sqlite3_path)
    query = "SELECT * FROM 'theses-2024-09-06' GROUP BY BARCODE HAVING COUNT(BARCODE) > 1"
    result = pd.read_sql_query(query, conn)
    if not result.empty:
        ANSI.warn(f"Warning: Duplicates found in the final dataframe:\n{result}")


    conn.close()
    # duplicates = df[df.duplicated()]
    # if not duplicates.empty:
    #     print(duplicates)
    #     ANSI.error(f"Error: Duplicates found in the final dataframe:\n{duplicates}")
    # print(df)
        