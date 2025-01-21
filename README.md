# YC-Job-Analytics

# codes

### `fetch_html_titles.py`
**Purpose**:Fetches and stores HTML content from a list of predefined URLs for analysis or archiving.

**Key Functionality**:
- Automates the process of collecting HTML data from multiple web pages.
- Handles HTTP errors and timeouts gracefully, logging errors for failed requests.
- Saves the HTML content along with associated metadata (URL and error details) in a structured JSON file.
- The result stored in json under title "HTML_All_Titles.json".

### `Extract_who_is_hiring.py`
**Purpose**:To extract all "Who is Hiring" posts from a JSON file containing the HTML content of Hacker News pages and save the relevant data (titles, URLs, and source URLs, data) to a new JSON file for further analysis or archiving. 

**Key Functionality**:
- Input File is "HTML_All_Pages.json", Output File "Who_Is_Hiring_Posts.json" and Script Name is "extract_who_is_hiring.py"
- Reads a JSON file with webpage URLs and HTML content.
- Parses HTML to find posts titled "Who is Hiring" (case-insensitive).
- Extracts post titles, direct URLs, and source page URLs.
- Saves the extracted data to a new JSON file.


### `fetch_html_who_is_hiring.py`
***Purpose**:To fetch and save the HTML content of "Who is Hiring" posts specified in a JSON file (Who_Is_Hiring_Posts.json). Each post's content is stored as an individual HTML file in the HTML_Content directory for offline use, analysis, or archival. Additionally, the metadata and HTML content are consolidated into a JSON file (HTML_Content_Data.json) for further processing.

**Key Functionality**:
- Input file: Who_Is_Hiring_Posts.json. Output Files: HTML_Content. All individual HTML files are saved in this directory and Consolidated JSON File: File Name: HTML_Content_Data.json which is a single JSON file consolidating metadata, including titles, URLs, paths to saved HTML files, and optional HTML content. Script Name: fetch_html_who_is_hiring.py  
- Reads a JSON file (Who_Is_Hiring_Posts.json) containing: title: The title of the post. url: The URL to fetch HTML content from.
- Fetches HTML content for each post using HTTP requests with retry and exponential backoff mechanisms.
- Saves the HTML content as:
- Individual .html files in the HTML_Content directory, named based on sanitized post titles.
- A consolidated JSON file (HTML_Content_Data.json) containing metadata and file paths for all fetched posts.


# result

### `HTML_All_Titles.json`
**Purpose**: Stores the results of the fetch_html_titles.py script, containing the HTML content and metadata for each processed URL.

**Key Functionality**:
- This result has been driven from the code called "fetch_html_titles_py"
- Provides a detailed log of successful and failed URL requests.
- Allows easy parsing and analysis of the collected HTML content and errors.
- be used to troubleshoot network issues or analyze the structure of the retrieved web pages.

### `Who_Is_Hiring_Posts.json`
***Purpose**:To store the extracted data of "Who is Hiring" posts, including their titles, direct URLs, and source page URLs, from the processed HTML content.

**Key Functionality**:
- This result has been driven from the code called "Extract_who_is_hiring.py"
- Contains structured data with fields: title, url (direct post URL), and source_url (page from which the post was extracted).
- Serves as the output of the Extract_who_is_hiring_posts.py script.
- Enables easy access to filtered "Who is Hiring" posts for analysis or archiving.
