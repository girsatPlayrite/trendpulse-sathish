# Task 3 — Analysis with Pandas and NumPy
# We load the clean CSV from Task 2, explore it,
# compute statistics, add new columns, and save the result

import pandas as pd    # for working with tables of data
import numpy as np     # for mathematical calculations

# STEP 1 — Load and Explore the Data


# Load the clean CSV file that Task 2 created
df = pd.read_csv("data/trends_clean.csv")

# Print the shape — shape means (number of rows, number of columns)
print(f"Loaded data: {df.shape}")
print()

# Print the first 5 rows so we can see what the data looks like
print("First 5 rows:")
print(df.head())
print()

# Calculate and print the average score and average comments
# .mean() adds all values and divides by count — that is the average
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")
print()

# STEP 2 — Basic Analysis with NumPy

print("--- NumPy Stats ---")

# Convert the score column to a NumPy array so we can use NumPy functions
scores = np.array(df["score"])

# Mean = average of all scores
mean_score = np.mean(scores)

# Median = the middle value when all scores are sorted
median_score = np.median(scores)

# Standard deviation = how spread out the scores are from the average
std_score = np.std(scores)

# Max and min scores
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")
print()

# Which category has the most stories?
# value_counts() counts stories per category
# idxmax() returns the category name with the highest count
top_category       = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()

print(f"Most stories in: {top_category} ({top_category_count} stories)")
print()

# Which story has the most comments?
# idxmax() returns the row index of the highest num_comments value
most_commented_index = df["num_comments"].idxmax()

# Use that index to get the full row
most_commented_story = df.loc[most_commented_index]

print(f"Most commented story: \"{most_commented_story['title']}\"")
print(f"  — {most_commented_story['num_comments']} comments")
print()

# STEP 3 — Add Two New Columns

# New column 1: engagement
# Formula: num_comments divided by (score + 1)
# We add 1 to score so we never divide by zero
# This tells us how much discussion a story gets per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Round engagement to 2 decimal places so it looks clean
df["engagement"] = df["engagement"].round(2)

# New column 2: is_popular
# True if the story's score is above the average score, False if not
# avg_score was already calculated above in Step 1
df["is_popular"] = df["score"] > avg_score

# Print a quick preview to confirm the new columns were added
print("Preview with new columns:")
print(df[["title", "score", "engagement", "is_popular"]].head())
print()

# STEP 4 — Save the Result

# Save the updated DataFrame to a new CSV file
# index=False means don't add an extra numbered column at the start
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"Saved to {output_file}")