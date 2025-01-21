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


### ``
***Purpose**
**Key Functionality**:


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
