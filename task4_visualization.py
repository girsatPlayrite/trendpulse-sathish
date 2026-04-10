# Task 4 — Visualizations
# We load the analysed CSV from Task 3 and create 3 charts
# plus a combined dashboard. Everything is saved as PNG files.

import pandas as pd                 # for loading and working with data
import matplotlib.pyplot as plt     # for creating charts
import matplotlib.patches as mpatches  # for creating legend items
import os                           # for creating folders

# STEP 1 — Setup

# Load the analysed CSV from Task 3
df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} rows from data/trends_analysed.csv")

# Create the outputs/ folder if it doesn't exist
# exist_ok=True means don't crash if it already exists
os.makedirs("outputs", exist_ok=True)

# STEP 2 — Chart 1: Top 10 Stories by Score

# Sort stories by score from highest to lowest
# then take only the top 10
top10 = df.sort_values("score", ascending=False).head(10)

# Shorten any title that is longer than 50 characters
# This stops long titles from overflowing the chart
top10 = top10.copy()  # copy to avoid a pandas warning
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "..." if len(t) > 50 else t
)
# ↑ lambda is a mini function — if title is over 50 chars, cut it and add "..."

# Create a new figure with a specific size (width=10, height=6 inches)
plt.figure(figsize=(10, 6))

# Create a horizontal bar chart
# barh means horizontal bars — titles on y axis, scores on x axis
plt.barh(top10["short_title"], top10["score"], color="steelblue")

# Invert the y axis so the highest score appears at the top
plt.gca().invert_yaxis()

# Add title and axis labels
plt.title("Top 10 Stories by Score", fontsize=14)
plt.xlabel("Score")
plt.ylabel("Story Title")

# tight_layout makes sure nothing gets cut off
plt.tight_layout()

# IMPORTANT: always savefig BEFORE show
plt.savefig("outputs/chart1_top_stories.png")
plt.close()  # close the figure to free memory

print("Saved: outputs/chart1_top_stories.png")

# STEP 3 — Chart 2: Stories per Category

# Count how many stories are in each category
category_counts = df["category"].value_counts()

# Define a different colour for each bar
colors = ["steelblue", "coral", "mediumseagreen", "mediumpurple", "goldenrod"]

# Create a new figure
plt.figure(figsize=(8, 5))

# Create a vertical bar chart
# category names on x axis, counts on y axis
plt.bar(category_counts.index, category_counts.values, color=colors)

# Add title and axis labels
plt.title("Number of Stories per Category", fontsize=14)
plt.xlabel("Category")
plt.ylabel("Number of Stories")

# Rotate x axis labels slightly so they don't overlap
plt.xticks(rotation=15)

plt.tight_layout()

# Save before show
plt.savefig("outputs/chart2_categories.png")
plt.close()

print("Saved: outputs/chart2_categories.png")

# STEP 4 — Chart 3: Score vs Comments Scatter Plot

# Split data into popular and non-popular stories
# using the is_popular column we created in Task 3
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create a new figure
plt.figure(figsize=(8, 5))

# Plot non-popular stories as blue dots
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="steelblue",
    alpha=0.6,        # alpha controls transparency — 0 is invisible, 1 is solid
    label="Not Popular"
)

# Plot popular stories as orange dots
plt.scatter(
    popular["score"],
    popular["num_comments"],
    color="coral",
    alpha=0.8,
    label="Popular"
)

# Add title and axis labels
plt.title("Score vs Number of Comments", fontsize=14)
plt.xlabel("Score")
plt.ylabel("Number of Comments")

# Add a legend so we know which colour is which
plt.legend()

plt.tight_layout()

# Save before show
plt.savefig("outputs/chart3_scatter.png")
plt.close()

print("Saved: outputs/chart3_scatter.png")

# STEP 5 — BONUS: Combined Dashboard

# Create one big figure with 1 row and 3 columns of subplots
# figsize makes it wide enough to fit all 3 charts side by side
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Add an overall title to the whole dashboard
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold")

# ── Dashboard Chart 1: Top 10 Stories ──
axes[0].barh(top10["short_title"], top10["score"], color="steelblue")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].tick_params(axis="y", labelsize=7)  # make y labels smaller to fit

# ── Dashboard Chart 2: Stories per Category ──
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=15)

# ── Dashboard Chart 3: Scatter Plot ──
axes[2].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="steelblue",
    alpha=0.6,
    label="Not Popular"
)
axes[2].scatter(
    popular["score"],
    popular["num_comments"],
    color="coral",
    alpha=0.8,
    label="Popular"
)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

# tight_layout with rect leaves space for the big title at the top
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the dashboard
plt.savefig("outputs/dashboard.png")
plt.close()

print("Saved: outputs/dashboard.png")
print()
print("All charts saved successfully!")