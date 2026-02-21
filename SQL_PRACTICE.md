# SQL Practice — 100 Queries on the SPL Database

Work through these in order in the Supabase SQL Editor. No solutions provided — figure it out, run it, verify the output makes sense. If you get stuck, Google the concept then come back.

## Database Quick Reference

| Table | Key Columns |
|-------|------------|
| `players` | id, display_name, full_name, is_active |
| `games` | id, game_date, team_a_goals, team_b_goals, championship, venue |
| `player_game_stats` | game_id, player_id, team, goals, own_goals, mvp, spl_bonus, penalty, friend_referrals |
| `player_rankings` | player_id, player_name, rank, total_points, games_played, win_ratio, goals_per_game |
| `fantasy_teams` | id, team_name, owner_name |
| `fantasy_rosters` | id, team_id, player_id, tier, price_millions |
| `scoring_parameters` | parameter_name, game_format_id, points_value |
| `positions` | id, name |
| `game_formats` | id, name |

---

## Level 1 — SELECT Basics (1–15)

These are pure fundamentals. If any of these feel hard, slow down — everything builds on this.

**1.** Select all columns from the `players` table.

**2.** Select only `display_name` and `full_name` from `players`.

**3.** Select all games, ordered by `game_date` from newest to oldest.

**4.** Select the first 10 players alphabetically by `display_name`.

**5.** Select all players where `is_active` is true.

**6.** Select all games where `championship` is `'Bovisa'`.

**7.** Select all games where Team A scored more than 10 goals.

**8.** Select all games that ended in a draw (Team A goals = Team B goals).

**9.** Select all players whose `display_name` starts with `'A'`.

**10.** Select all games played in 2025 (game_date between Jan 1 and Dec 31 2025).

**11.** Select all games where the total goals (both teams combined) exceeded 20.

**12.** Select distinct values of `championship` from the `games` table.

**13.** Select all fantasy teams, ordered by `team_name`.

**14.** Select all player_game_stats where the player scored 3 or more goals.

**15.** Select all players whose `display_name` contains the word `'Matteo'`.

---

## Level 2 — Filtering & Sorting (16–25)

Combining conditions, using operators you'll need every day.

**16.** Select all Bovisa games from 2024 onwards, ordered by date.

**17.** Select all games where Team A won by 5+ goals.

**18.** Select all player_game_stats where the player scored at least 1 goal AND got MVP (mvp = 1).

**19.** Select all players whose display_name is NOT null and full_name IS null.

**20.** Select games where championship is either `'Bovisa'` or `'Lambrate'` and total goals > 15. (Use `IN` for the championship filter.)

**21.** Select the 5 highest-scoring games (by total goals both teams), showing date, championship, and both scores.

**22.** Select all player_game_stats rows where goals is 0 and own_goals is greater than 0 (own goals without scoring).

**23.** Select all games played on a Wednesday. (Hint: `EXTRACT(DOW FROM game_date)` — 3 = Wednesday.)

**24.** Select all fantasy rosters where `price_millions` is 10 (the expensive tier).

**25.** Select all players whose display_name has parentheses in it (contains `'('`).

---

## Level 3 — Aggregations (26–40)

COUNT, SUM, AVG, MIN, MAX, GROUP BY. This is where SQL gets powerful.

**26.** Count the total number of games in the database.

**27.** Count how many games each championship has.

**28.** What is the average Team A goals across all games?

**29.** What is the highest number of goals a single player scored in one game? (MAX on player_game_stats.goals)

**30.** How many total goals has each player scored? Show player_id and total goals, ordered by most goals first.

**31.** How many games has each player participated in? (Count rows per player_id in player_game_stats.)

**32.** What is the average total goals per game for each championship?

**33.** How many players are in each fantasy roster tier? (Group by tier, count players.)

**34.** What is the total `price_millions` spent per fantasy team? (Group by team_id, sum price.)

**35.** Find the game with the most participants. (Count player_game_stats rows per game_id, order desc, limit 1.)

**36.** For each player, what is their average goals per game? Only include players with 10+ games.

**37.** How many games ended in a draw vs. a win for either team? (Hint: use CASE WHEN inside COUNT or SUM.)

