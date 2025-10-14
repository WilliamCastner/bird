import requests
import os

# === Configuration ===
query = "American Robin"
save_dir = "american_robins"
max_images = 100

# Wikimedia Commons API endpoint
base_url = "https://commons.wikimedia.org/w/api.php"

# Create output directory
os.makedirs(save_dir, exist_ok=True)

# === Step 1: Search for images ===
params = {
    "action": "query",
    "format": "json",
    "generator": "search",
    "gsrsearch": query,
    "gsrlimit": "50",  # fetch 50 at a time (max allowed)
    "prop": "imageinfo",
    "iiprop": "url",
    "gsrnamespace": 6,  # restrict to File: pages
}

headers = {
    "User-Agent": "bird-image-downloader (williambcastner@gmail.com)"
}

session = requests.Session()
downloaded = 0
continue_token = None

while downloaded < max_images:
    if continue_token:
        params["continue"] = continue_token

    response = session.get(base_url, headers=headers, params=params)
    data = response.json()

    if "query" not in data:
        print("No more results found.")
        break

    for page in data["query"]["pages"].values():
        if "imageinfo" in page:
            img_url = page["imageinfo"][0]["url"]
            filename = os.path.join(save_dir, os.path.basename(img_url))
            print(f"Downloading: {img_url}")

            try:
                img_data = session.get(img_url, headers=headers).content
                with open(filename, "wb") as f:
                    f.write(img_data)
                downloaded += 1
                if downloaded >= max_images:
                    break
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

    if "continue" in data:
        continue_token = data["continue"].get("continue")
    else:
        break

print(f"\n✅ Downloaded {downloaded} images to {save_dir}")
