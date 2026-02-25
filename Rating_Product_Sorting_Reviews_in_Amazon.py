
###################################################
# Business Problem
###################################################

# One of the most critical problems in e-commerce is the accurate calculation of product ratings after sales.
# Solving this problem leads to increased customer satisfaction for the e-commerce platform, 
# better visibility for sellers, and a seamless shopping experience for buyers. 
# Another challenge is the accurate sorting of product reviews. Since misleading reviews 
# can directly affect product sales, they can cause both financial and customer loss. 
# By solving these two fundamental problems, e-commerce platforms and sellers will increase their sales, 
# while customers will complete their purchasing journey without issues.

###################################################
# Dataset Story
###################################################

# This dataset contains Amazon product data, including various metadata and product categories.
# It features user ratings and reviews for the most reviewed product in the Electronics category.

# Variables:
# reviewerID: Unique User ID
# asin: Unique Product ID
# reviewerName: Username
# helpful: Degree of helpfulness of the review
# reviewText: The content of the review
# overall: Product rating (1-5)
# summary: Review summary
# unixReviewTime: Review time (unix timestamp)
# reviewTime: Review time (raw format)
# day_diff: Number of days passed since the review
# helpful_yes: Number of times the review was found helpful
# total_vote: Total number of votes given to the review


import matplotlib.pyplot as plt
import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', 10)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

###################################################
# TASK 1: Calculate Average Rating Based on Recent Reviews and Compare with Existing Average Rating.
###################################################

# In the shared dataset, users have provided ratings and reviews for a product.
# Our goal in this task is to evaluate the ratings by weighting them according to their dates.
# The initial average rating must be compared with the time-weighted average rating obtained.


###################################################
# Step 1: Read the Dataset and Calculate the Average Rating of the Product.
###################################################

df = pd.read_csv("Modül_3_Ölçümleme_Problemleri/datasets/amazon_review.csv")
df["overall"].mean()

df.head()

###################################################
# Step 2: Calculate the Time-Weighted Average Rating.
###################################################

# Exploring ratings by quartiles of recency (day_diff)
df.loc[df["day_diff"] <= df["day_diff"].quantile(0.25), "overall"].mean() # 4.696
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.25)) & (df["day_diff"] <= df["day_diff"].quantile(0.50)), "overall"].mean() # 4.64
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.50)) & (df["day_diff"] <= df["day_diff"].quantile(0.75)), "overall"].mean() # 4.57
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.75)), "overall"].mean() # 4.45


# Function to determine time-based weighted averages
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.25), "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.25)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.50)), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.50)) & (dataframe["day_diff"] <= dataframe["day_diff"].quantile(0.75)), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > dataframe["day_diff"].quantile(0.75)), "overall"].mean() * w4 / 100


time_based_weighted_average(df, w1=28, w2=26, w3=24, w4=22) # 4.59559316512811

df["overall"].mean() # 4.58


###################################################
# Task 2: Determine the Top 20 Reviews to be Displayed on the Product Detail Page.
###################################################


###################################################
# Step 1. Generate the helpful_no Variable
###################################################

# Note:
# total_vote is the total number of up-down votes given to a review.
# "up" means helpful_yes.
# Since "helpful_no" does not exist in the dataset, it must be generated from existing variables.


df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

df = df[["reviewerName", "overall", "summary", "helpful_yes", "helpful_no", "total_vote", "reviewTime"]]

df.head()

###################################################
# Step 2. Calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound Scores
###################################################

def wilson_lower_bound(up, down, confidence=0.95):
    """
    Calculate Wilson Lower Bound Score

    - The lower bound of the confidence interval calculated for the Bernoulli parameter p 
      is accepted as the WLB score.
    - The calculated score is used for product/review ranking.
    - Note:
    If the scores are between 1-5, they can be mapped to 1-3 as negative and 4-5 as positive 
    to fit the Bernoulli distribution. This may bring some limitations; in such cases, 
    Bayesian Average Rating might be preferred.

    Parameters
    ----------
    up: int
        Upvote count (helpful_yes)
    down: int
        Downvote count (helpful_no)
    confidence: float
        Confidence level (default 0.95)

    Returns
    -------
    wilson score: float
    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


def score_up_down_diff(up, down):
    return up - down


def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)

#####################
# score_pos_neg_diff
#####################

df["score_pos_neg_diff"] = df.apply(lambda x: score_up_down_diff(x["helpful_yes"], x["helpful_no"]), axis=1)
# df.sort_values("score_pos_neg_diff", ascending=False).head(20)


#####################
# score_average_rating
#####################
df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)
# df.sort_values("score_average_rating", ascending=False).head(20)


#####################
# wilson_lower_bound
#####################
df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)
# df.sort_values("wilson_lower_bound", ascending=False).head(20)


##################################################
# Step 3. Identify the Top 20 Reviews and Interpret the Results.
###################################################

df.sort_values("wilson_lower_bound", ascending=False).head(20)