# Clustering r/NBA post Titles

by Lucas Churchman

## The Problem

On many subreddits, posts can be labeled by what "type" post they are which can be helpful for finding specific types of content you're interested in finding. However, these labels are often unreliable. Take the NBA subreddit for example.
<br>
<br>
<br>

- A post can be tagged as a "rostermove" even if it's just speculating on such an event

![beal1](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealrostermove.png)
<br>
<br>
<br>



- However a post about the same player, when they *actually* sign a contract can go untagged (the majority posts go untagged even if they easily fall under an existing label)


![beal2](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealnotag.png)
<br>
<br>
<br>

- Also, even when posts do have tags, they are often miscategorized entirely. The "highlights" tag is supposed to be used for highlights from games, but here it was applied simply because the submission was a video link

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/whyhighlight.png)
<br>
<br>
<br>

- Another point of confusion is the existience of the "discussion" tag since any comment thread on Reddit can be considered a discussion whether the post is of a highlight, trade news, speculation, etc.

- Roughly 80-90% of posts aren't tagged at all. This combined with Reddit's questionable search functionality, makes finding a specific post, even if you know how it *should* be tagged, impossible at times.

Because of the inconsitencies of post tagging, I hope to find structure in the titles of posts to see if a better tagging systyem could be implemented.

## Data
The data used was generated from [this](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_05?pli=1) database on Google BigQuery. Many columns are available database, but only a few were needed here.

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bigquerytable.png)

where `link_flair_css_class` is the posts' tag type.

A query for posts from January 2018 through August 2019 generated a table of over 500,000 post titles, where about 70,000 were tagged.

## EDA

![postsbytype](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/PostsByType.png)

![barstats](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/BarStats.png)

## Conclusions
  -Probably a problem better suited for topic modeling (looking at keywords rather than similarity)
  -Could be several text-preprocessing options that weren't explored.
