## This is a small tool to generate player statistics from double elimination brackets on start.gg

First, follow the directions [here](https://developer.start.gg/docs/authentication) to get a token. Save it to a file named ".token" in the same directory as the script

Next, you need the event ID of the bracket. On the start.gg page, navigate to Settings > Brackets > your bracket. The link at the top of the screen should look something like: www.start.gg/admin/tournament/YOUR-TOURNAMENT-NAME/BRACKETS/**number1**/number2/number3

Copy and paste number1, it is the event ID. 

Now, open a terminal in the directory you have the code saved and run the command `python post_bracket_stats.py EVENT_ID`. After a short period, you should see the stats printed to the console.