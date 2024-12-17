# Analytics-projects
Here I store the code used for my modelling projects in football analytics. 
Attacking in the final third is often considered the most challenging aspect of football. Phrases like “We’re not good enough in the final third” or “We’re struggling to find solutions in the final third” are commonly heard when a possession-oriented team tries to explain why things aren’t going their way. Since many modern football teams aim to play a possession-oriented style, cracking the code in the final third is a critical issue for many teams.

Often, these phrases are used without any real answers to exactly what the problem is. As an analyst, I want to measure and clearly quantify how good my team is in the final third. Naturally, this depends on our style of play and the types of defenses we tend to face. In this text, I attempt to reason through this challenge and define a way to measure how successful teams are in the final third.

Definition and Derivation of the Final Third Proficiency Index (FTPI)

The dynamics of attacking in the final third depend on several factors. First, it depends on how often a team attacks in the final third. The amount of time spent in the final third will influence how those attacks unfold. For example, if the defending team spends more time in the final third, it may impact how they learn to defend against a particular team and how fatigue sets in.

Second, it obviously depends on the team’s own style of play. Third, it depends on the nature of the opponent. How the opponent defends can vary based on multiple factors: whether they have a specific idea about how they want to defend in the final third and how they choose to adapt to the attacking team.

As an analyst, if I want to measure how well my team performs in the final third, the metric I use will inevitably be influenced by these three elements. What I’m really trying to measure is my team’s proficiency in the final third, relative to the opponents we face. To analyze tactical or principled changes and adjustments in the team, I need a metric that allows for meaningful comparisons. For this reason, the measure must be as independent of playing style as possible.

This independence also allows comparisons between teams with different playing styles, while still accounting for the opponents they face in their league. This is crucial because the opposition plays a central role when evaluating league matches.

Offensive Outputs as the Basis of FTPI

When measuring success in the final third, it’s naturally about quantifying offensive output in various ways. This is the first overarching parameter in the model I aim to create. It involves identifying which KPIs are most important for measuring final-third output.

To build such a model, I want to combine different metrics and weight them according to two factors:

How important these metrics are to the model from my perspective.
How well the metrics align with one another in terms of scale, as different metrics often look quite different. For example, xG is not directly comparable to the number of touches in the final third.
These weights can, of course, be modified to adapt the model to the team’s style of play. However, as mentioned earlier, there are drawbacks to tailoring the model too closely to the current playing style. Doing so diminishes the model’s analytical value if it’s used after tactical adjustments have been made.

Thus, the biggest challenge in creating this model is staying objective enough to select the correct weights.

Examples of Metrics to Measure Offensive Output in the Final Third

Here are some examples of metrics to evaluate offensive output in the final third:

Chance-Creation Metrics
Key Passes: Measures the number of passes that directly lead to a shot.
Expected Assists (xA): Quantifies the quality of chances created by measuring the probability that a pass will result in a shot that leads to a goal.
Shot-Creating Actions (SCA): Includes all offensive actions (passes, dribbles, fouls drawn) that lead to a shot.
2. Shot Quality and Frequency

Shots on Target in the Final Third: Measures a team’s ability to create accurate shooting opportunities in critical areas.
xG: The quality of chances based on historical probabilities of scoring from similar positions.
Goal Conversion Rate: The percentage of shots converted into goals, indicating finishing efficiency.
3. Possession in the Final Third

Touches in the Box: Reflects how often the team reaches dangerous positions.
Successful Passes in the Final Third: Indicates the ability to maintain possession and circulate the ball effectively.
Passing Accuracy in the Final Third: Demonstrates technical skill and decision-making in tight spaces.
Sequence Time in the Final Third: Measures how long the team maintains possession in the final third, reflecting sustained pressure.
Progressive Passes into the Final Third: Evaluates how effectively the team breaks through defensive lines.
4. Pressing and Recovery in the Final Third

Recoveries in the Final Third: Indicates how often the team regains possession in advanced positions, potentially leading to goal-scoring opportunities.
Counter-Pressing Success: Measures how efficiently the team quickly recovers the ball after losing it in the final third.
5. Movement and Positioning

Off-Ball Runs: Analyzes player movements to create space or receive passes in dangerous areas.
Progressive Carries in the Final Third: Captures the ability to individually transport the ball into advanced positions.
We define the “raw” measure of offensive output in the final third as:


where www represents the weights for the various metrics as discussed earlier.

Adjusting for Opponent Compactness

Previously, I argued why it’s important to adjust the index for the opponents faced. The most significant factor opponents influence to hinder the attacking team’s success in the final third is their compactness — minimizing the space available for the attacking team. We measure the opponent’s compactness by determining a “Compactness Factor,” which depends on four components:

Density of Players in the Final Third or Penalty Area: How many players the defending team has in the penalty area, referred to as Density.
Defensive Line Depth: How deep the defending team positions its defensive line.
Defensive Actions in the Final Third: Includes tackles, interceptions, blocks, etc., and could also include how aggressively the team presses in the final third, measured by metrics like PPDA. Referred to as Defensive Actions in Final Third.
Occupied Area or Shape Width: How much space the defending team occupies in the final third, including their width.
Similar to the offensive output measure, we define the Compactness Factor as a weighted measure of these four components:


Adjusting for Opponent Field Tilt

It’s important to remember that opponents spending little time in their own final third often appear less compact than teams spending more time defending there. Thus, it’s natural to adjust the compactness factor based on the opponent’s field tilt — a metric representing the proportion (as a percentage between 0 and 1) of all touches and passes in the offensive final thirds that each team has in a match.

If a team spends more time defending in their final third, their field tilt will be lower. Dividing the compactness factor by a smaller value (between 0 and 1) increases the compactness factor, which is what we want. We define the Adjusted Compactness Factor as:


Final Model for FTPI

We then adjust the raw measure of offensive output for both the adjusted compactness factor and the attacking team’s field tilt, as time spent in the final third impacts the measure of efficiency. Adjusting for this, we normalize the raw output by dividing it by the attacking team’s field tilt:


Analyzing Trends and Expected FTPI

FTPI is calculated for individual matches. To analyze trends, it’s useful to calculate rolling averages over several matches to observe a team’s performance over a period.

If FTPI data is collected for an entire league, and FTPI is calculated for each opponent, one can derive an Expected FTPI (xFTPI) against a specific opponent. This can be defined as the average FTPI that all other teams achieve against that opponent. By studying a single match, it’s then possible to assess whether a team overperformed or underperformed relative to expectations by calculating:


where a positive value indicates performance above expectations and a negative value below expectations. Alternatively:


where a ratio >1 indicates performance above expectations, and <1 below expectations.
