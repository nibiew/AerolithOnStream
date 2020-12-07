# Aerolith On Stream
A basic Twitch bot that relies on pyautogui to run Aerolith on stream.

## Files you need on your local version

  `config.json`
   This is the configuration file to connect the bot to a Twitch account (fake credentials supplied).
	{
		"irc_token": "oauth:ab2cefg45hika25mntu34dsffsa143v3",
		"nick": "BotAccount",
		"channel": "Streamer"
	}
      
    
## Setting up your own bot
### Instructions adapted from https://github.com/danibarker/TwitchBot. You can run AerolithOnStream.py if you have python, or the exe if you don't.

  	1. Create a new Twitch account with the username you want the bot to have

  	2. Go to https://twitchapps.com/tmi/ and click Connect, copy what is in the text box including "oauth:"

  	3. Sign in as that account and go here: https://dev.twitch.tv/console/apps/create

  	4. Register a new application. The name is not important, it isn't shown anywhere except in your applications list

  	5. Paste the oauth you got earlier, you'll also need to put this into config.json (just open in notepad or similar)

  	6. Choose Chat Bot for Category

  	7. Click Create

  	8. Open config.json and replace the lines with your information. Be sure to leave the variables in quotes:
	  	
		irc_token is the oauth, make sure it includes the text "oauth:" and not just the rest of the string
	  	nick is your bot's username
	  	channel is your stream channel

  	9. Save this file

  	10. That's it, run aerolithonstream.exe or AerolithOnStream.py and it should connect and show a message saying "Bot has joined <Streamer>'s channel!"
    
    11. You will need to have the pyautogui package installed to run AerolithOnStream.py.

## How to use the bot

The bot can be activated with the streamer typing in "!start" (preferably using another device). After this, the bot will type out and enter any stream chat messages sent - so make sure that your cursor is typing into Aerolith before activating it. The bot can be deactivated with the streamer typing in "!end" or closing the program.