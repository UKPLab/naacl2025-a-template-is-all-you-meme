# Use Our Scraping Code to Make Your Own KYMKB!
#### Disclaimer: Our work should only ever be used for academic purposes.
### Step 1: Install Dependencies

See the installation section here: https://github.com/UKPLab/naacl2025-a-template-is-all-you-meme

### Step 2: Run `downloader.ipynb`

This step will download and write to disk all the parent entries in the "confirmed" section of Know Your Meme.

#### Code Explanation

- **WebDriver Setup**:  
  The script initializes a Chrome browser using **Selenium WebDriver** and automatically downloads the correct **ChromeDriver** using the **webdriver-manager** package.

- **Navigation**:  
  The script scrapes the list of memes starting from the first page and moves to subsequent pages using the "next page" button. It continuously saves each page's HTML source.

- **Error Handling**:  
  If an issue occurs with locating the "next page" button, the script will gracefully terminate and inform the user.

- **Sleep Time**:  
  The script waits for **2 seconds** after loading each page to ensure that the page is fully loaded before performing actions.

#### Output

The HTML source of each meme list page will be saved in the **`selenium_snapshots`** directory as `page_{page_number}.html`. Each file represents one page of memes.

---

### Step 3: Run `parseandwrite.py`

This script looks at all the parent entries in the "confirmed" section, downloads them, and writes them to disk.

#### Code Explanation

1. **Imports and Setup**  
   The script uses the following libraries:
   - **requests**: For HTTP requests to access the **Wayback Machine API** and fetch snapshots.
   - **BeautifulSoup** from **bs4**: To parse and extract links from HTML pages.
   - **json**: For reading and writing JSON data.
   - **os**: To handle file and directory creation.
   - **tqdm**: To display a progress bar during the process.

2. **Directories and Data Loading**  
   - **snapshots_dir**: Directory for storing the HTML snapshots.
   - **jsons_dir**: Directory for storing metadata.
   - The script loads previously processed meme URLs from **meme_tables.json** to avoid re-processing them. If there are any missed URLs (for which snapshots were not found), they are loaded from **miss.json**.

3. **Fetching Wayback Machine Snapshots**  
   - The `get_wayback_snapshot()` function queries the Wayback Machine’s API for a snapshot of a given meme URL. If a snapshot is found, the function returns the snapshot’s URL and timestamp; otherwise, it returns `None`.

4. **Processing HTML Files**  
   - The script iterates over all HTML files in the **`selenium_snapshots/`** directory.
   - It extracts meme URLs by looking for `<img>` tags with the attribute `data-data-entry-name`.
   - Invalid URLs (those not starting with "http") are ignored.

5. **Handling Already Processed URLs**  
   - URLs that have already been processed (stored in **meme_tables.json**) are excluded from the processing queue.

6. **Fetching and Storing Snapshots**  
   - For each new meme URL, the script fetches the closest **Wayback Machine snapshot**.
   - If a snapshot is found, the script downloads the snapshot content and saves it as an HTML file in the appropriate directory.
   - The script writes the URL of each successfully processed meme snapshot into **meme_tables.json** and logs missed URLs in **miss.json**.

7. **Error Handling**  
   - If a request fails while fetching a Wayback Machine snapshot or HTML content, the script will wait for **10 minutes** before retrying.
   - If no snapshots are found for a meme, it logs the missed URL for future attempts.

---

### Output

- **HTML Files**:  
  Each snapshot of a meme is saved as an HTML file in the **`selenium_snapshots`** directory under a folder named by the timestamp of the snapshot.  
  For example, a snapshot with the timestamp `20230222120000` would be saved in **`selenium_snapshots/20230222120000/`**.  
  The files are named `1_tablecontent.html`, `2_tablecontent.html`, etc., depending on how many snapshots have been processed.

- **JSON Files**:  
  - **meme_tables.json**: This file stores metadata about the successfully processed meme URLs and their associated snapshots. Each entry contains the `url` of the snapshot and the `count` of how many memes have been processed.
  - **miss.json**: This file contains URLs for which snapshots could not be found. Each entry in this file includes the `url` and the `count` of missed URLs.
 

### Step 4: Run write_html.py

## Overview

This script extracts meme data from a JSON file, retrieves archived snapshots from the Wayback Machine, and saves them as HTML files. It also records successful and missed retrievals.

## Features

- Parses a JSON file containing meme data and groups entries by title.
- Retrieves the most recent archived snapshot from the Wayback Machine.
- Saves snapshot HTML files to a structured directory.
- Maintains logs of successful and missed requests.
- Implements polite request handling with rate limiting.

## Directory Structure

After running the script, the data is saved in the following format:

```
📂 **jsons/**
├── 📄 *meme_data.json* — Source JSON with meme information  
├── 📄 *wayback_hits.json* — Successfully retrieved snapshots  
├── 📄 *wayback_misses.json* — URLs with no available snapshots  

📂 **wayback_snapshots/**
├── 📄 *Meme_Title_1_timestamp.html*  
├── 📄 *Meme_Title_2_timestamp.html*
```


## Usage

Run the script:
`python write_html.py`

### Step 5 run get_templates_examples.py Meme Scraper & Organizer 🖼️📜  

This script extracts meme data from archived webpages, downloads relevant images, and organizes them into structured JSON files for analysis and reference.  

## 📂 Project Structure  

```
📂 jsons/  
├── 📄 meme_data.json — Source JSON with meme information  
├── 📄 wayback_hits.json — Successfully retrieved snapshots  
├── 📄 wayback_misses.json — URLs with no available snapshots  
├── 📄 master_metadata.json — Merged metadata of all memes  

📂 wayback_snapshots/  
├── 📄 Meme_Title_1_timestamp.html  
├── 📄 Meme_Title_2_timestamp.html  

📂 templates/  
├── 📂 Meme_Title_1/  
│   ├── 📄 metadata.json — Contains extracted text and image metadata  
│   ├── 🖼️ Meme_Title_1.jpg — Base template image  
│   ├── 📂 examples/ — Folder with example images  
│       ├── 🖼️ 1.jpg  
│       ├── 🖼️ 2.jpg  
├── 📂 Meme_Title_2/  
│   ├── 📄 metadata.json  
│   ├── 🖼️ Meme_Title_2.jpg  
│   ├── 📂 examples/  
│       ├── 🖼️ 1.jpg  
│       ├── 🖼️ 2.jpg
```

## Features  
- **Extracts text and metadata**  
  - Parses archived HTML pages from `wayback_snapshots/`  
  - Extracts sections, descriptions, and meme titles  

- **Downloads images**  
  - Finds and saves the main template image  
  - Collects example images and saves them in `examples/`  

- **Stores data**  
  - Generates a `metadata.json` file per meme  
  - Updates `master_metadata.json` with all processed memes  

## 🛠️ Usage
run the script:
`python get_templates_examples.py`