**38.** What is the total number of own goals in the entire database?

**39.** How many MVPs has each player received? Show only players with 2+ MVPs.

**40.** What percentage of all games were played in Bovisa? (Count Bovisa / Count total × 100.)

---

## Level 4 — JOINs (41–58)

This is THE most important SQL skill. Master this section.

**41.** Join `player_game_stats` with `players` to show `display_name` alongside goals for each stat row. Limit to 20 rows.

**42.** Join `player_game_stats` with `games` to show the `game_date` and `championship` alongside each player's stats. Limit to 20.

**43.** Show each player's display_name and their total goals across all games. (Join + GROUP BY.)

**44.** Show each player's display_name and number of games played, ordered by most games first. Top 20 only.

**45.** Join `fantasy_rosters` with `players` to show the display_name of each player in each roster.

**46.** Join `fantasy_rosters` with `fantasy_teams` to show team_name and owner_name alongside each roster entry.

**47.** Triple join: Show fantasy team_name, owner_name, and player display_name for every roster entry. Order by team name.

**48.** Show each player's display_name and the date of their most recent game. (Join player_game_stats → games, group by player, MAX game_date.)

**49.** Show each player's display_name and their total goals, but only for Bovisa games. (Join with games, filter championship, group by player.)

**50.** Find all players who have NEVER played a game. (LEFT JOIN player_game_stats, WHERE game_id IS NULL.)

**51.** Show each game's date, championship, and the number of players who participated. (Join games ← player_game_stats, group by game.)

**52.** For each fantasy team, show the team name and the number of players on the roster. (Join + GROUP BY.)

