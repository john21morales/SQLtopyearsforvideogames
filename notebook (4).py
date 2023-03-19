#!/usr/bin/env python
# coding: utf-8

# # 1. The ten best-selling video games
# <p><img src="https://assets.datacamp.com/production/project_1413/img/video_game.jpg" alt="A video game player choosing a game to play on Nintendo Switch." width="400"></p>
# <p>Photo by <a href="https://unsplash.com/@retromoon">Dan Schleusser</a> on <a href="https://unsplash.com">Unsplash</a>.</p>
# <p>Video games are big business: the global gaming market is projected to be worth more than $300 billion by 2027 according to <a href="https://www.mordorintelligence.com/industry-reports/global-gaming-market">Mordor Intelligence</a>. With so much money at stake, the major game publishers are hugely incentivized to create the next big hit. But are games getting better, or has the golden age of video games already passed?</p>
# <p>In this project, we'll explore the top 400 best-selling video games created between 1977 and 2020. We'll compare a dataset on game sales with critic and user reviews to determine whether or not video games have improved as the gaming market has grown.</p>
# <p>Our database contains two tables. We've limited each table to 400 rows for this project, but you can find the complete dataset with over 13,000 games on <a href="https://www.kaggle.com/holmjason2/videogamedata">Kaggle</a>. </p>
# <h3 id="game_sales"><code>game_sales</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>game</code></td>
# <td>varchar</td>
# <td>Name of the video game</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>platform</code></td>
# <td>varchar</td>
# <td>Gaming platform</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>publisher</code></td>
# <td>varchar</td>
# <td>Game publisher</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>developer</code></td>
# <td>varchar</td>
# <td>Game developer</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>games_sold</code></td>
# <td>float</td>
# <td>Number of copies sold (millions)</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>Release year</td>
# </tr>
# </tbody>
# </table>
# <h3 id="reviews"><code>reviews</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>game</code></td>
# <td>varchar</td>
# <td>Name of the video game</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>critic_score</code></td>
# <td>float</td>
# <td>Critic score according to Metacritic</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>user_score</code></td>
# <td>float</td>
# <td>User score according to Metacritic</td>
# </tr>
# </tbody>
# </table>
# <p>Let's begin by looking at some of the top selling video games of all time!</p>

# In[19]:


get_ipython().run_cell_magic('sql', '', 'postgresql:///games\n\n-- We want to see the top 10 best selling video games of all time\nSELECT *\nFROM game_sales\nORDER BY games_sold DESC\nLIMIT 10;')


# # 2. Missing review scores
# <p>Wow, the best-selling video games were released between 1985 to 2017! That's quite a range; we'll have to use data from the <code>reviews</code> table to gain more insight on the best years for video games. </p>
# <p>First, it's important to explore the limitations of our database. One big shortcoming is that there is not any <code>reviews</code> data for some of the games on the <code>game_sales</code> table. </p>

# In[20]:


get_ipython().run_cell_magic('sql', '', '\n-- Since we are going to use reviews as a metric to judge the quality of games that year,\n-- We want to check the limitations of our database in terms of NULL review values.\n-- We check how many of the games that were included in both tables had NULL reviews.\nSELECT COUNT(*)\nFROM game_sales AS g\nLEFT JOIN reviews AS r\nON g.game = r.game\nWHERE r.critic_score IS NULL AND r.user_score IS NULL;')


# In[21]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (1, 1), \\\n    "The query should return just one value, a count of games where both critic_score and user_score are null."\n    assert results.columns.tolist() == ["count"], \\\n    \'The results should have just one column, called "count".\'\n    assert last_output.DataFrame().loc[0, \'count\'] == 31, \\\n    "There should be 31 games where both critic_score and user_score are null."')


# ## 3. Years that video game critics loved
# <p>It looks like a little less than ten percent of the games on the <code>game_sales</code> table don't have any reviews data. That's a small enough percentage that we can continue our exploration, but the missing reviews data is a good thing to keep in mind as we move on to evaluating results from more sophisticated queries. </p>
# <p>There are lots of ways to measure the best years for video games! Let's start with what the critics think. </p>

