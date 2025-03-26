# KYMKB scraper
#### Disclaimer: Our work should only ever be used for academic purposes.
## Overview
This script scrapes meme data from wayback machine. It downloads metadata, images, and textual information, organizing them into a structured format for easy access.

## Features
- Scrapes meme titles, URLs, and sectioned textual data (e.g., "About", "Origin", "Spread").
- Downloads base template images and example images.
- Stores all data in a structured directory format.
- Implements exponential backoff for handling request failures.
- Maintains a master JSON file to track progress and prevent redundant scraping.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install requests beautifulsoup4 tqdm
```

## Directory Structure
After running the script, the data is saved in the following format:

```
KYMKB/
│── images/
│   ├── Meme_Title_1/
│   │   ├── base_template.jpg
│   │   ├── examples/
│   │   │   ├── example_1.jpg
│   │   │   ├── example_2.jpg
│   │   ├── metadata.json
│   ├── Meme_Title_2/
│   │   ├── base_template.jpg
│   │   ├── examples/
│   │   ├── metadata.json
│── master_data.json
```

## Usage

1. **Prepare the JSON input file**: Ensure you have `jsons/updated_chonky_meme_data.json` available.
2. **Run the script**:

```bash
python kymkb_scraper.py
```

## Handling Interruptions
If the script is interrupted, it will resume from the last processed meme by checking `master_data.json`.

## Known Issues
- If `web.archive.org` is temporarily unavailable, the script will retry using exponential backoff.
- Some memes may not have a base template image available.
