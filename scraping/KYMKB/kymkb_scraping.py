import os
import json
import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Paths
BASE_DIR = "KYMKB/images"
MASTER_JSON_PATH = "KYMKB/master_data.json"

# Load existing master data to avoid re-scraping
if os.path.exists(MASTER_JSON_PATH):
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            master_data = json.load(f)
        except json.JSONDecodeError:
            master_data = {}
else:
    master_data = {}

# Load the updated meme data JSON
with open("jsons/updated_chonky_meme_data.json", "r", encoding="utf-8") as f:
    memes = json.load(f)

# Headers for requests
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Function to download an image
def download_image(img_url, save_path):
    if os.path.exists(save_path):
        return save_path  # Return existing path if already downloaded
    try:
        response = requests.get(img_url, headers=HEADERS, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return save_path  # Return file path after successful save
    except requests.RequestException as e:
        print(f"❌ Failed to download {img_url}: {e}")
    return None

# Function to fetch a URL with exponential backoff
def fetch_with_backoff(url, max_retries=5):
    delay = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response
        except requests.RequestException as e:
            print(f"⚠️ Attempt {attempt+1}: Failed to fetch {url}: {e}")
        time.sleep(delay)
        delay *= 2  # Exponential backoff
    return None

# Function to scrape and categorize text dynamically
def scrape_text(url):
    response = fetch_with_backoff(url)
    if not response:
        print(f"⚠️ Could not fetch {url}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    
    text_sections = {}

    # Known section headers to track
    section_headers = ["About", "Origin", "Spread", "Notable Examples", "Search Interest", "External References"]

    # Extract all sections with h2/h3 headings
    for section in soup.find_all(["h2", "h3"]):
        section_title = section.get_text(strip=True)

        # Only store known sections
        if section_title not in section_headers:
            continue

        section_content = []

        # Get all relevant sibling paragraphs
        for sibling in section.find_next_siblings():
            if sibling.name in ["h2", "h3"]:  # Stop at next heading
                break
            if sibling.name in ["p", "ul", "ol"]:
                section_content.append(sibling.get_text(separator=" ", strip=True))

        if section_content:
            text_sections[section_title] = " ".join(section_content)

    return text_sections

# Function to extract base template image from Wayback Machine
def get_base_template(soup, meme_dir):
    img_tag = soup.find("img", {"class": "entry_photo_image"})  # Adjust selector if needed
    if img_tag and "src" in img_tag.attrs:
        img_url = urljoin("https://web.archive.org", img_tag["src"])
        base_template_path = os.path.join(meme_dir, "base_template.jpg")

        # Actually write to disk
        if download_image(img_url, base_template_path):
            return base_template_path  # Return file path instead of URL

    return None

# Process each meme
for meme in tqdm(memes.values(), desc="Scraping Memes"):
    tqdm.write(f"🔍 Processing: {meme['title']}")
    title = meme["title"]
    url = meme["url"]
    example_images = meme.get("example_images", [])

    if not url:
        continue

    # Skip already processed memes
    if title in master_data:
        print(f"✅ Skipping {title}, already processed.")
        continue

    # Create directory structure
    meme_dir = os.path.join(BASE_DIR, title)
    os.makedirs(os.path.join(meme_dir, "examples"), exist_ok=True)

    # Scrape and categorize textual data
    categorized_text = scrape_text(url)

    # Fetch meme page for base template
    response = fetch_with_backoff(url)
    if not response:
        print(f"⚠️ Failed to access {url}")
        continue
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract and download base template image
    base_template_path = get_base_template(soup, meme_dir)

    # Download example images
    downloaded_examples = []
    for idx, img_url in enumerate(example_images):
        img_name = f"example_{idx+1}.jpg"
        img_path = os.path.join(meme_dir, "examples", img_name)
        if download_image(img_url, img_path):
            downloaded_examples.append(img_path)  # Store local file path
        time.sleep(1)  # Add delay between image downloads

    # Save metadata JSON
    metadata = {
        "title": title,
        "url": url,
        "base_template": base_template_path,  # Store local path, not just URL
        "example_images": downloaded_examples,
        **categorized_text  # Merging structured text data into JSON
    }

    with open(os.path.join(meme_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    # Update master JSON
    master_data[title] = metadata
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=4, ensure_ascii=False)

    time.sleep(5)  # Delay between meme scrapes

print("✅ Scraping complete! Data saved in KYMKB/images/")
