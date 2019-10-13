SELECT
  *
FROM
  [fh-bigquery:reddit_comments.2016_01],
  [fh-bigquery:reddit_comments.2016_02],
  [fh-bigquery:reddit_comments.2016_03],
  [fh-bigquery:reddit_comments.2016_04],
  [fh-bigquery:reddit_comments.2016_05],
  [fh-bigquery:reddit_comments.2016_06],
  [fh-bigquery:reddit_comments.2016_07],
  [fh-bigquery:reddit_comments.2016_09],
  [fh-bigquery:reddit_comments.2016_10],
  [fh-bigquery:reddit_comments.2016_11],
  [fh-bigquery:reddit_comments.2016_01],
  [fh-bigquery:reddit_comments.2016_02],
  [fh-bigquery:reddit_comments.2016_03],
  [fh-bigquery:reddit_comments.2016_04],
  [fh-bigquery:reddit_comments.2016_05],
  [fh-bigquery:reddit_comments.2016_06],
  [fh-bigquery:reddit_comments.2016_07],
  [fh-bigquery:reddit_comments.2016_09],
  [fh-bigquery:reddit_comments.2016_10],
  [fh-bigquery:reddit_comments.2017_11],
  [fh-bigquery:reddit_comments.2018_12],
  [fh-bigquery:reddit_comments.2018_01],
  [fh-bigquery:reddit_comments.2018_02],
  [fh-bigquery:reddit_comments.2018_03],
  [fh-bigquery:reddit_comments.2018_04],
  [fh-bigquery:reddit_comments.2018_05],
  [fh-bigquery:reddit_comments.2018_06],
  [fh-bigquery:reddit_comments.2018_07],
  [fh-bigquery:reddit_comments.2018_09],
  [fh-bigquery:reddit_comments.2018_10],
  [fh-bigquery:reddit_comments.2018_11],
  [fh-bigquery:reddit_comments.2018_12],
  [fh-bigquery:reddit_comments.2019_01],
  [fh-bigquery:reddit_comments.2019_02],
  [fh-bigquery:reddit_comments.2019_03],
  [fh-bigquery:reddit_comments.2019_04],
  [fh-bigquery:reddit_comments.2019_05],
WHERE 
  subreddit IN ('Mavericks', 'denvernuggets','warriors',
                'rockets', 'laclippers', 'lakers', 'memphisgrizzlies',
                'timberwolves', 'nolapelicans', 'thunder', 'suns',
                'ripcity', 'kings', 'nbaspurs', 'utahjazz',
                'atlantahawks', 'bostonceltics', 'gonets', 'charlottehornets',
                'chicagobulls', 'clevelandcavs', 'detroitpistons', 'pacers', 
                'heat', 'mkebucks', 'nyknicks', 'orlandomagic', 'sixers', 
                'torontoraptors', 'washingtonwizards')
                