# In[22]:


get_ipython().run_cell_magic('sql', '', '\n-- We want to check the average critic score of each year\n-- And see the top scoring years\n-- To do this, we group by year and aggregate the years by AVG of its critic scores.\nSELECT g.year,\n       ROUND(AVG(r.critic_score),2) AS avg_critic_score\nFROM game_sales AS g\nLEFT JOIN reviews AS r\nON g.game = r.game\nGROUP BY g.year\nORDER BY avg_critic_score DESC\nLIMIT 10;')


# In[23]:


get_ipython().run_cell_magic('nose', '', 'from decimal import Decimal as D\nlast_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (10, 2), \\\n    "Make sure to limit the query to only ten results."\n    assert results.columns.tolist() == ["year", "avg_critic_score"], \\\n    \'The results should have two columns, called "year" and "avg_critic_score".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 1990, \\\n    "The year with the highest score should be 1990."\n    assert last_output.DataFrame().loc[0, \'avg_critic_score\'] == D(\'9.80\'), \\\n    "The highest average critic score should be 9.80."')


# ## 4. Was 1982 really that great?
# <p>The range of great years according to critic reviews goes from 1982 until 2020: we are no closer to finding the golden age of video games! </p>
# <p>Hang on, though. Some of those <code>avg_critic_score</code> values look like suspiciously round numbers for averages. The value for 1982 looks especially fishy. Maybe there weren't a lot of video games in our dataset that were released in certain years. </p>
# <p>Let's update our query and find out whether 1982 really was such a great year for video games.</p>

# In[24]:


get_ipython().run_cell_magic('sql', '', '\n-- Here, we filter out years that had less than 5 reviewed games in our database.\n-- We do this with the HAVING clause : A filtering that lets use the aggregated filter COUNT()\n-- We also use INNER JOIN on the game_sales and reviews table to filter out games not in both tables.\nSELECT g.year,\n       ROUND(AVG(COALESCE(r.critic_score, 0)), 2) AS avg_critic_score, -- NULL reviews as 0 \n       COUNT(g.game) AS num_games\nFROM game_sales AS g\nINNER JOIN reviews AS r\nON g.game = r.game\nGROUP BY g.year\nHAVING COUNT(g.game) > 4\nORDER BY avg_critic_score DESC\nLIMIT 10;')


# In[25]:


get_ipython().run_cell_magic('nose', '', 'from decimal import Decimal as D\nlast_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (10, 3), \\\n    "Make sure to limit the query to only ten results."\n    assert set(last_output.DataFrame().columns) == set(["year", "num_games", "avg_critic_score"]), \\\n    \'The results should have three columns: "year", "num_games", and "avg_critic_score".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 1998, \\\n    "The year with the highest score should be 1998."\n    assert last_output.DataFrame().loc[0, \'num_games\'] == 10, \\\n    "In the year with the highest critic score, there were 10 games released."\n    assert last_output.DataFrame().loc[0, \'avg_critic_score\'] == D(\'9.32\'), \\\n    "The highest average critic score should be 9.32."')


# ## 5. Years that dropped off the critics' favorites list
# <p>That looks better! The <code>num_games</code> column convinces us that our new list of the critics' top games reflects years that had quite a few well-reviewed games rather than just one or two hits. But which years dropped off the list due to having four or fewer reviewed games? Let's identify them so that someday we can track down more game reviews for those years and determine whether they might rightfully be considered as excellent years for video game releases!</p>
# <p>It's time to brush off your set theory skills. To get started, we've created tables with the results of our previous two queries:</p>
# <h3 id="top_critic_years"><code>top_critic_years</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>Year of video game release</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>avg_critic_score</code></td>
# <td>float</td>
# <td>Average of all critic scores for games released in that year</td>
# </tr>
# </tbody>
# </table>
# <h3 id="top_critic_years_more_than_four_games"><code>top_critic_years_more_than_four_games</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>Year of video game release</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>num_games</code></td>
# <td>int</td>
# <td>Count of the number of video games released in that year</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>avg_critic_score</code></td>
# <td>float</td>
# <td>Average of all critic scores for games released in that year</td>
# </tr>
# </tbody>
# </table>

