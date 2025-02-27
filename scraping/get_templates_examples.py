import os
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Directory setup
snapshots_dir = "wayback_snapshots"
templates_dir = "templates"
master_json_path = 'jsons/master_metadata.json'

# Load existing master metadata if it exists
if os.path.exists(master_json_path):
    with open(master_json_path, "r", encoding="utf-8") as f:
        master_metadata = json.load(f)
else:
    master_metadata = {}

# Ensure directories exist
os.makedirs(templates_dir, exist_ok=True)

def get_wayback_snapshot(url):
    """Fetches the most recent Wayback Machine snapshot of a given URL."""
    wayback_api = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&filter=statuscode:200&collapse=timestamp&limit=1&sort=reverse"
    try:
        response = requests.get(wayback_api, timeout=10)
        response.raise_for_status()
        snapshots = response.json()
        if len(snapshots) > 1:
            return f"http://web.archive.org/web/{snapshots[1][1]}/{url}"
    except requests.RequestException:
        print(f"⚠️ Wayback snapshot failed for {url}")
    return None

def download_image(img_url, save_path):
    """Downloads an image from a URL and saves it to a specified path."""
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except requests.RequestException:
        print(f"❌ Image download failed: {img_url}")
    return False

for file in tqdm(os.listdir(snapshots_dir), desc="Processing Snapshots"):
    if not file.endswith(".html"):
        continue

    meme_title = file.rsplit("_", 1)[0].replace(" ", "_")
    meme_dir = os.path.join(templates_dir, meme_title)
    examples_dir = os.path.join(meme_dir, "examples")
    os.makedirs(meme_dir, exist_ok=True)
    os.makedirs(examples_dir, exist_ok=True)

    file_path = os.path.join(snapshots_dir, file)
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    metadata = {"title": meme_title, "sections": {}, "template_image": None, "examples": []}

    # Extract all text sections
    for header in soup.find_all("h2"):
        section_id = header.get("id", header.text.strip().lower().replace(" ", "_"))
        next_elem = header.find_next_sibling()
        section_text = []
        while next_elem and next_elem.name not in ["h2", "h3"]:
            if next_elem.name in ["p", "ul", "ol"]:
                section_text.append(next_elem.get_text(strip=True))
            next_elem = next_elem.find_next_sibling()
        if section_text:
            metadata["sections"][section_id] = " ".join(section_text)

    # Extract template image
    meta_img = soup.find("meta", property="og:image")
    if meta_img:
        original_img_url = meta_img.get("content")
        wayback_img_url = get_wayback_snapshot(original_img_url) if "web.archive.org" not in original_img_url else original_img_url
        time.sleep(1)
    else:
        original_img_url = wayback_img_url = None

    if wayback_img_url:
        template_img_path = os.path.join(meme_dir, f"{meme_title}.jpg")
        if download_image(wayback_img_url, template_img_path):
            metadata["template_image"] = {
                "original_url": original_img_url,
                "wayback_url": wayback_img_url,
                "local_path": template_img_path,
            }
            print(f"✅ Template saved: {template_img_path}")

    # Extract example images
    example_images = soup.find_all("img")
    print(f"🔍 Found {len(example_images)} images on the page.")

    seen_images = set()
    for idx, img in enumerate(example_images):
        original_img_url = img.get("data-src") or img.get("src")
        if not original_img_url or "i.kym-cdn.com/photos/" not in original_img_url:
            print(f"⚠️ Skipping image {idx + 1}: Invalid or unrelated URL.")
            continue

        normalized_url = original_img_url.split("?")[0]
        if normalized_url in seen_images:
            print(f"🔄 Skipping image {idx + 1}: Duplicate detected.")
            continue
        seen_images.add(normalized_url)

        # Save the image
        example_img_path = os.path.join(examples_dir, f"{len(metadata['examples']) + 1}.jpg")
        if download_image(original_img_url, example_img_path):
            metadata["examples"].append({
                "original_url": original_img_url,
                "local_path": example_img_path,
            })
            print(f"📸 Saved example {len(metadata['examples'])}: {example_img_path}")
            time.sleep(1)
        else:
            print(f"❌ Failed to download example image {original_img_url}")

    # Save per-meme metadata
    meme_json_path = os.path.join(meme_dir, "metadata.json")
    with open(meme_json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    master_metadata[meme_title] = metadata

# Save master metadata
with open(master_json_path, "w", encoding="utf-8") as f:
    json.dump(master_metadata, f, indent=4)

print(f"\n✅ Processing complete! Master metadata saved to {master_json_path}.")
