# My_Data_centric_Programming_assignment
# Questions for the Data
1. Does workout duration affect how much my mood improves after exercising? 

1. Does consuming an energy drink affect my workout duration and mood improvement? 

1. Does the time i start my workout influence my workout duration and mood improvement? 



## Data Dictionary 
Some of this data is collected by using two apps, Hevy and MyFitnessPal. Hevy allows me to track my workout whilst MyFitnessPal allows me to track my calories. 

| Column | Data Type | Units | Measurements / Definitions |
|---|---|---|---|
| Date   | dates     | day-month-year | The day that this entry is recored | 
| Muscle Group | Categorical | String | What muscle group I have worked for this entry | 
| duration_minutes | Numeric | Integer | How long the workout has taken to complete | 
| start_time | Time | Hour and Minutes | What time I started the workout | 
| mood_before(0-5) | Categorical | Integer | What mood i was in before going to the gym | 
| mood_after(0-5) | Categorical | Integer | What mood i was in after going to the gym |
| Calories_consumed | Numeric | Integer | How many calories i have consumed that day | 
| Energy Drink(0-1)| Numeric | Boolean | Did i have an energy drink before the workout | 
