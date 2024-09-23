# The S.H.R.E.Y. 
### A basketball statistics tool for analysis and impact on winning

## Description
Great play and contribution typically stands out like a sore thumb on the stats sheet in basketball, and makes it easy for fans to deduce their own conclusions regarding a player from box-score analysis.
In the same vein, it can be hard for high-impact players to garner recognition when they provide intangibles that aren't encapsulated effictively by the box score.
The box score can be very deceiving when it comes to distinguishing how impactful a player truly is, and the S.H.R.E.Y. was devised as a way to study a wide array of players, using NBA databases
**specifically from 1998-2022**, and contextualize their impact based on team play, defensive impact, offense outside of scoring, and the era they played in.

## Analysis Guide
### **S**: **Scoring**
The first criteria being looked at is Scoring. We first find the plaeyr's point per game average on the season inputted, and sort the player into tiers depending on the averages.
These tiers have different criteria for each different era of basketball accounted for. We will touch over more on the eras in the **Reasonability** section. 
If a player was within the top 10 for scoring averages on the season, they received a complimentary scaler ranging from 1.05 to 1.5, the scaler increasing as the number of players
averaging more dwindles. The final score provided for this section is a number that results from the equation:   
**(points per game * tier) * (scaler if the player qualified)**.

### **H**: **Help**
This section bears the most responsibilty for the total analysis, as it uses the **Reasonability** and **Yearly Outlook** portions of the program to formulate
its final output. 
#### Part I
This section is not only used to gauge how much help a player had throughout their season, as supplimentary star power simplifies the game 
exponentially, but it also measures how much help a player gives back to their team in the form of assists, rebounds, and defensive efficiency. 
The first factor that we devise to aid this section's output is the **help scaler**. This is formed from consideration of the **ratio of team points** scored by
the player, **tier provided based on the stocks (steals + blocks) a player logs**, and the **Reasonability Scaler**, which is explained in the **Reasonability** portion.
We then sort players into tiers based on their assist and rebounding numbers, which differs by position. 
### Part II
