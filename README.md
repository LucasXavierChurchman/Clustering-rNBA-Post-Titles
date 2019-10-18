# Clustering r/NBA post Titles

by Lucas Churchman

## The Problem

On many subreddits, posts can be labeled by what "type" post they are which can be helpful for finding specific types of content you're interested in finding. However, these labels are often unreliable. Take the NBA subreddit for example.
<br>
<br>
<br>

- A post can be tagged as a 'Rostermove' even if it's just speculating on such an event

![beal1](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealrostermove.png)
<br>
<br>
<br>



- However a post about the same player, when they *actually* sign a contract can go untagged (the majority posts go untagged even if they easily fall under an existing label)


![beal2](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealnotag.png)
<br>
<br>
<br>

- Also, even when posts do have tags, they are often miscategorized entirely. The 'Highlights' tag is supposed to be used for highlights from games, but here it was applied simply because the submission was a video link

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/whyhighlight.png)
<br>
<br>
<br>

- Roughly 80-90% of posts aren't tagged at all. This combined with Reddit's questionable search functionality, makes finding a specific post, even if you know how it *should* be tagged, impossible at times.

Because of the inconsitencies of post tagging, I hope to find structure in the post titles to see if a better tagging systyem could be implemented to better identify and filter posts

## Data
The data used was generated from [this](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_05?pli=1) database on Google BigQuery. Many columns are available database, but only a few were needed here.

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bigquerytable.png)

where `link_flair_css_class` is the posts' tag type.

A query for posts from January 2018 through August 2019 generated a table of over 500,000 post titles, where about 70,000 were tagged.

## EDA

It wouldn't make sense to attempt to tag posts based on their title if posts that already do have tags don't have a consistent structure already. So, for this analysis, we'll look at posts with these tags for these reasons:

- Highlights: Similar language is used to describe highlight clips
- Game Thread: Follow a consistent structure, title prefixed by "GAME THREAD". Should nearly trivial to cluster.
- Postgame Thread: Similar as above
- News: Often prefixed with the article/tweet authors name, use similar buzz words
- Discussion: Often phrased as a question
- Roster Moves: Use similar language, use city names more often and use words like "deal" and "negotiate" often

![postsbytype](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/PostsByType.png)
- Highlights are far and away the most used type tag. This probably because almost any video posted gets this tag whether it's actually a highlight clip or instead an interview, postgame conference etc. along with the fact that people like watching and sharing highlights. 
- Similarly, any text article seems to automatically tagged as news, so it makes sense that would be the runner up. 
- Game and postgame threads having similar counts makes sense because there's only so many games per year. Not a perfect 1-to-1 ratio since postgame threads are auto-generated but game threads are usually user submitted.

<br>
<br>
<br>

![barstats](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/BarStats.png)
- Originally when generating this plot, every type of post had title of over 200 words; curious since the maximum title length allowed on reddit is 300 characters. These outliers were omitted and this is the reason highlights, news, discussion, and roster moves all have a maximum length of 41 words.
- Logical that game threads and postgame threads have the lowest standard deviation because of their consistent structure.
- News having the highest average title length seems to make sense headlines have to pack in a lot of information for the space they're given.

## Analysis

As with all NLP problems, the text went through a pre-processing pipeline. Here the (fairly standard) process was:

- Casting to lower case
- Removing punctation
- Stemming (Lemmatization was tried as well, but had better results with stemming)
- Removed numbers (Important because 100 points in a box score is a lot different than 100 million dollars when talking about a contract)

It's also important to mention count vectorization was used instead of a tf-idf matrix as it gave better results. 

Dimensionality reduction was done with SVD

![svd](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/SVDCumulativeVariance.png)

800 features were decied to be used. Just around the 90% explained variance mark and a signifcant decrease from our original 7500 features (words).

The feature reduced model was fit with K-Means with k=6, hoping the original 6 types of posts would appear as their own cluster. 

![silhouette](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/Silhouette.png)

Posts per label:

| Label |Count |
|-------|------|
| 5     | 4074 |
| 2     | 3213 |
| 0     | 2587 |
| 3     | 2334 |
| 1     | 1684 |
| 4     | 1108 |

As you can see, clusters 0 and 3 have fairly well defined structure (these are the game and post game clusters, which was expected), and the only reason the average silhouette score is just above 0, indicating some amount of cluster definition overall (silhouette scores range from -1 to 1). However, without these types of posts, the clusters would have little no structure at all.



## Conclusions
  - The posts that are often generated by bots (Game Thread, Postgame Thread) were obviously the most easy to identify and cluster together.
  - Could be several text-preprocessing options that weren't explored. A big one would be converting names all to the same word or adding all names to stop words. Would probably help identify Roster news and Highlight posts easier.
  - Probably a problem better suited for topic modeling (looking at keywords rather than vector similarity)
  
