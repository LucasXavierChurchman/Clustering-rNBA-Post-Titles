# Clustering r/NBA Post Titles
### Exploring Alternatives to the Current Reddit Tagging System
![banner](https://github.com/LucasXavierChurchman/Clustering-rNBA-Post-Titles/blob/master/images/reddit-banner.jpg)

by Lucas Churchman

## The Problem

On many subreddits, posts can be labeled by what "type" post they are which can be helpful for finding specific types of content you're interested in finding. However, these labels are often unreliable. Take the NBA subreddit for example.
<br>
<br>
<br>

- A post can be tagged as a 'Roster Move' even if it's just speculating on such an event

![beal1](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealrostermove.png)
<br>
<br>
<br>


- However a post about the same player, when they *actually* sign a contract can go untagged (the majority posts go untagged even if they easily fall under an existing label).


![beal2](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealnotag.png)
<br>
<br>
<br>

- Also, even when posts do have tags, they are often miscategorized entirely. The 'Highlights' tag is supposed to be used for highlights from games, but here it was applied simply because the submission was a video link.

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/whyhighlight.png)
<br>
<br>
<br>

- Roughly 80-90% of the posts aren't tagged at all. This combined with Reddit's questionable search functionality, makes finding a specific post, even if you know how it *should* be tagged, impossible at times.

Because of these inconsistencies in these post taggings, I hope to find some sort of consistency in post title structure to see if a better tagging system could be implemented to better classify and filter posts.

## Data
The data used was generated from [this](https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2015_05?pli=1) database on Google BigQuery. Many columns are available on this database, but only a few were needed here.

![BQTable](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bigquerytable.png)

where `link_flair_css_class` is the posts' tag type.

A query for posts from January 2018 through August 2019 generated a table of over 500,000 post titles, where about 70,000 were tagged.

## EDA

It wouldn't make sense to attempt to tag posts based on their title if posts that already do have tags don't have a consistent structure. So, for this analysis, we'll look at posts with these tags for these reasons:

- Highlights: Similar, 'exciting' language is used to describe highlight clips.
- Game Thread: Follow a consistent structure, title prefixed by "GAME THREAD". Should nearly trivial to cluster together.
- Post Game Thread: Similar as above.
- News: Often prefixed with the article/tweet authors name, use similar buzz words.
- Discussion: Often phrased as a question.
- Roster Moves: Use similar language, use city names more often and use words like "deal" and "negotiate" often.

The initial hypothesis is that these first there will generate distinct clusters while the latter 3 will be less distinct.

![postsbytype](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/PostsByType.png)
- Highlights are far and away the most used tag type. This probably because almost any video posted gets this tag whether it's actually a highlight clip or instead an interview, postgame conference etc. along with the fact that people like watching and sharing highlights. 
- Similarly, any text article/tweet seems to automatically tagged as news, so it makes sense that would be the runner up. 
- Game and postgame threads having similar counts makes sense because there's only so many games per year. Not a perfect 1-to-1 ratio since postgame threads are auto-generated but game threads are usually user submitted.

<br>
<br>
<br>

![barstats](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/BarStats.png)
- Originally when generating this plot, every type of post had a title with over 200 words; curious since the maximum title length allowed on reddit is 300 characters. These outliers were omitted and this is the reason highlights, news, discussion, and roster moves all have a maximum length of 41 words.
- Logical that game threads and postgame threads have the lowest standard deviation because of their consistent structure.
- News having the highest average title length seems to make sense headlines have to pack in a lot of information for the space they're given.

## Analysis

As with all NLP problems, the text went through a pre-processing pipeline. Here the (fairly standard) process was:

- Casting to lowercase
- Removing punctuation
- Stemming (Lemmatization was tried as well, but had better results with stemming)
- Removed numbers (Important because 100 points in a box score is a lot different than 100 million dollars when talking about a contract)

It's also important to mention count vectorization was used instead of a tf-idf matrix as it gave better results. 

Dimensionality reduction was done with SVD.

![svd](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/SVDCumulativeVariance.png)

