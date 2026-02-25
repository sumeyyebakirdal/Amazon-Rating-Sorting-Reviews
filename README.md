# Amazon Rating Product & Sorting Reviews

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-v1.3+-green)
![Statistics](https://img.shields.io/badge/Focus-Wilson_Lower_Bound-red)

## 📌 Business Problem
In the world of e-commerce, two problems stand out in terms of customer trust and conversion:
1. **Accurate Product Rating:** Simple averages can be misleading as they ignore the "recency" of feedback. A product's quality might change over time.
2. **Review Sorting:** Displaying the most "helpful" reviews first is crucial. If misleading or unhelpful reviews dominate the top of the page, it leads to customer dissatisfaction and financial loss.

This project implements advanced statistical methods to solve these challenges using a real-world Amazon Electronics dataset.

---

## 📂 Dataset Story
The dataset contains user ratings and reviews for one of the most commented products in the Amazon Electronics category.

* **Dataset Source:** [Kaggle - Amazon Review Dataset](https://www.kaggle.com/code/mehmetisik/rating-product-sorting-reviews-in-amazon)
* **Variables:**
    * `overall`: Product rating (1-5).
    * `reviewerID`: Unique user ID.
    * `day_diff`: Days passed since the review.
    * `helpful_yes`: Number of "helpful" votes.
    * `total_vote`: Total number of votes (up + down) for the review.

---

## 🛠️ Project Roadmap

### 1. Time-Based Weighted Average Rating
Instead of a simple arithmetic mean, we apply weights based on how recently the review was written. 
* We divided the `day_diff` into four quartiles.
* Recent reviews were given higher weights (e.g., 28% for the most recent vs. 22% for the oldest).
* **Result:** This ensures that the current quality of the product is better reflected in the score.



### 2. Sorting Reviews (The Search for the "Best" Review)
We compared three different scoring methods to determine which reviews should be displayed first:

* **Score Up-Down Difference:** `Upvotes - Downvotes`. (Fails when volume is low).
* **Average Rating Score:** `Upvotes / Total Votes`. (Fails when a review has only 1 vote/1 upvote).
* **Wilson Lower Bound (WLB):** Provides a 95% confidence interval for the true proportion of positive votes and uses the lower bound as the ranking score.



---

## 📊 Why Wilson Lower Bound?
WLB is the "Gold Standard" for ranking. 
* **Scenario:** Review A has 600 upvotes and 400 downvotes (60% positive). Review B has 5 upvotes and 0 downvotes (100% positive).
* **WLB Logic:** WLB will rank Review A higher because the sample size (1000 votes) provides much more statistical certainty than Review B's small sample size, even though B has a higher percentage.

---
