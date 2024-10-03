import praw
from collections import Counter

# Initialize the PRAW Reddit instance
reddit = praw.Reddit(
    client_id='63eRXo4ycPqIjQcmkiyh1Q',  # Replace with your client_id
    client_secret='XM43R1-yZmo1VOt8_HjJZdNk97mdfA',  # Replace with your client_secret
    user_agent='Greedy-Savings-9742',  # Replace with your user_agent
)

# Specify the subreddit you want to analyze
subreddit_name = "HubermanLab"  # Change to the subreddit you want to analyze
subreddit = reddit.subreddit(subreddit_name)

# Initialize a counter to track the number of comments by each user
user_activity = Counter()

# Fetch comments from the subreddit
print(f"Fetching comments from r/{subreddit_name}...")
for comment in subreddit.comments(limit=1000):  # Adjust limit as needed
    if comment.author is not None:
        user_activity[comment.author.name] += 1
    else:
        print("Skipping a comment with no author.")

# Fetch submissions from the subreddit
print(f"Fetching submissions from r/{subreddit_name}...")
for submission in subreddit.top(limit=1000):
    if submission.author:
        user_activity[submission.author.name] += 1

# Get the top 10 most active users
top_users = user_activity.most_common(10)

# Display the top 10 most active users along with their personal 'about' details
print("\nTop 10 most active users and their bios:")
for i, (username, count) in enumerate(top_users, 1):
    try:
        # Get the user's Redditor object
        redditor = reddit.redditor(username)

        # Fetch the user's 'about' bio (public description)
        user_bio = redditor.subreddit['public_description'] if hasattr(redditor, 'subreddit') and redditor.subreddit else "No bio available"

        # Display user information
        print(f"{i}. {username} - {count} interactions")
        print(f"   Bio: {user_bio}\n")

    except Exception as e:
        # Handle cases where the user might be deleted or the profile is inaccessible
        print(f"{i}. {username} - {count} interactions")
        print("   Bio: Unable to retrieve bio (user might be deleted or inaccessible)\n")