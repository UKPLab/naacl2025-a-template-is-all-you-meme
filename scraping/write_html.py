import os
import re
import json
import time
import requests
from tqdm import tqdm
from collections import defaultdict
from utils import get_wayback_snapshot, sanitize_filename

def extract_and_group_by_title(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all valid JSON arrays in the file
        json_lists = re.findall(r"\[\s*{.*?}\s*\]", content, re.DOTALL)

        grouped_data = defaultdict(list)

        for json_list in json_lists:
            try:
                parsed_list = json.loads(json_list)
                if isinstance(parsed_list, list):  # Ensure it's a valid list
                    for entry in parsed_list:
                        if isinstance(entry, dict) and "title" in entry:
                            grouped_data[entry["title"]].append(entry)
                        else:
                            print(f"❌ Skipping invalid entry: {entry}")
            except json.JSONDecodeError:
                print("❌ Skipping malformed JSON chunk")
                continue  # Skip malformed sections

        print(f"✅ Extracted and grouped JSON into {len(grouped_data)} unique titles.")
        return grouped_data

    except Exception as e:
        print(f"❌ Error processing JSON file: {e}")
        return {}
# Example usage
meme_data_file = "jsons/meme_data.json"
meme_data = extract_and_group_by_title(meme_data_file)


# Directory paths
jsons_dir = "jsons"
snapshots_dir = "wayback_snapshots"
WAYBACK_API = "http://web.archive.org/cdx/search/cdx"


# Ensure directories exist
os.makedirs(jsons_dir, exist_ok=True)
os.makedirs(snapshots_dir, exist_ok=True)

# JSON file names
meme_data_file = os.path.join(jsons_dir, "meme_data.json")
hits_file = os.path.join(jsons_dir, "wayback_hits.json")
misses_file = os.path.join(jsons_dir, "wayback_misses.json")
#meme_data = load_meme_json(meme_data_file)
print(f"✅ Loaded {len(meme_data)} memes successfully!")


wayback_hits = []
wayback_misses = []
processed_urls = {}  # Track already fetched meme URLs

# Process each meme entry
 #Loop over dictionary keys (titles) and their corresponding list of entries
for title, entries in tqdm(meme_data.items(), desc="Fetching Wayback Snapshots"):
    for entry in entries:
        meme_url = entry.get("meme_url")

        if not meme_url:
            print(f"⚠️ Missing meme_url for {title}")
            continue

        # Skip if we've already processed this URL
        if meme_url in processed_urls:
            continue

        # Get the most recent Wayback snapshot
        snapshot_url = get_wayback_snapshot(meme_url)

        if snapshot_url:
            # Save snapshot HTML
            timestamp = snapshot_url.split("/web/")[1].split("/")[0]
            filename = os.path.join(snapshots_dir, f"{sanitize_filename(title.replace(' ', '_'))}_{timestamp}.html")

            try:
                response = requests.get(snapshot_url)
                response.raise_for_status()

                with open(filename, "wb") as f:
                    f.write(response.content)

                wayback_hits.append({"title": title, "wayback_url": snapshot_url})
                processed_urls[meme_url] = snapshot_url  # Mark as processed
                print(f"✅ Saved {filename}")

            except requests.RequestException:
                print(f"⚠️ Failed to save {title} from {snapshot_url}")
                wayback_misses.append({"title": title, "meme_url": meme_url})

            time.sleep(1)  # Be polite to Wayback Machine

        else:
            print(f"❌ No snapshot found for {title}")
            wayback_misses.append({"title": title, "meme_url": meme_url})

# Save results to JSON
with open(hits_file, "w", encoding="utf-8") as f:
    json.dump(wayback_hits, f, indent=4)

with open(misses_file, "w", encoding="utf-8") as f:
    json.dump(wayback_misses, f, indent=4)

print(f"\n✅ Completed! {len(wayback_hits)} snapshots saved, {len(wayback_misses)} missed.")