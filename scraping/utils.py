import requests
import re



def sanitize_filename(filename):
    """Removes or replaces invalid characters for filenames."""
    filename = filename.replace(" ", "_")  # Replace spaces with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid characters
    return filename
# Function to get the most recent Wayback snapshot
def get_wayback_snapshot(url):
    """Fetch the most recent Wayback Machine snapshot for a given URL."""
    api_url = f"https://archive.org/wayback/available?url={url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            return data["archived_snapshots"]["closest"]["url"]

        return None  # No snapshot found

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Wayback snapshot for {url}: {e}")
        return None