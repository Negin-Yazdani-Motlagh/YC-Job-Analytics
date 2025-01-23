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
**Purpose**:To fetch and save the HTML content of "Who is Hiring" posts specified in a JSON file (Who_Is_Hiring_Posts.json). Each post's content is stored as an individual HTML file in the HTML_Content directory for offline use, analysis, or archival. Additionally, the metadata and HTML content are consolidated into a JSON file (HTML_Content_Data.json) for further processing.

**Key Functionality**:
- Input file: Who_Is_Hiring_Posts.json. Output Files: HTML_Content. All individual HTML files are saved in this directory and Consolidated JSON File: File Name: HTML_Content_Data.json which is a single JSON file consolidating metadata, including titles, URLs, paths to saved HTML files, and optional HTML content. Script Name: fetch_html_who_is_hiring.py  
- Reads a JSON file (Who_Is_Hiring_Posts.json) containing: title: The title of the post. url: The URL to fetch HTML content from.
- Fetches HTML content for each post using HTTP requests with retry and exponential backoff mechanisms.
- Saves the HTML content as:
- Individual .html files in the HTML_Content directory, named based on sanitized post titles.
- A consolidated JSON file (HTML_Content_Data.json) containing metadata and file paths for all fetched posts.

### `parse_and_extract_posts.py`
**Purpose**:This script processes HTML files containing "Who is Hiring" posts, parses the content to analyze its structure, and extracts top-level job posts while organizing them into a nested JSON structure for further analysis or storage.

**Key Functionality**:
- output file:Nested_Job_Posts.json. Input file:HTML_Content/HTML_Content, Contains monthly HTML files representing "Who is Hiring" posts. Each file is named by month (e.g., 2025-01.html) and includes nested comments. 
- Reads HTML files from the folder: C:/Users/negin/HTML_Content/HTML_Content.
- Uses BeautifulSoup to parse the HTML structure.
- Identifies and extracts top-level comments (job posts) by checking indentation levels.
- Organizes extracted data into a nested JSON format with the following structure: Month: Key representing the file name (e.g., "2025-01").comments: List of extracted top-level job posts. numJobPost: Count of extracted job posts for the month.
- Saves the structured data in a JSON file
  
### `count_job_posts.py`
**Purpose**:To extract the number of job posts and their associated dates from the processed HTML files or JSON structure, summarizing the job post count by date for analysis or visualization.

**Key Functionality**:
- output:job_post_counts.json. Input:HTML content
- Iterates through parsed data containing HTML content or JSON files.
- Extracts the date and counts the number of job posts in each.
- Outputs a summary of job post counts with their respective dates.
- Saves the results to a structured JSON file or displays them in a readable format for further analysis.

### `analyze_soft_skills_occurrence.py`
**Purpose**: This script analyzes the occurrence of predefined soft skills within job posts extracted from a nested JSON dataset. It organizes the results by month and year, identifies the number of job posts mentioning soft skills, and generates a structured JSON output for further analysis.

**Key Functionality**:
- Input: "Nested Job Posts JSON" and Dictionary of Soft Skills (Excel). Output:soft_skills_occurrence_analysis
- Load and Process Input Data
- Counts occurrences of soft skills mentioned in the job post comments
- Sorts the soft skills by their frequency in descending order for each month.
- Structures results with months grouped by year
- Includes "Who is Hiring Right Now" data in the appropriate chronological position
- Saves the processed data to a new JSON file for visualization or further analysis.

### `visualize_soft_skills_proportion.py`
**Purpose**: To analyze and visualize the proportion of job posts mentioning soft skills over time. This helps identify trends in the emphasis on soft skills in job postings.
**Key Functionality**:
- Input files: Reads a nested JSON file containing job post data. Loads a dictionary of soft skills from an Excel file. output file: soft_skills_proportion_chart.png.
- For each month and year, calculates the proportion of job posts mentioning at least one soft skill relative to the total job posts.
- Converts month and year information into a datetime format. Sorts data chronologically for consistent visualization.
- Saves the chart as a PNG file for further use

