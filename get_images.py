import requests
import os


def download_images(bird_name):
    query = bird_name
    save_dir = f"data/train/{bird_name.replace(" ", "_")}"
    max_images = 100

    base_url = "https://commons.wikimedia.org/w/api.php"

    #output
    os.makedirs(save_dir, exist_ok=True)

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
            if "imageinfo" in page and any(page["imageinfo"][0]["url"].lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
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


if __name__ == '__main__':
    download_images("European Starling")