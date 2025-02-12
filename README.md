# YC-Job-Analytics

# codes

### `yc_job_extractor.py`
**Purpose**: To scrape all paginated content from websites with multiple pages, ensuring relevant data or URLs are collected systematically while navigating through each page in the website (https://news.ycombinator.com/submitted?id=whoishiring) 
**Key Functionality**:
- Dynamically navigates through multiple pages using "Next," "More," or similar pagination buttons.
- Supports ?page=x URL patterns or dynamically generated pagination links
- Extracts specific information from each page, such as job posting URLs, titles, or other relevant elements
- Gracefully manages situations where a "Next" button is missing, or the page fails to load
- Saves scraped data (e.g., URLs, job titles) into a text file for easy access

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

### `Job_Posts_Pre_Post_ChatGPT.py`
**Purpose**: This script analyzes job posts from the Y Combinator dataset to determine the proportion of job posts mentioning soft skills before and after the launch of ChatGPT (November 2022). The goal is to identify trends and changes in how often soft skills are referenced in job posts over time.

**Key Functionality**:
- Reads nested job post data from a JSON file
- Searches job post comments for mentions of soft skills using a predefined dictionary of keywords.
- Splits the data into pre-ChatGPT (before November 2022) and post-ChatGPT (November 2022 and onward) based on the job post dates
- Calculates the proportion of job posts mentioning at least one soft skill compared to the total number of job posts for each month-year
- Plots the trends of soft skill mentions over time, with separate lines for pre- and post-ChatGPT periods
- output name:soft_skills_pre_post_chatgpt_chart.png

### `Soft_Skills_Trend_Analysis.py`
**Purpose**: The script processes a JSON dataset containing monthly occurrences of soft skills and organizes the data into a structured format for deeper analysis and visualization. It calculates proportions of skill occurrences relative to total job postings (numJobPost) and outputs the results into an Excel file with multiple tabs for comprehensive exploration.

**Key Functionality**:
- Input file:soft_skills_occurrence_analysis.json. Output file:soft_skills_occurrence_analysis_with_proportions.xlsx
- Reads a JSON file containing soft skill occurrences categorized by year and month
- Combines month and year into a single column header (e.g., "January 2023")
- Transforms the processed dictionary into a Pandas DataFrame
- Adds a new tab (Proportions) to the Excel file. Calculates the proportion of each skill's occurrence relative to total job postings for each time period: Formula: Proportion = (Skill Occurrence / numJobPost)
- Rounds the calculated proportions to two decimal places for clarity.
- Exports the resulting DataFrame to an Excel file for easy access and visualization

### `Seasonal_Job_Postings_Analysis.py`
**Purpose**: This script analyzes seasonal trends in job postings over time by processing JSON data. It calculates monthly averages and visualizes seasonal changes, aiding in understanding patterns in job postings.
**Key Functionality**:
- Input: JSON file "job_post_counts" containing job posting data by month and year. Output file:Excel file: seasonal_job_postings.xlsx and PNG file: seasonal_change_job_postings.png
- Reads and processes job posting data from a JSON file.
- Extracts and cleans dates from the dataset.
- Adds separate columns for Month and Year for detailed analysis.
- Calculates the average number of job postings for each month across all years.
- Saves the processed data into an Excel file for future reference or additional analysis.
- Generates a line chart visualizing seasonal changes in job postings, labeled by months.

### `Seasonal_Job_Postings_Yearly_Comparison.py`
**Purpose**:To analyze and visualize seasonal changes in job postings over multiple years, providing insights into trends and fluctuations in job postings by month and year.
**Key Functionality**:
- Input file: Reads a JSON file containing job postings data (job_post_counts.json). Output file:seasonal_change_job_postings_yearly.png
- Extracts and cleans month and year information from the dataset
- Converts month names to numerical order for consistent plotting
- Creates a pivot table to organize job postings data by month (rows) and year (columns)
- Plots a multi-line graph showing the number of job postings for each month across all years

### `categorized_soft_skills.py`
**Purpose**: The purpose of this script is to analyze and categorize soft skills extracted from nested job post data. It identifies and counts occurrences of sub-skills within job post comments and aggregates them under corresponding head skill categories.

**Key Functionality**:
- soft_skills_occurrence_analysis.json: Contains extracted occurrences of soft skills.(This file have been extracted based on vs 8 of dictionary using privious code).
- Dictionary of soft skills (8).xlsx: A dictionary file mapping head skills to their respective sub-skills.
- Output File:categorized_soft_skills_analysis.json: Stores categorized counts of head skills based on their sub-skill occurrences.
- Reads an Excel file containing head skills and their associated sub-skills.
- Maps sub-skills to their respective head skills for accurate categorization.
- Processes a JSON file containing soft skill occurrences grouped by year and month.
- Scans the JSON data to count occurrences of sub-skills and updates the counts under their respective head categories.
- Handles case insensitivity (reads upper and lower case skill mentions equally).
- Outputs a JSON file categorizing the soft skills under head categories with chronological grouping (by year and month).

### `Soft_Skills_Trend_Analysis_categorize.py`
**Purpose**: This script processes a JSON file containing soft skill occurrence data grouped by year and month.

**Key Functionality**: 
- input_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\v8\categorized_soft_skills_by_headcategory.json' and output_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\v8\soft_skills_trend_analysis_categorized.xlsx'
- Reads a JSON input file containing skill occurrences over time.
- Cleans and sorts the data in chronological order (by year and month).
- Calculates proportions for each skill based on the total number of job posts (`numJobPost`).
- Exports results to an Excel file with two sheets: "Original Data" and "Proportions".

### `merge_who_is_hiring_urls.py`
**Purpose**: This script is designed to merge a new "Who is hiring?" URL entry into an existing JSON file of Hacker News URLs while ensuring data consistency and avoiding duplicates.
**Key Functionality**: 
- Loads an existing JSON file containing "Who is hiring?" URL entries. Input file: "HTML_Content_Data.json", Output file:Feb_who_is_hiring_URLs.json
- Adds a new URL entry to the list while checking for duplicates.
- Places the new entry at the top of the JSON data for better visibility.
- Saves the updated data into a new JSON file.


# result

### `hacker_news_urls.txt`
**Purpose**: This file contains a list of URLs extracted from Hacker News. It serves as the input data for scripts that filter, process, or analyze specific posts such as "Who is hiring?" threads.

**Key Functionality**:
- Provides a complete set of URLs scraped from Hacker News for further processing.
- Acts as the primary data source for identifying and extracting targeted information like "Who is hiring?" posts.

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

### `soft_skills_pre_post_chatgpt_chart.png`
**Purpose**:This chart visualizes the proportion of job posts mentioning soft skills before and after the launch of ChatGPT (November 2022). It highlights trends over time, showing how the emphasis on soft skills in job postings has evolved in relation to this milestone in AI development.

**Key Functionality**:
- Input Files: Nested_Job_Posts.json and Dictionary of soft skills.xlsx. Output File:soft_skills_pre_post_chatgpt_chart.png. Script Name:Job_Posts_Pre_Post_ChatGPT.py
- Displays separate trend lines for job posts mentioning soft skills in the pre-ChatGPT and post-ChatGPT periods
- Illustrates the proportion of job posts with soft skills mentions relative to the total number of job posts per month

### `soft_skills_occurrence_analysis_with_proportions.xlsx`
**Purpose**: This file provides a restructured and comprehensive view of soft skill occurrences and their proportions over time, enabling detailed analysis of trends and patterns. It is designed for visualization, comparison, and further analytical purposes.

**Key Functionality**:
- Script Name: Soft_Skills_Trend_Analysis.py. Input File Name: soft_skills_occurrence_analysis.json. Output File Name: soft_skills_occurrence_analysis_with_proportions.xlsx
- Rows represent individual soft skills.
- Columns represent time periods (formatted as "Month Year").
- Cell values indicate the number of occurrences for each skill during the specified time period.
- Computed the proportion of each skill's occurrence relative to the total job postings for each time period.
- Rounded proportions to two decimal places for simplicity and readability.
- 
### `soft_skills_proportion_chart ( math, science)`
**Purpose**: To provide a visual representation of the proportion of job posts mentioning at least one soft skill over time. This chart helps identify trends and patterns in the demand for soft skills in the job market.

**Key Functionality**:
- Input files: Reads a nested JSON file containing job post data. Loads a dictionary of soft skills from an Excel file include math and science. output file: soft_skills_proportion_chart ( math, science).png.
- Script name: visualize_soft_skills_proportion.py

### `seasonal_job_postings.xlsx` and  `seasonal_change_job_postings.png`
**Purpose**: To provide a detailed analysis of seasonal trends in job postings, capturing monthly variations and presenting the findings in both tabular and visual formats.

**Key Functionality**:
- Input: JSON file "job_post_counts" containing job posting data by month and year. Output file:Excel file: seasonal_job_postings.xlsx and PNG file: seasonal_change_job_postings.png. script name:`Seasonal_Job_Postings_Analysis.py`
- Lists raw job posting data with columns for the exact date, job post counts, month, and year. Enables further analysis or cross-referencing of specific time periods
- Displays the average number of job postings for each month across all years
- Highlights seasonal trends and peaks in job postings
  
### `seasonal_change_job_postings_yearly.png` and `seasonal_job_postings_yearly.xlsx`
**Purpose**: To visualize and analyze the seasonal trends in job postings over multiple years, helping identify patterns, peaks, and troughs across different months and years.

**Key Functionality**:
- Input file: Reads a JSON file containing job postings data (job_post_counts.json). Output file:seasonal_change_job_postings_yearly.png Script name: `Seasonal_Job_Postings_Yearly_Comparison.py`
- A visually enhanced, color-coded line chart displaying monthly job posting trends for each year.
- Clearly distinguishes trends for better readability, even when comparing numerous years.
- Highlights seasonal variations, making it easier to identify consistent patterns or anomalies.
- A pivot table with months as rows and years as columns, providing a concise year-by-year comparison for each month.

### `categorized_soft_skills_by_headcategory.json`
**Purpose**: The purpose of this JSON file is to store the aggregated counts of soft skills categorized under their respective head categories. It provides a clear representation of how often head skill categories appear in job post data, based on occurrences of their associated sub-skills.

**Key Functionality**:
- Script Name:categorized_soft_skills.py.
- Input Files: Nested_Job_Posts.json – Contains job post data, including comments and metadata such as year and month.Dictionary of soft skills (8).xlsx – A structured Excel file mapping head skill categories to their associated sub-skills.
- Data is grouped by year and month for temporal analysis of soft skill demands.
- Sub-skills found in job post comments are counted and aggregated under their respective head skill categories. Each head category represents the total occurrences of its associated sub-skills.
- Ensures that sub-skills are accurately mapped to their head categories, regardless of capitalization in the job post comments.
- Tracks the total number of job posts analyzed for each year and month (numJobPost), providing context for the aggregated data.

 ### `soft_skills_occurrence_analysis_final.xlsx`
**Purpose**: This script processes a JSON file containing data on the occurrences of soft skills categorized by year and month.It performs data cleaning, chronological sorting, proportion calculations, and outputs the data to an Excel file.

**Key Functionality**:
- Script Name: `Soft_Skills_Trend_Analysis_categorize.py`. input_file = categorized_soft_skills_by_headcategory.json' and output_file = soft_skills_occurrence_analysis_final.xlsx'
- Reads a JSON file containing skill occurrences grouped by month and year.
- Cleans and organizes the data, removing invalid or unwanted entries.
- Sorts data in chronological order (by year and month).
- Calculates proportions for each skill occurrence relative to the total number of job posts for each time period.
- Exports the results to an Excel file with separate tabs for original data and proportions.

# Apr 2011_ Feb 2025

### `Feb_who_is_hiring_URLs.json`
**Purpose**: This JSON file contains a curated list of "Who is hiring?" URLs from Hacker News, specifically updated to include the latest entries (e.g., February 2025). It serves as a centralized dataset for further processing or analysis of job posts.

**Key Functionality**: 
- Acts as an updated version of the existing Who_is_hiring_URLs.json with new entries added at the top.
- Script name: `merge_who_is_hiring_urls.py`


### `Feb_soft_skills_occurrence_analysis.json`
**Purpose**: soft_skills_occurrence_analysis.json
This updated file builds on soft_skills_occurrence_analysis.json, providing a refined and detailed analysis of the occurrence of predefined soft skills across job posts for February 2025. It serves as a structured dataset for tracking trends in soft skill demands over time with improved categorization and data accuracy.

**Key Functionality**: 
- scripts name: `analyze_soft_skills_occurrence.py` version (9) of dictionary has been used.
- Grouped by Year and Month
- Each month includes a breakdown of soft skills mentioned in job posts, sorted in descending order based on their frequency.
- The total number of job posts for each month is recorded to provide context for skill frequency analysis

### `Feb_categorized_soft_skills_by_headcategory.json`
**Purpose**: Updated Version of: categorized_soft_skills_by_headcategory.json
This updated JSON file stores the aggregated counts of soft skills categorized under their respective headcategories, specifically for February 2025. It refines the mapping of sub-skills to their respective categories, improving the accuracy of soft skill occurrence tracking across job postings. The file provides a structured view of how often different soft skill categories appear in job post data based on associated sub-skills.

**Key Functionality**: 
- Script Name: categorized_soft_skills.py. Input Files:Feb_Nested_Job_Posts.json – Contains job post data, including comments, metadata, and timestamps.Dictionary of soft skills (9).xlsx – A structured Excel file mapping headcategories to their associated sub-skills.
- Data is grouped by year and month for temporal analysis of soft skill demands.
- Sub-skills found in job post comments are counted and aggregated under their respective head skill categories. Each head category represents the total occurrences of its associated sub-skills.
- Ensures that sub-skills are accurately mapped to their head categories, regardless of capitalization in the job post comments.
- Tracks the total number of job posts analyzed for each year and month (numJobPost), providing context for the aggregated data.
