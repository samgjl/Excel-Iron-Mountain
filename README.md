<style>
    .code {
        border-radius: 5px;
        background-color: #26a641;
        color: white;
        padding: 10px;       
        border: none;
    }
    .code:hover {
        color: white;
        background-color: #52a869;
        text-decoration: none;
    }
    .code:active {
        background-color: #42c95f;

    }
</style>

# Excel-Iron-Mountain
Interface for the merging of spreadsheets for Caltech's Iron Mountain

## Installation and use:
1. Clone this repository, or download the zip file using the <a class="code" href="https://github.com/samgjl/Excel-Iron-Mountain/archive/refs/heads/main.zip"><> Code ▾</a> button in the top right (Code > Download Zip).
2. Download all of its requirements:
    - Pip: ```pip install -r requirements.txt```
    - Conda: ```conda install --file requirements.txt```
3. Modify the ```main.py``` file to your needs:
    - Update the set of spreadsheets you would like consolidated. Each entry is of the following format:
    <br> ```"<PATH>" : ["<Sheet1>", "<Sheet2>", ... , "<SheetN>"],```
    <br> Example: ```"C:Documents/Library/Theses.xlsx" : ["Main", "no_titles", "new barcodes - titles added"],```
    <br> <i>Note: add the comma at the end of each line. Otherwise, the program with break.</i>
    - Update the variables ```duplicates_path``` and ```no_duiplicates_path``` with the filepaths for the Excel file that allows duplicate entries and the one that does not, respectively. For example:
            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```duplicates_path = "C:Documents/Library/duplicates_file.xlsx"```
            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```no_duplicates_path = "C:Documents/Library/no_duplicates_file.xlsx"```
4. Run the file with your distribution of Python (```python main.py```).
<br> <i>Note: if you don't specify the absolute filepath, the program will try to output the files that the terminal is currently in.</i>