# In[26]:


get_ipython().run_cell_magic('sql', '', '\n-- We want to see the years that were rated high by critics but did not have the quantity of reviews needed of 5 games\n-- To do this, we use our query that found the years with the top avg critic ratings and use the EXCEPT key word\n-- against our query that found the years with the top avg critic ratings that had more than 4 reviews.\n-- We find that the years 1990,1992,2020,1993,1995,1982 were top scoring years with less than 5 reviewed games in our db.\nSELECT year, avg_critic_score\nFROM top_critic_years\nEXCEPT \nSELECT year, avg_critic_score\nFROM top_critic_years_more_than_four_games\nORDER BY avg_critic_score DESC;')


# In[27]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (6, 2), \\\n    "There should be six years that dropped off the critics\' favorite list after implementing the criteria that the year had to have at least five games released to be considered."\n    assert results.columns.tolist() == ["year", "avg_critic_score"], \\\n    \'The results should have two columns: "year" and "avg_critic_score".\'\n    assert last_output.DataFrame().loc[5, \'year\'] == 1982, \\\n    "The last year returned by the query should be 1982."\n    assert last_output.DataFrame().loc[5, \'avg_critic_score\'] == 9.00, \\\n    "1982\'s average critic score should be 9.00."')


# ## 6. Years video game players loved
# <p>Based on our work in the task above, it looks like the early 1990s might merit consideration as the golden age of video games based on <code>critic_score</code> alone, but we'd need to gather more games and reviews data to do further analysis. </p>
# <p>Let's move on to looking at the opinions of another important group of people: players! To begin, let's create a query very similar to the one we used in Task Four, except this one will look at <code>user_score</code> averages by year rather than <code>critic_score</code> averages.</p>

# In[28]:


get_ipython().run_cell_magic('sql', '', '\n-- We want to know the years that the general public loved, based on their ratings.\n-- We do this by grouping by year, filtering for years that had 5 or more reviewed games\n-- We also order by avg rating to find the top 10 scoring years.\nSELECT g.year,\n       COUNT(g.game) AS num_games,\n       ROUND(AVG(r.user_score),2) AS avg_user_score\nFROM game_sales AS g\nINNER JOIN reviews AS r\nON g.game = r.game\nGROUP BY g.year\nHAVING COUNT(g.game) > 4\nORDER BY avg_user_score DESC\nLIMIT 10;')


# In[29]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (10, 3), \\\n    "Don\'t forget to limit the query results to ten."\n    assert set(results.columns.tolist()) == set(["year", "num_games", "avg_user_score"]), \\\n    \'The results should have three columns: "year", "num_games", and "avg_user_score".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 1997, \\\n    "The year with the highest user score should be 1997."\n    assert last_output.DataFrame().loc[0, \'num_games\'] == 8, \\\n    "In the year with the highest user score, there were eight games released."\n    assert last_output.DataFrame().loc[0, \'avg_user_score\'] == 9.50, \\\n    "The highest average user score should be 9.50."')


# ## 7. Years that both players and critics loved
# <p>Alright, we've got a list of the top ten years according to both critic reviews and user reviews. Are there any years that showed up on both tables? If so, those years would certainly be excellent ones!</p>
# <p>Recall that we have access to the <code>top_critic_years_more_than_four_games</code> table, which stores the results of our top critic years query from Task 4:</p>
# <h3 id="top_critic_years_more_than_four_games"><code>top_critic_years_more_than_four_games</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>Year of video game release</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>num_games</code></td>
# <td>int</td>
# <td>Count of the number of video games released in that year</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>avg_critic_score</code></td>
# <td>float</td>
# <td>Average of all critic scores for games released in that year</td>
# </tr>
# </tbody>
# </table>
# <p>We've also saved the results of our top user years query from the previous task into a table:</p>
# <h3 id="top_user_years_more_than_four_games"><code>top_user_years_more_than_four_games</code></h3>
# <table>
# <thead>
# <tr>
# <th style="text-align:left;">column</th>
# <th>type</th>
# <th>meaning</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td style="text-align:left;"><code>year</code></td>
# <td>int</td>
# <td>Year of video game release</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>num_games</code></td>
# <td>int</td>
# <td>Count of the number of video games released in that year</td>
# </tr>
# <tr>
# <td style="text-align:left;"><code>avg_user_score</code></td>
# <td>float</td>
# <td>Average of all user scores for games released in that year</td>
# </tr>
# </tbody>
# </table>

