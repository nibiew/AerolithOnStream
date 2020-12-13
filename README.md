# Aerolith On Stream
A basic Twitch bot that relies on PyAutoGUI to run Aerolith (https://www.aerolith.org/) on stream. GUI built using PySimpleGUI (command line window still pops up to facilitate easier debugging). Credits to César Del Solar for helping to build an API to facilitate this, and many other Scrabble players for helping to test this out and share suggestions.

### Files you need on your local version

  `config.json`
   This is the configuration file to connect the bot to a Twitch account. Place it in the same folder as AerolithOnStream.exe or AerolithOnStream.py. The below example has fake credentials supplied:
   
		{
			"irc_token": "oauth:ab2cefg45hika25mntu34dsffsa143v3",
			"nick": "BotAccount",
			"channel": "Streamer",
			"theme": "Dark Black",
			"font": "Arial",
			"colours": ["yellow", "black", "sandy brown"]
		}
    
### Setting up your own bot
Instructions adapted from https://github.com/danibarker/TwitchBot. You can run AerolithOnStream.py if you have python, or the exe if you don't.

  	1. Create a new Twitch account with the username you want the bot to have and log in.

  	2. Go to https://twitchapps.com/tmi/ and click Connect. Copy what is in the text box including "oauth:".

  	3. Open config.json and replace the lines with your information before saving it. Be sure to leave the variables in quotes:
	  	
		irc_token is the oauth, make sure it includes the text "oauth:" and not just the rest of the string
	  	nick is your bot's username
	  	channel is your stream channel
		theme is your preferred theme (default is Dark Black - you can select your favourite at https://pysimplegui.readthedocs.io/en/latest/cookbook/#themes-window-beautification)
		font is your preferred font
		colours are your preferred three colours for the top three positions - you may refer to https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Color_Names_Smaller_List.py for colour names or use hex codes

  	4. That's it, run AerolithOnStream.exe or AerolithOnStream.py and you should see a message on the console saying "Bot <Bot's nick> has joined the channel <Streamer>!"
    
    5. You will need to have the PyAutoGUI and PySimpleGUI packages installed to run AerolithOnStream.py.

### How to use the bot

	1. First, start up your Aerolith session and enter a room / table. Copy the room / table number.
	
	2. Paste the room / table number into the "Room Number" field.
	
	3. Start the round on Aerolith BEFORE clicking "Start" in the program. The bot will send the message "Starting Aerolith On Stream!"
	
	4. After this, the bot will type out and enter stream chat messages sent - so switch your cursor back into Aerolith. (WARNING: Do not put your cursor in Twitch chat or the account that is logged in will start spamming!)
	
	5. The bot will only send guesses if the letters in the stream message match one of the words in the quiz.
	
	6. The bot will automatically deactivate when the quiz timer has expired. You can also manually deactivate it by typing in "!end" (streamer only) or clicking on "End" in the program. If so, the bot will send the message "Ending Aerolith On Stream!"
	
	7. To begin a new round, once again, start the round on Aerolith before clicking on "Start" in the program (staying in the same room / table will eliminate the need to update it).
	
	8. To clear the scoreboard and "nopeboard" in between rounds, uncheck "Retain scores across rounds" before clicking "Start" in the program.
