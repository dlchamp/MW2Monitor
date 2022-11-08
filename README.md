# MW2Monitor
  A simple bot that monitors MW2 activities and create time sessions and a leaderboard to compare time played among your friends

  Bot built per request by Reddit user

### TODO
Since I don't personally own MW2 and didn't have access to fully testing the activity monitor features, this feature may not work 100% as intended.  I will be fixing it, if needed, once I have the ability to do so.

# Commands and features
This bot is designed to automatically create timestamps for sessions when a user starts/stops playing MW2 so long as they are reporting their game activity to Discord.  However, this isn't perfect, so the commands below will allow you two different methods of adding sessions manually.  
  
  
All commands supported by this bot are slash commands (`/command`)

- `/leaderboard` - Displays the current leaderboard with all players sorted by play time for Call of Duty MW2

- `/start_session` - Starts a new gaming session (Creates a data point for "now" and will calculate until you run the `/end_session` command)

- `/end_session` - Adds a data point for "now" that will end the current active session

- `/add_session [hours] [minutes]` - Allows you to add a session length (hours, minutes) and will create a starting-end time based around "now" minus the hours/minutes that have inputted
&nbsp;(**Hours and minutes default to 0**)


# Creating a new Bot Application
1. Head over to the [discord developer portal](https://discord.com/developers/applications)
2. Create a new application and attach a new bot
3. You will need the bot token so do not refresh or close this page until you've copied the bot token elsewhere
4.  You will need to enable the **Privileged Gateway Intents** for *Presence Intent*
5. Head over to Oauth2 > URL Generator
6. Select *bot* and scroll down to permissions section
7. This bot needs the following permissions to work properly  
 a. Send Messages
 
8. Copy the *Generated URL* and paste it into your Discord Client or browser tab to invite the bot to your server



# Configuring the bot 
1. Pull down this repo and store it somewhere you can quickly access.  Like, *Documents* or anywhere that's not a system directory
2. Paste the copied token from Step 3 above in the .env-sample file.  Should read like:  `TOKEN = YOUR TOKEN`, then save and rename this file to `.env`
3. Within your terminal, navigate to the location of the bot's main project folder `mw2bot`.  If you're inside this directory, you went too far.
4. Run the bot with `poetry run python -m mw2bot` or `poetry run python3 -m mw2bot` (if on linux/MacOS)



