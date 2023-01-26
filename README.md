## This is a small tool to generate player statistics, namely Seed Performance Ranking and Upset Factor, from double elimination brackets on start.gg

First, follow the directions [here](https://developer.start.gg/docs/authentication) to get a token. Save it to a file named ".token" in the same directory as the script

The two arguments of the script are the slug of the tournament and of the event. A start.gg event link looks something like start.gg/tournament/TOURNAMENT_NAME/events/EVENT_NAME. Go to your event and copy both the tournament name and the event name

Now, open a terminal in the directory you have the code saved and run the command `python post_bracket_stats.py TOURNAMENT_NAME EVENT_NAME`. After a short period, you should see the stats printed to the console.

I didn't bother with any error handling in the API requests section, so if something goes wrong just run it again and it'll probably work after a few tries. 
