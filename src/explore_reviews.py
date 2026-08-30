import pandas as pd

# Load the reviews table
reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

print("Shape (rows, columns):", reviews.shape)

print("\nColumns:")
print(reviews.columns.tolist())

# Distribution of review scores (1 to 5 stars)
print("\nReview score counts:")
print(reviews["review_score"].value_counts().sort_index())

# A couple of example review messages
print("\nExample review messages:")
print(reviews["review_comment_message"].dropna().head(3).tolist())