# result

### `HTML_All_Titles.json`
**Purpose**: Stores the results of the fetch_html_titles.py script, containing the HTML content and metadata for each processed URL.

**Key Functionality**:
- This result has been driven from the code called "fetch_html_titles_py"
- Provides a detailed log of successful and failed URL requests.
- Allows easy parsing and analysis of the collected HTML content and errors.
- be used to troubleshoot network issues or analyze the structure of the retrieved web pages.

### `Who_Is_Hiring_Posts.json`
**Purpose**:To store the extracted data of "Who is Hiring" posts, including their titles, direct URLs, and source page URLs, from the processed HTML content.

**Key Functionality**:
- This result has been driven from the code called "Extract_who_is_hiring.py"
- Contains structured data with fields: title, url (direct post URL), and source_url (page from which the post was extracted).
- Serves as the output of the Extract_who_is_hiring_posts.py script.
- Enables easy access to filtered "Who is Hiring" posts for analysis or archiving.

### `HTML_content.html` NOT AVAILBLE 
**Purpose**: To consolidate and store metadata and file paths for the HTML content of "Who is Hiring" posts fetched from their respective URLs. This file serves as a centralized reference for analysis, verification, and further processing.

**Key Functionality**:
- Script name:`fetch_html_who_is_hiring.py`
- Contains the title, URL, and file path of each post's HTML content.
- Links each entry to its corresponding saved .html file.
- Stores the raw HTML content of each post for quick access without needing to open the .html files.

### `HTML_Content_Data.json` NOT AVAILBLE 
**Purpose**:To consolidate and store metadata and file paths for the HTML content of "Who is Hiring" posts fetched from their respective URLs. This file serves as a centralized reference for analysis, verification, and further processing.

**Key Functionality**:
- Script name:`fetch_html_who_is_hiring.py`
- Contains the title, URL, and file path of each post's HTML content.
- Links each entry to its corresponding saved .html file.

### `Nested_Job_Posts.json` NOT AVAILBLE 
**Purpose**: Stores the parsed data from monthly HTML files of "Who is Hiring" posts, keeping only top-level job posts and removing replies for further analysis.
**Key Functionality**:
- Scripts: `parse_and_extract_posts.py`
- Organizes job post data into a structured JSON format.
- Stores parsed comments from each HTML file under the respective month key.
- Includes metadata such as the number of job posts (numJobPost) for each month.
- Provides a cleaned dataset for additional analysis or reporting.

### `job_post_counts.json`
**Purpose**:To provide a simplified summary of the number of job posts for each date extracted from the HTML_content file. This file is essential for quick analysis and visualization of job post trends over time.

**Key Functionality**:
- output:job_post_counts.json. Input:HTML content. script:count_job_posts.py
- Stores the count of job posts associated with each date.
- Provides a clear and concise structure for further data analysis or visualization

### `soft_skills_occurrence_analysis.json`
**Purpose**: The purpose of this file is to provide a detailed analysis of the occurrence of predefined soft skills across job posts for different months and years. It serves as an organized and structured dataset to enable further insights, such as trends in soft skill demands over time.

**Key Functionality**:
- scripts name: `analyze_soft_skills_occurrence.py`
- Grouped by Year and Month
- Each month includes a breakdown of soft skills mentioned in job posts, sorted in descending order based on their frequency.
- The total number of job posts for each month is recorded to provide context for skill frequency analysis

### `soft_skills_proportion_chart.png`
**Purpose**: To provide a visual representation of the proportion of job posts mentioning at least one soft skill over time. This chart helps identify trends and patterns in the demand for soft skills in the job market.
**Key Functionality**:
- Displays how the emphasis on soft skills in job postings evolves across months and years
- The chart is organized by date, ensuring an easy-to-follow timeline
- Each data point represents the normalized ratio of job posts mentioning soft skills to the total job posts for a given period

