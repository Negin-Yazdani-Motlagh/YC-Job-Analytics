# YC-Job-Analytics

# codes

### `fetch_html_titles.py`
**Purpose**:Fetches and stores HTML content from a list of predefined URLs for analysis or archiving.

**Key Functionality**:
- Automates the process of collecting HTML data from multiple web pages.
- Handles HTTP errors and timeouts gracefully, logging errors for failed requests.
- Saves the HTML content along with associated metadata (URL and error details) in a structured JSON file.
- The result stored in json under title "HTML_All_Titles.json".

# result

### `HTML_All_Titles.json`
**Purpose**: Stores the results of the fetch_html_titles.py script, containing the HTML content and metadata for each processed URL.

**Key Functionality**:
- This result has been driven from the code called "fetch_html_titles_py"
- Provides a detailed log of successful and failed URL requests.
- Allows easy parsing and analysis of the collected HTML content and errors.
- be used to troubleshoot network issues or analyze the structure of the retrieved web pages.
