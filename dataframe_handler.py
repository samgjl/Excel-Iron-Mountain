import pandas as pd
from ansi import ANSI
from tqdm import tqdm

# Standardize column names for the dataframe
def standardize(df: pd.DataFrame, page: str) -> pd.DataFrame:
    ANSI.info(f"    Standardizing '{page}'")
    df = df.copy()
    # Rename columns to official names:
    official_names = ["BARCODE", "TITLE", "TITLE OVERFLOW", "AUTHOR", "YEAR", "SOURCE"]
    for name in official_names:
        for col in df.columns:
            if name.upper() in col.upper():
                df = df.rename(columns={col: name})
                break # hard-coding for 'TITLE' and 'TITLE OVERFLOW'
    check_columns(df)
    # Remove unneccessary columns:
    for col in df.columns:
        if col not in official_names:
            df = df.drop(columns=[col])

    return unify_title(df)

# Combine the TITLE and TITLE OVERFLOW columns
def unify_title(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
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

# Concatenate multiple dataframes into one + deduplication if desired
def concatenate_dfs(dfs: list[pd.DataFrame], dedupe: bool = False) -> pd.DataFrame:
    lengths = [df.shape[0] for df in dfs]
    ANSI.header(f"Concatenating {len(lengths)} dataframes with a total of {sum(lengths)} rows.")
    ANSI.info("    Deduplication is ON." if dedupe else "    Deduplication is OFF.")

    dfs = [df.copy() for df in dfs]
    for df in dfs:
        df.set_index("BARCODE", inplace=True)

    df = pd.concat(dfs)
    # TODO: If these dupes are found, we need to MERGE THEM, not just drop the last ones
    if dedupe:
        df = merge_dupes(df)
    ANSI.success(f"    Complete.")
    return df

def merge_dupes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    dupes = df[df.index.duplicated(keep=False)]
    ANSI.info(f"    Found {len(dupes)} duplicates ({dupes.index.unique().shape[0]} barcodes with dupes).")

    for barcode in tqdm(dupes.index.unique()):
        rows = df.loc[barcode]
        rows.reset_index(inplace=True)
        # Merge the rows together:
        merged: pd.Series = rows.iloc[0]
        for i in range(1, len(rows)):
            if pd.isnull(merged["TITLE"]) and pd.notnull(rows.iloc[i]["TITLE"]):
                merged = rows.iloc[i]
        df = df.drop(barcode)
        df.loc[barcode] = merged
    return df