# In[30]:


get_ipython().run_cell_magic('sql', '', '\n-- We want to find the years that scored in the top 10 for both critics and the general public\n-- To do this, we can INNER JOIN the queries of top 10 scoring games by critics and the public\n-- ON the year. This will match all the years that the top 10 shared in common.\nSELECT c.year\nFROM top_critic_years_more_than_four_games AS c\nINNER JOIN top_user_years_more_than_four_games AS u\nON c.year = u.year;')


# In[31]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (3, 1), \\\n    "There should be three years present in both tables."\n    assert results.columns.tolist() == ["year"], \\\n    \'The results should just have one column: "year".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 1998, \\\n    "The first year returned by the query should be 1998."')


# ## 8. Sales in the best video game years
# <p>Looks like we've got three years that both users and critics agreed were in the top ten! There are many other ways of measuring what the best years for video games are, but let's stick with these years for now. We know that critics and players liked these years, but what about video game makers? Were sales good? Let's find out.</p>
# <p>This time, we haven't saved the results from the previous task in a table for you. Instead, we'll use the query from the previous task as a subquery in this one! This is a great skill to have, as we don't always have write permissions on the database we are querying.</p>

# In[32]:


get_ipython().run_cell_magic('sql', '', '\n-- What also matters in how good a game was is the number of times the game was sold\n-- We can find this in our games_sales table under the games_sold column\n-- To find total games sold, we can GROUP BY year then SUM up every game in the grouped year.\n-- We know that the top 10 year, based on critic and general public reviews were 1998 , 2002, 2008\n-- Thus, we can use a WHERE year IN to check if those years were also a top 10 video game selling year.\n-- Our query returns all three years, thus 2008,  2002, and 1998 are the top years for video games, according to our SQL queries.\nSELECT g.year,\n       SUM(g.games_sold) AS total_games_sold\nFROM game_sales AS g\nINNER JOIN reviews AS r\nON g.game = r.game\nWHERE g.year IN (1998 , 2002 , 2008)\nGROUP BY g.year\nORDER BY total_games_sold DESC')


# In[33]:


get_ipython().run_cell_magic('nose', '', 'from decimal import Decimal as D\nlast_output = _\n\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (3, 2), \\\n    "There should be games sales data for three years: the same three years from the previous query."\n    assert results.columns.tolist() == ["year", "total_games_sold"], \\\n    \'The results should have two columns: "year" and "total_games_sold".\'\n    assert last_output.DataFrame().loc[0, \'year\'] == 2008, \\\n    "Just like in the last query, the first year returned should be 2008."\n    assert last_output.DataFrame().loc[0, \'total_games_sold\'] == D(\'175.07\'), \\\n    "In 2008, the total_games_sold value should be 175.07."')


# In[34]:


get_ipython().run_cell_magic('nose', '', 'from decimal import Decimal as D\nlast_output = _\n\ndef test_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_results():\n    assert results.shape == (10, 6), \\\n    "The results should have six columns and ten rows."\n    assert results.columns.tolist() == ["game", "platform", "publisher", "developer", "games_sold", "year"], \\\n    \'The results should have columns named "game", "platform", "publisher", "developer", "games_sold", and "year".\'\n    assert _.DataFrame().loc[0, \'games_sold\'] == D(\'82.90\')\n    "The top selling game should be Wii Sports with 82.90 million copies sold."')

