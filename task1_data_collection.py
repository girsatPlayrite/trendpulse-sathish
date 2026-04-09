# We import the tools we need
import requests       # lets us call URLs (like a browser, but in Python)
import json           # lets us save/read JSON files
import os             # lets us create folders
import time           # lets us pause the script
from datetime import datetime  # lets us get the current date and time

# ─────────────────────────────────────────
# STEP A: Define our categories and keywords
# ─────────────────────────────────────────
# This is a dictionary: each category name maps to a list of keywords.
# If a story title contains ANY of these words, it belongs to that category.

CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer",
                      "data", "cloud", "API", "GPU", "LLM", "programming",
                      "developer", "python", "javascript", "open source",
                      "startup", "app", "web", "security", "database",
                      "machine learning", "neural", "robot", "hardware",
                      "chip", "microsoft", "google", "apple", "meta"],

    "worldnews":     ["war", "government", "country", "president",
                      "election", "climate", "attack", "global", "police",
                      "court", "law", "bill", "military", "nuclear",
                      "china", "russia", "ukraine", "india", "europe",
                      "congress", "senate", "policy", "crisis", "protest"],

    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team",
                      "player", "league", "championship", "soccer",
                      "football", "basketball", "baseball", "tennis",
                      "olympic", "tournament", "coach", "win", "score",
                      "match", "athlete", "cricket", "golf", "racing"],

    "science":       ["research", "study", "space", "physics", "biology",
                      "discovery", "NASA", "genome", "climate", "ocean",
                      "fossil", "planet", "star", "telescope", "vaccine",
                      "medicine", "health", "brain", "evolution", "lab",
                      "experiment", "scientist", "energy", "quantum"],

    "entertainment": ["movie", "film", "music", "Netflix", "game",
                      "book", "show", "award", "streaming", "actor",
                      "director", "album", "song", "concert", "theatre",
                      "disney", "amazon", "hulu", "spotify", "podcast",
                      "youtube", "tiktok", "celebrity", "sequel", "series"],
}
# ─────────────────────────────────────────
# STEP B: A helper function to assign a category
# ─────────────────────────────────────────
# This function takes a title (string) and returns which category it fits.
# If no keyword matches, it returns None (we skip those stories).

def get_category(title):
    title_lower = title.lower()  # make the title lowercase so matching is case-insensitive
    
    for category, keywords in CATEGORIES.items():  # loop through each category
        for keyword in keywords:                    # loop through each keyword in it
            if keyword.lower() in title_lower:      # if keyword is found in title
                return category                     # return that category name immediately
    
    return None  # no match found

# ─────────────────────────────────────────
# STEP C: Fetch the top 500 story IDs from HackerNews
# ─────────────────────────────────────────

print("Fetching top story IDs from HackerNews...")

# This is the URL that gives us a list of trending story IDs
ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

# We add a User-Agent header so the server knows who's asking
headers = {"User-Agent": "TrendPulse/1.0"}

try:
    response = requests.get(ids_url, headers=headers)  # make the request
    all_ids = response.json()[:1000]                    # parse JSON, take first 500 IDs
    print(f"Got {len(all_ids)} story IDs.")
except Exception as e:
    print(f"Failed to fetch story IDs: {e}")
    all_ids = []  # if it fails, use empty list so script doesn't crash

# ─────────────────────────────────────────
# STEP D: Fetch story details for each ID
# ─────────────────────────────────────────
# We'll collect up to 25 stories per category.
# We use a dictionary to track how many we've collected in each category.

# This will hold our final list of story dictionaries
collected_stories = []

# This tracks how many stories we have per category so far
category_counts = {cat: 0 for cat in CATEGORIES}
# ↑ This creates: {"technology": 0, "worldnews": 0, "sports": 0, ...}

MAX_PER_CATEGORY = 25  # we want at most 25 stories per category

print("Fetching individual story details...")

for story_id in all_ids:  # loop through each of the 500 IDs
    
    # If all categories already have 25 stories, we're done — stop early
    if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
        break
    
    # Build the URL for this specific story
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    
    try:
        story_response = requests.get(story_url, headers=headers)  # fetch the story
        story = story_response.json()                               # parse the JSON
        
        # Some stories might be None or not have a title — skip those
        if not story or "title" not in story:
            continue
        
        title = story.get("title", "")   # get the title (or empty string if missing)
        category = get_category(title)   # find which category this title belongs to
        
        # If no category matched, skip this story
        if category is None:
            continue
        
        # If we already have 25 stories for this category, skip
        if category_counts[category] >= MAX_PER_CATEGORY:
            continue
        
        # ── Extract all 7 required fields ──
        story_data = {
            "post_id":      story.get("id"),           # unique story ID
            "title":        story.get("title"),        # story title
            "category":     category,                  # our assigned category
            "score":        story.get("score", 0),     # upvotes (default 0 if missing)
            "num_comments": story.get("descendants", 0), # comments (default 0)
            "author":       story.get("by", "unknown"), # username
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # current time
        }
        
        collected_stories.append(story_data)   # add to our master list
        category_counts[category] += 1         # increase the count for this category
        
    except Exception as e:
        # If fetching ONE story fails, just print and move on
        print(f"Skipping story {story_id}: {e}")
        continue
    
    # ── Sleep 2 seconds after finishing each category's 25th story ──
    if category_counts[category] == MAX_PER_CATEGORY:
        print(f"  ✓ Collected 25 stories for: {category}")
        time.sleep(2)  # pause for 2 seconds before continuing

# ─────────────────────────────────────────
# STEP E: Save the data to a JSON file
# ─────────────────────────────────────────

# Create the data/ folder if it doesn't already exist
os.makedirs("data", exist_ok=True)
# ↑ exist_ok=True means: don't crash if the folder already exists

# Build today's date string for the filename, e.g. "20240115"
today = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today}.json"

# Write our list of stories to the file
with open(filename, "w") as f:
    json.dump(collected_stories, f, indent=2)
# ↑ indent=2 makes the JSON nicely formatted and readable

# ─────────────────────────────────────────
# STEP F: Print a summary
# ─────────────────────────────────────────

print(f"\nCollected {len(collected_stories)} stories. Saved to {filename}")
print("\nBreakdown by category:")
for cat, count in category_counts.items():
    print(f"  {cat}: {count} stories")
