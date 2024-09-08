from src.dataframe_handler import concatenate_dfs
from src.io_handler import *

spreadsheets = {
    # Format:
    # "<path to spreadsheet>"": ["<sheet name>", "<sheet name>", ...],
    # The following are examples:
    # "C:Documents/extra/THESES.xlsx": ["Sheet1", "Sheet2", "Sheet3", "Sheet4 - No barcodes"],
    "./extra/THESES in IM - Additional Theses Audit.xlsx": ["Sheet3"],
    "./extra/THESES IN IM - Last-First author order 22X2Z MYSTERY BOXES.xlsx": ["L4263713-file", "Additional theses audit"],
    "./extra/Theses in IM - no titles.xlsx": ["L2484789-file", "new barcodes"],
    "./extra/Theses in Iron Mountain 22X2Z File Report.xlsx": ["L2484789-file", "L2484789-file", "174 theses - barcodes 0 inTIND", "barcodes-only no-title theses", "new barcodes"],
}
duplicates_path = "with_duplicates.xlsx"
no_duplicates_path = "without_duplicates.xlsx"


pages = []
for path, subsheet in spreadsheets.items():
    pages += get_spreadsheet_pages(path, subsheet)

dupe = concatenate_dfs(pages, dedupe=False)
dedupe = concatenate_dfs(pages, dedupe=True)

write_to_excel(dupe, duplicates_path)
write_to_excel(dedupe, no_duplicates_path)