800 features were decided to be used. Just around the 90% explained variance mark and a significant decrease from our original 7500 features (words).

The feature reduced model was fit with K-Means with k=6, hoping the original 6 types of posts would appear as their own cluster. 

![silhouette](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/Silhouette.png)

As you can see, clusters 0 and 3 have fairly well defined structure (these are the game and post game clusters, which was expected), and the only reason the average silhouette score is just above 0, indicating some amount of cluster definition overall (silhouette scores range from -1 to 1). However, without these types of posts, the clusters would have little to no overall structure at all.

![clustermap](https://github.com/LucasXavierChurchman/Capstone2/blob/master/plots/ClusterMap.png)

This cluster map gives a sense of how close the centers of each cluster are in the original feature space. The larger the circle, the more members in that cluster. Because this is only being plotted on two partial components, the circle sizes aren't a 1-to-1 representation of membership as indicated by the key on the bottom left.

Posts per label:

| Label |Count |
|-------|------|
| 5     | 4074 |
| 2     | 3213 |
| 0     | 2587 |
| 3     | 2334 |
| 1     | 1684 |
| 4     | 1108 |

Even though this was an unsupervised model, it's helpful to look at how the model clustered compared to how they were tagged on Reddit.

| index | cluster label | type on reddit | title                                                                                                                                                                                                   |
| ----- | ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4640  | 0             | gamethread     | GAME THREAD: Toronto Raptors (2-2) @ Milwaukee Bucks (2-2) - (May 23, 2019)                                                                                                                             |
| 3764  | 0             | gamethread     | GAME THREAD: Minnesota Timberwolves (30-18) @ LA Clippers (23-22) - (January 22, 2018)                                                                                                                  |
| 4454  | 0             | gamethread     | GAME THREAD: Brooklyn Nets (40-40) @ Indiana Pacers (47-33) - (April 07, 2019)                                                                                                                          |
| 3047  | 0             | gamethread     | GAME THREAD: Minnesota Timberwolves (30-18) @ LA Clippers (23-22) - (January 22, 2018)                                                                                                                  |
| 2635  | 0             | gamethread     | GAME THREAD: Dallas Mavericks (27-37) @ Orlando Magic (30-36) - (March 08, 2019)                                                                                                                        |
| 14118 | 1             | rostermoves    | The Blazers should do whatever it takes to sign Rudy Gay                                                                                                                                                |
| 12550 | 1             | rostermoves    | [Wojnarowski] Golden State is moving Shabazz Napier, Treveon Graham and cash onto Minnesota, league sources tell ESPN. Napier and Graham are part of the D'Angelo Russell sign-and-trade.               |
| 9456  | 1             | news           | [Nicholas] “I’m shocked, SHOCKED to find gambling going on here.” (sigh) Seriously someone needs to explain to me why the NBA still has tampering rules. No one follows them. Can’t we just move on?    |
| 13105 | 1             | rostermoves    | [Daryl Morey] "The fit we envisioned when Carmelo chose to sign with the Rockets has not materialized, therefore we thought it was best to move on as any other outcome would have been unfair to him." |
| 9936  | 1             | news           | [Amick] The Kings have extended a qualifying offer to Willie Cauley-Stein, a source with knowledge tells @TheAthletic, making him a restricted free agent.                                              |
| 10028 | 2             | discussion     | DeMar DeRozan is one of the biggest playoff chokers of this decade and that’s backed by stats                                                                                                           |
| 17    | 2             | highlights     | Hornets GM Mitch Kupchak on Kemba's comments about taking less than the supermax: "I don't know if his representatives approved of that comment, but I guess we'll find out."                           |
| 14633 | 2             | rostermoves    | Predicting where all the 2019 free agents sign                                                                                                                                                          |
| 12428 | 2             | discussion     | Using the NBA's Stats website, how to you figure out what percentile a player is in for a given category?                                                                                               |
| 9495  | 2             | news           | The #sixers shot 30.2% on uncontested field goal attempts last night. Thirty point two percent. Had 25 3pta with 4+ feet of space, shot just 24% on them.                                               |
| 7318  | 3             | postgamethread | [Serious Next Day Thread] The Boston Celtics defeat the Philadelphia 76ers, 101-98                                                                                                                      |
| 6955  | 3             | postgamethread | [Post Game Thread] The Los Angeles Clippers (30-26) defeat the Boston Celtics (40-19), 129-119.                                                                                                         |
| 5524  | 3             | postgamethread | [Post Game Thread] The Boston Celtics (50-23) defeat the Sacramento Kings (24-50) 104-93 behind Terry Rozier's 33 points                                                                                |
| 5572  | 3             | postgamethread | [Post Game Thread] The Los Angeles Clippers (15-19) defeat the Charlotte Hornets (13-22) 108-105Post Game Thread                                                                                        |
| 5453  | 3             | postgamethread | [Post Game Thread] Lakers (34-44) defeat the (45-34) Spurs 122-112 behind Kuzma's 33pts, sweeping them this season                                                                                      |
| 11171 | 4             | discussion     | [ESPNStatsInfo] Joel Embiid and Ben Simmons combined for 30 points in the 1st half, 2 shy of the Pistons' entire team. Philly's 30-point halftime lead is the team's largest since 2012.                |
| 10140 | 4             | discussion     | How do I check what someone's stats look like when they are on the floor with a specific player... and when they are playing when a specific player is on the bench?                                    |
| 12350 | 4             | discussion     | Of all the superstars/stars this season wih the qualifying MVP stats, James Harden needs the most help, so therefore.....                                                                               |
| 1861  | 4             | highlights     | One of the most embarrassing late game sequences in the fourth quarter                                                                                                                                  |
| 14099 | 4             | rostermoves    | [Wojnarowski] Source: Memphis sent $1.5M in cash to Kings in Garrett Temple trade --- which is the equivalent of Deyonta Davis' salary. If Kings waive him, Grizzlies covered the cost                  |
| 270   | 5             | highlights     | Bradley Beal 34 Pts and John Wall 25 Pts Full Highlights vs Grizzlies (2018.01.05)                                                                                                                      |
| 13387 | 5             | rostermoves    | NBA free agency rumors: Cavaliers hoping to re-sign Jeff Green | NBA                                                                                                                                    |
| 252   | 5             | highlights     | LeBron creates his own lane, then hammers it home                                                                                                                                                       |
| 12778 | 5             | rostermoves    | How LeBron, LA Lakers Can Claim a Top-4 Seed out West This Season                                                                                                                                       |
| 9906  | 5             | news           | [Charania] Los Angeles Lakers coach Luke Walton has been fined $15,000 for public comments on officiating Monday night.                                                                                 |
|       |

Game and postgame threads were clustered almost flawlessly while every other post type are scattered across all the other clusters. Another observation here is that the other clusters seem to be based somewhat on title length.

## Conclusions

  - The posts that are often generated by bots (Game Thread, Postgame Thread) were obviously the most easy to identify and cluster together.
  - Could try several other text-preprocessing options that weren't explored. A big one would be converting names all to the same word or adding all names to stop words. Would probably help identify Roster news and Highlight posts easier.
  - With the process here it's hard to determine whether this clustering is actually categorizing better than Reddit's poor tagging system or vice versa.
  - Probably a problem better suited for topic modeling or sentiment analysis instead of clustering. Possibly a combination of all 3.
  
## Bonus
My original goal was to train an RNN to generate title posts but didn't get far with it. Just for fun, here's some highlight titles generated using the pre-built `textgenrnn` package with 5 epochs and only 1000 samples:

-**Epoch 1:** "LeBron James on the same three on the same of the court to the comment on the shot to the shot on the game of the game of the game of the first court with a commeration on the game on the first poster of the game of the first play to the situation on the first court to the court to the game on the"

-**Epoch 3:** "DeMar DeRozan with the steal and the best clutch leading to the stand to the season and the confirms in the steal 
and the steal in the steal"

-**Epoch 5:** "LeBron James with a clutch for the NBA series after the steal of the first defensive props"
  