**53.** Show every game where Cameron McAinsh played, with the date, his team, and his goals. (Join through players to find Cameron's player_id.)

**54.** Show all players who played on Team A in the most recent game. (Subquery or JOIN to find latest game_date first.)

**55.** For each championship, show the player with the most total goals. (This is harder — think about how to get the max per group.)

**56.** Show each fantasy team's total SPL points earned by their rostered players. (Join fantasy_rosters → player_rankings for total_points, sum per team.)

**57.** List all pairs of players who have been on the same team in at least 10 games. (Self-join player_game_stats on game_id and team, where player_id differs.)

**58.** Show all games where at least one player scored a hat trick (3+ goals), with the game date and the player's name.

---

## Level 5 — Subqueries & CTEs (59–72)

Writing queries inside queries. CTEs (WITH) make complex logic readable.

**59.** Find all players who have scored more total goals than Cameron McAinsh. (Use a subquery to get Cameron's total first.)

**60.** Select all games where the total goals exceeded the overall average total goals per game. (Subquery in WHERE.)

**61.** Using a CTE, calculate each player's total goals, then select only those in the top 10.

**62.** Find the game_date of the last game each player participated in. Use a CTE, then join back to players for display_name.

**63.** Using a CTE, calculate each championship's average goals per game, then show only championships above the overall average.

**64.** Find all players who have played in BOTH Bovisa and Lambrate championships. (Hint: use two subqueries or a CTE with INTERSECT.)

**65.** Write a CTE that calculates each player's win rate (wins / games played), then find all players with a win rate above 50% and at least 20 games.

**66.** Find the top scorer of each individual game. Use a CTE to rank players per game, then filter rank = 1.

**67.** Using a subquery, find all fantasy teams where EVERY player on the roster has played at least 5 games.

**68.** Find the longest gap (in days) between consecutive games for the Bovisa championship. (CTE with LAG window function.)

**69.** Calculate the "form" of each player: their average goals in their last 5 games vs. their career average. Show the difference. (CTE + window function for last 5.)

**70.** Find all players who scored in every game they played (no games with 0 goals). Use NOT EXISTS or a CTE.

**71.** Show each player's rank by total goals within their most-played championship. (CTE to find most-played championship, then rank within it.)

**72.** Find all fantasy teams where the combined total_points of the roster (from player_rankings) is above the median team total.

---

## Level 6 — Window Functions (73–82)

The power tool of analytics SQL. RANK, ROW_NUMBER, LAG, LEAD, running totals.

**73.** Rank all players by total goals using `RANK()`. Show display_name, total_goals, rank.

**74.** Use `ROW_NUMBER()` to assign a unique number to each game per championship, ordered by date (essentially recreating gameweek numbering).

**75.** For each game, show the cumulative total goals scored in that championship over time (running total with `SUM() OVER`).

**76.** Use `LAG()` to show each game's total goals alongside the previous game's total goals for the same championship.

**77.** Use `LEAD()` to show each player's goals in a game alongside their goals in their next game.

**78.** Calculate each player's moving average goals over their last 3 games (use `AVG() OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`).

**79.** Use `DENSE_RANK()` to rank fantasy teams by total roster points. How does it differ from RANK()?

**80.** For each championship, find the game with the highest total goals using `RANK()` partitioned by championship.

**81.** Show each player's goals per game as a percentage of the team's total goals in that game. (Window SUM partitioned by game_id + team.)

**82.** Calculate each player's "streak" — consecutive games with at least 1 goal. (This is hard. Think about gaps using ROW_NUMBER differences.)

---

## Level 7 — Data Manipulation & Advanced (83–92)

INSERT, UPDATE, DELETE, CASE, COALESCE, string functions, date functions.

**83.** Write an INSERT statement that would add a new player (don't run it — just write it correctly). Include display_name, full_name, is_active.

**84.** Write an UPDATE that would set `is_active = false` for all players who haven't played a game since 2024. (Don't run — just write it.)

**85.** Use `CASE WHEN` to create a column that labels each game as 'High Scoring' (>15 total goals), 'Normal' (8-15), or 'Low Scoring' (<8).

**86.** Use `COALESCE` to show each player's full_name, falling back to display_name if full_name is null.

**87.** Extract the month from game_date and show how many games were played in each month across all years.

**88.** Use string functions to extract just the first name from display_name (everything before the first space). Handle names without spaces.

**89.** Calculate the number of days between each player's first and last game (their "career span").

**90.** Write a query that pivots the data: show each championship as a column with the count of games. (Use CASE + SUM or FILTER.)

**91.** Use `GENERATE_SERIES` to create a calendar of all Wednesdays in 2025, then LEFT JOIN with games to find which Wednesdays had no game.

**92.** Write a DELETE statement (don't run) that would remove all player_game_stats for games before 2023.

---

## Level 8 — Real-World Challenges (93–100)

These simulate actual questions you'd get at work. Multi-step, requiring you to combine everything.

**93.** **"Who is the most improved player this season?"** — Compare each player's average PPG (points per game) in the current season vs. the previous season. Show the biggest positive difference. You'll need to calculate season from game_date, join, and compare.

**94.** **"Which day of the week produces the most goals?"** — Group games by day of week, calculate average total goals, and rank the days.

**95.** **"Build a fantasy draft board"** — For each player with 10+ games, show: display_name, total_points, goals_per_game, win_rate, and a calculated "value score" (total_points / games_played × win_rate). Rank by value score.

**96.** **"Find the most one-sided games"** — Show the top 10 games by goal difference, with date, championship, scores, and all player names on the winning team.

**97.** **"Player chemistry report"** — For each pair of players who have played 5+ games together (same team), calculate their combined win rate. Who are the best and worst duos?

**98.** **"Championship parity analysis"** — For each championship and season, calculate the standard deviation of goals across games. Higher StdDev = less predictable. Which championship-season was the most unpredictable?

**99.** **"Create a complete player dashboard query"** — Single query that returns for a given player: total games, wins, losses, draws, total goals, goals per game, win rate, current rank, market value trend (from rankings), fantasy teams they're on, and their last 5 game results.

**100.** **"Simulate a new scoring system"** — Using CTEs, recalculate total points for all players using modified rules: double the goal points, remove MVP bonus, and add 2 points for clean sheets (games where the player's team conceded 0). Show how the top 20 ranking would change compared to the current ranking.

---

## Tips

- Run each query before moving on. Read the output. Does it make sense?
- If a query returns unexpected results, debug it — that's where the learning is.
- When stuck: break the query into smaller parts, run each part separately.
- Supabase uses **PostgreSQL** — you can Google "postgres [concept]" for syntax help.
- Some queries may take a few seconds on large joins — that's normal.

Good luck. By query 100 you'll be dangerous. 🔥
