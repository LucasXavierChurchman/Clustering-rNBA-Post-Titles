# Clustering r/NBA post Titles

by Lucas Churchman

## The Problem

On many subreddits, posts can be labeled by what "type" post they are which can be helpful for finding specific types of content you're interested in finding. However, these labels are often unreliable. In the NBA subreddit, a post can be tagged as a "rostermove" if it's speculating on a player signing a contract, 

for example:

![beal1](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealrostermove.png)
<br>
<br>
<br>



However a post about the same player, when they ACTUALLY sign a contract can go untagged (the majority posts go untagged even if they easily fall under an existing label)


![beal2](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/bealnotag.png)
<br>
<br>
<br>

Also, even when posts do have tags, they are often miscategorized entirely. The "highlights" tag is supposed to be used for highlights from games, but here it was applied simply because the submission was a video link

![notahighlight](https://github.com/LucasXavierChurchman/Capstone2/blob/master/images/whyhighlight.png)
<br>
<br>
<br>

Furthermore, the difference in posts that should be tagged as "news" versus "rostermoves" versus "discussion" is vague at times.

Because all of these inconsistencies, I'm going to explore if these posts can be clustered using K-Means using their titles.
