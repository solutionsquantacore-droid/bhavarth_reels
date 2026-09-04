import yt_dlp
import json
import os

JSON_FILE = "sadhanpath_shorts.json"

def get_channel_shorts(channel_handle):
    url = f"https://www.youtube.com/{channel_handle}/shorts"
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True
    }
    
    shorts_urls = []
    print(f"Fetching shorts from {channel_handle}...")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    video_url = entry.get('url')
                    if video_url:
                        shorts_urls.append(video_url)
        except Exception as e:
            print(f"Error fetching shorts: {e}")
            
    return shorts_urls

def main():
    channel = "@SadhanPath"
    new_urls = get_channel_shorts(channel)
    
    existing_urls = []
    
    # Load existing URLs to prevent duplicates
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                data = json.load(f)
                existing_urls = data.get("urls", [])
        except json.JSONDecodeError:
            print(f"Error reading {JSON_FILE}. Starting fresh.")
    
    # Convert to a set for fast duplicate checking, but keep a list for order
    existing_set = set(existing_urls)
    all_urls = existing_urls.copy()
    
    added_count = 0
    # Prepend new videos (since YouTube puts newest first)
    for url in reversed(new_urls): 
        if url not in existing_set:
            all_urls.insert(0, url) # Add new ones to the top
            existing_set.add(url)
            added_count += 1
            
    print(f"Found {added_count} new shorts.")
    
    # Save back to JSON
    with open(JSON_FILE, "w") as f:
        json.dump({"urls": all_urls}, f, indent=4)
        
    print(f"Successfully saved {len(all_urls)} total URLs to {JSON_FILE}")

if __name__ == "__main__":
    main()
