# Clustering r/NBA post Titles

by Lucas Churchman

## The Problem

On many subreddits, posts can be labeled by what "type" post they are which can be helpful for finding specific types of content you're interested in finding. However, these labels are often unreliable. Take the NBA subreddit for example.

- A post can be tagged as a "rostermove" even if it's just speculating on such an event

![beal1](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealrostermove.png)
<br>
<br>
<br>



- However a post about the same player, when they ACTUALLY sign a contract can go untagged (the majority posts go untagged even if they easily fall under an existing label)


![beal2](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealnotag.png)
<br>
<br>
<br>

- Also, even when posts do have tags, they are often miscategorized entirely. The "highlights" tag is supposed to be used for highlights from games, but here it was applied simply because the submission was a video link

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/whyhighlight.png)
<br>
<br>
<br>

Furthermore, the difference in posts that should be tagged as "news" versus "rostermoves" versus "discussion" is vague at times.

Because all of these inconsistencies in tagging, I'm going to explore if the **language** used in post titles is consistent enough to cluster together using Kmeans. If so, a better automated tagging or possible title generation system could be used for r/NBA and other subreddits.

## Data
The data used was generated from [this](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_05?pli=1) database on Google BigQuery. Many columns are available database, but only a few were needed here.

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bigquerytable.png)

where `link_flair_css_class` is the posts' tag type.

A query for posts from January 2018 through August 2019 created a table of 517,547 post titles, although this was further narrowed down later.
