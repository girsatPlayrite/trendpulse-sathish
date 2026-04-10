#Task 2 — Data Processing
#We load the JSON from Task 1, clean it, and save it as a CSV file

import pandas as pd    # pandas helps us work with tables of data
import os              # helps us work with files and folders
import glob            # helps us search for files by pattern

#STEP 1 — Find and Load the JSON File


#We use glob to automatically find the JSON file in the data/ folder
json_files = glob.glob("data/trends_*.json")

#If no file is found, stop the script and show an error
if len(json_files) == 0:
    print("ERROR: No JSON file found in data/ folder.")
    print("Please run task1_data_collection.py first.")
    exit()

#Pick the most recent file (in case there are multiple)
json_file = sorted(json_files)[-1]

#Load the JSON file into a Pandas DataFrame
#A DataFrame is like an Excel table — rows and columns
df = pd.read_json(json_file)

#Print how many rows (stories) were loaded
print(f"Loaded {len(df)} stories from {json_file}")
print()  # blank line for readability

# STEP 2 — Clean the Data


# ── Fix 1: Remove Duplicate Stories ──
# Some stories might appear twice with the same post_id
# We keep only the first occurrence and drop the rest
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# ── Fix 2: Remove Rows With Missing Values ──
# If a story is missing post_id, title, or score it's useless to us
# dropna means "drop rows where these columns have no value"
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# ── Fix 3: Fix Data Types ──
# score and num_comments should be whole numbers (integers)
# Sometimes they come in as decimals like 45.0 — we fix that here
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# ── Fix 4: Remove Low Quality Stories ──
# Stories with a score less than 5 are not trending — remove them
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")
print()  # blank line

# ── Fix 5: Clean Whitespace From Titles ──
# Some titles might have extra spaces at the start or end
# .str.strip() removes those extra spaces
df["title"] = df["title"].str.strip()

# STEP 3 — Save as CSV


# Make sure the data/ folder exists (it should already from Task 1)
os.makedirs("data", exist_ok=True)

# Save the cleaned DataFrame to a CSV file
# index=False means don't add an extra numbered column at the start
csv_file = "data/trends_clean.csv"
df.to_csv(csv_file, index=False)

# Print confirmation
print(f"Saved {len(df)} rows to {csv_file}")
print()

# STEP 4 — Print Summary by Category

# value_counts() counts how many stories are in each category
# sort_index() sorts them alphabetically
category_summary = df["category"].value_counts().sort_index()

print("Stories per category:")
for category, count in category_summary.items():
    # We use ljust(15) to align the numbers neatly in a column
    print(f"  {category.ljust(15)} {count}")