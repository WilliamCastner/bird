import requests
from dotenv import load_dotenv
import os
from collections import defaultdict

import requests

def get_commons_images(query, limit=10):
    """
    Fetch image URLs from Wikimedia Commons for a given search query.
    """
    endpoint = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
        "origin": "*"
    }

    resp = requests.get(endpoint, params=params)
    data = resp.json()

    results = []
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        imageinfo = page.get("imageinfo")
        if imageinfo:
            results.append(imageinfo[0]["url"])
    return results

# Example: search for European Starling




def get_frequency(start, finish):
    load_dotenv() # Load environment variables from .env file
    api_key = os.environ.get("api_token")

    # Replace these with your actual values
    serverName = "api.ebird.org"
    contextRoot = "v2"
    regionCode = "US-IL-031"
    y = "2025"
    m = "08"
    api_token = "br39qj9m24rq"

    speciesCount = defaultdict(int)

    headers = {
        "x-ebirdapitoken": api_key
    }

    # loop through October of 2024
    for day in range(start, finish):
        url = f"https://{serverName}/{contextRoot}/data/obs/{regionCode}/historic/{y}/{m}/{str(day)}"
        response = requests.get(url, headers=headers)
        for i in response.json():
            if 'howMany' in i:
                speciesCount[i['comName']] += int(i['howMany'])
            else:
                print(i)

    for key, value in speciesCount.items():
        print(f"{key}: {value}")

def sort_bird_frequencies(filename, output_file="sorted_bird_frequency.txt"):
    """
    Reads a text file containing bird species and counts,
    sorts them from most to least common,
    and writes the results to a new file.
    """

    bird_counts = {}

    # Read and parse lines like "Species Name: 123"
    with open(filename, "r") as file:
        for line in file:
            if ":" in line:
                name, count = line.strip().split(":", 1)
                bird_counts[name.strip()] = int(count.strip())

    # Sort dictionary by count (descending)
    sorted_birds = sorted(bird_counts.items(), key=lambda x: x[1], reverse=True)

    # Write sorted output to file
    with open(output_file, "w") as out:
        out.write(f"{'Bird Species':40s} | Count\n")
        out.write("-" * 55 + "\n")
        for name, count in sorted_birds:
            out.write(f"{name:40s} | {count}\n")

    # Print summary
    print(f"✅ Sorted {len(sorted_birds)} bird species.")
    print(f"📄 Results written to '{output_file}'")

    return sorted_birds


# Example usage
if __name__ == "__main__":
    file = 'File:The_Blue_Marble.jpg'

    headers = {
    # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'User-Agent': 'YOUR_APP_NAME (YOUR_EMAIL_OR_CONTACT_PAGE)'
    }

    base_url = 'https://api.wikimedia.org/core/v1/commons/file/'
    url = base_url + file
    response = requests.get(url, headers=headers)
    print(response.json())