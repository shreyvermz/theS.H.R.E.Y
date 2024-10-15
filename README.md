# The S.H.R.E.Y. 
### A Basketball Statistics Analysis Tool Gauging Impact on Winning

## Description
Great play and contribution typically stands out like a sore thumb on the stat sheets, making it easy for fans to deduce seemingly reasonable conclusions regarding a player from quick box score analysis.
In the same vein, it can be hard for high-impact players to garner recognition when they provide intangibles that aren't encapsulated effectively by the box score.
The box score can be very deceiving when it comes to distinguishing how impactful a player truly is, and the **S.H.R.E.Y.** was devised as a way to go past the box score, and truly find the impact of a player. Using NBA databases
**specifically from 1998-2022**, this program contextualizes a player's impact based on team play, defensive efficiency, offensive contributions outside of scoring, and the era they played in.

## Method and Motivation
This program was written in Python using the Pandas library. After learning Python, I wanted to learn Pandas to determine if there were ways I could contribute to my internship role at the time.
While doing this, I inadvertently learned the means to accomplish a basketball-related project I had been wanting to do for some time. This was mainly a way for me to practice pulling data from multiple databases, manipulating and analyzing it, and creating a sufficient analysis product that simplifies large amounts of information.

## Analysis Guide
### **S**: **Scoring**
The first criteria being looked at is Scoring. We first find the player's point per game average on the season inputted, and sort the player into tiers depending on the averages.
These tiers, which are an integer value that increases as points per game increases, have different criteria for each different era of basketball accounted for. We will touch over more on the eras in the **Reasonability** section. 
If a player was within the top 10 for scoring averages on the season, they received a complimentary scaler ranging from 1.05 to 1.5, the scaler increasing as the number of players
averaging more dwindles. 
#### Final Scoring Grade:   
(points per game * tier) * (scaler, if the player qualified)

### **H**: **Help**
This section bears the most responsibilty for the total analysis, as it uses the **Reasonability** and **Yearly Outlook** portions of the program to formulate
its final output. 
#### Part I
This section is not only used to gauge how much help a player had throughout their season (as supplimentary star power simplifies the game 
exponentially), but it also measures how much help a player gives back to their team in the form of assists, rebounds, and defensive efficiency. 
The first factor that we devise to aid this section's output is the **help scaler**. This is formed from consideration of the **ratio of team points** scored by
the player, **tier provided based on the stocks (steals + blocks)** a player logs, and the **Reasonability Scaler**, which is a scaling integer returned from the **Reasonability** section.
Players are then sorted into tiers based on their assist and rebounding numbers, which differs by position. These tiers are an integer number increasing with 
enhanced performance, and the sorted tier is multiplied by the **help scaler** in each instance, giving **help scores** in the context of **assists and rebounds**.
#### The **final help grade** is a simple addition of these two help scores.
1. help scaler = (ratio +1) * (reasonability output) * (stocks tier)
2. help_assists = (help scaler) * (assists tier)
3. help_rebounds = (help scaler) * (rebounds tier)
4. final help grade = help_assists + help_rebounds
#### Part II
The second part of the Help portion is the text based analysis of the **Role** we assign a player. The players are sorted among the Roles of **Givers, Takers, Complimentary**, and
**Winners**. Assignment of these roles consider the **ratio of teams points scored, team defensive efficiency**, and the **total help grade** from Part I. This section contextualizes the help score the player received, and allows the user a deeper level of insight into how the player's playstyle 
meshed with their team. If the player's team won a championship that year, they are automatically given the Role of **Winner** (the database to find championship winners only goes to 2018 versus the other 2 used going to 2022, so needs to add error handling). This portion of the program is optional,
and users are given the choice between receiving the **help score** by itself, or in conjunction with the Role descriptor.

### **R**: **Reasonability**
This section is responsible for the division of eras when considering scoring, giving more weight to impressive scoring numbers in prior eras, as the game's pace was much slower and scoring at a high volume has gotten less meaningful over time. It has no explicit output, but is embedded within the **Help** section detailed above.
#### Pre 2004-05 Season  
The first era we split on is any year in our databases prior to the 2004-2005 season. The 2004 season marked a turn of the tides in offensive styles, as coach of the Phoenix Suns, Mike D'Antoni, established the **'Seven Seconds or Less'** rule to urge his team to increase their tempo and generate more possessions throughout the game. This introduction ushered more teams to experiment with more offensive playstyles.
#### 2004-2016 Seasons
**If the NBA was the universe, 2004 would be the Big Bang of offensive output**, and the coinciding next 12 seasons was the universe adjusting to this new plethora of resources. This era was still dominated by mid-range and paint play, but teams were beginning to retool and restructure offensive approaches, increasing their tempos and taking more 3 pointers. This era marked the introduction of **Stephen Curry**, the man who arguably changed the offensive landscape more than any player in history by his absurd efficiency from the 3 point line.
#### 2016 and Onwards
After the Warriors' championship in 2015, teams knew they had a juggernaut to take down, and the only way to match their 3 point output? **More 3 pointers**. This era marks the point of no return for offenses.
Teams are averaging shooting numbers that would have broken records in previous eras. The league has become hyper-efficient, and the pure scoring talent of players in this era numb fans to the development of
offensive excellency. Coaches choose gameplans more based on analytics and statistics as technology becomes increasingly incorporated into the sports world, and these analytics favor fast tempo, 3 pointers, and getting to the rim. The tempo of games almost completely gets rid of the mid range, and **3 pointers rule all**.

### **E**: **Efficiency**
One of the best statistics to measure offensive effieciency, while also considering the trade off between 2 and 3 pointers that has become increasingly debated as the style of offense changes, is the eFG.
**Efficient Field Goal Percentage**, or **eFG%** has become an increasingly popular tool to measure the **value** of a player's shot diet. 
#### **Formula:**
**(Field goals + (1.5 * 3pt field goal))** 
  /
**(Total field goals attempted)** 

  
Since eFG% is one of the most reliable stats, this section uses existing information on eFG% and gives a text-based description of how a player's eFG% helped define their contributions in their respective eras.

### **Y**: **Yearly Outlook**
This is another implicitly used section within **Help**. It used to search a third database detailing the winners and MVPs of each season up to 2018, and is mainly used to determine whether a player won a ring that season. After returning True or False, the player's Role may be retroactively changed to Winner if it wasn't already. MVPs are not considered in the final score due to their unreliability, specifically due to a phenomenon known as **Voter Fatigue**, which barred players such as Kobe Bryant, LeBron James, and Michael Jordan from receiving a fair number of these trophies due to the disregard greatness is approached with when it is sustained for an abnormally long time. 

