import sys
import re
import pyautogui
import socket
import threading
import string
import config as cf
import PySimpleGUI as sg
import requests
import json
import datetime
import time
import pyperclip
from util import containsAll


def joinChat():
    loading = True
    while loading:
        readbuffer_join = irc.recv(1024).decode() #receiving 1024 bits/bytes at a time, save in readbuffer join
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            loading = loadingComplete(line)

def loadingComplete(line):
    if ("End of /NAMES list" in line):
        print('Bot ' + config.nick + ' has joined the channel ' + config.channel + '!')
        window['-BOTSTATUS-'].update('Bot ' + config.nick + ' has joined the channel ' + config.channel + '!')
        return False
    else:
        return True

def getUser(line):
    separate = line.split(":", 2) #split by colon, up to two times
    user = separate[1].split("!", 1)[0]
    return user

def getMessage(line):
    try:
        message = line.split(":", 2)[2] #split by colon, up to two times
    except:
        message = ""
    return message

def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + config.channel + " :" + message
    irc.send((messageTemp + "\n").encode())

def twitch():
    global scoresRank
    while True:
        try:
            received = irc.recv(1024)
            readbuffer = received.decode() #receiving 1024 bits/bytes at a time, save in readbuffer join
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            if "PING" in line and not "PRIVMSG" in line: #responds to ping from server, needed to stay connected
                msg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msg)
                print(msg)
                continue
            else:
                user = getUser(line)
                message = getMessage(line)
                print(user + ": " + message) #useful for debugging purposes
                message = ''.join(message.split()).upper() #remove spaces
                if convert==True:
                    message = message.translate(str.maketrans('ñąćęłńóśźżÑĄĆĘŁŃÓŚŹŻ', 'NACELNOSZZNACELNOSZZ')) #change to english language characters
                else:
                    message = message.translate(str.maketrans('ñąćęłńóśźż', 'ÑĄĆĘŁŃÓŚŹŻ')) #change to upper case characters
                if started:
                    sortedMessage = ''.join(sorted(message))
                    if blank:
                        if len(message) != blank_length or not any(containsAll(sortedMessage, string) for string in alpha): #blank quiz - probably slower.
                            continue
                    elif subword:
                        if not containsAll(alpha[0], sortedMessage):
                            continue
                    elif not sortedMessage in alpha: #wrong letters
                        continue
                    try:
                        if polish or spanish:
                            pyperclip.copy(message)
                            pyautogui.hotkey('ctrl', 'v')
                        else:
                            pyautogui.typewrite(message) #should be faster?
                        pyautogui.press('enter')
                        if message in words:
                            window['-MESSAGES-' + sg.WRITE_ONLY_KEY].print(f"{user}: {message}", background_color='green')
                            solved.append(message)
                            if message in words: words.remove(message) #if statement added to reduce crashes
                            if not user in scores:
                                scores[user] = 1
                            else:
                                scores[user]+= 1
                            window['-SCORES-' + sg.WRITE_ONLY_KEY].update('')
                            rank = 1
                            scoresRank = sorted(scores, key=scores.get, reverse=True)
                            for u in scoresRank:
                                if rank <= 3: #add coloured ranks for top 3
                                    window['-SCORES-' + sg.WRITE_ONLY_KEY].print(f"{u}: {str(scores[u])}", text_color=config.colours[rank-1]) #default is ["yellow", "#bdb7ab", "sandy brown"]
                                else:
                                    window['-SCORES-' + sg.WRITE_ONLY_KEY].print(f"{u}: {str(scores[u])}")
                                rank += 1
                            window['-SCORES-' + sg.WRITE_ONLY_KEY].Widget.yview_moveto(0) #move to start
                            if not words: endGame('All words found!')
                        elif message.upper() in solved: #guessed before
                            window['-MESSAGES-' + sg.WRITE_ONLY_KEY].print(f"{user}: {message}", background_color='grey')
                        else: #wrong guess
                            window['-MESSAGES-' + sg.WRITE_ONLY_KEY].print(f"{user}: {message}", background_color='red')
                            if not user in badguess:
                                badguess[user] = 1
                            else:
                                badguess[user]+= 1
                            window['-BADGUESS-' + sg.WRITE_ONLY_KEY].update('')
                            badguessRank = sorted(badguess, key=badguess.get, reverse=True)
                            for u in badguessRank:
                                window['-BADGUESS-' + sg.WRITE_ONLY_KEY].print(u + ': ' + str(badguess[u]))
                            window['-BADGUESS-' + sg.WRITE_ONLY_KEY].Widget.yview_moveto(0) #move to start
                    except:
                        print("There was some issue with this message: " + message)

def endGame(msgToSend):
    global started, scoresRank, t2
    if started: #do nothing if started is false
        finalRanks = ' Leaderboard - '
        for i in range(min(5, len(scores))):
            user = scoresRank[i]
            finalRanks += f"{str(i+1)}. @{user}: {str(scores[user])} "
        sendMessage(irc, msgToSend + finalRanks)
        window['-OUTPUT-'].update('Aerolith On Stream is not running.', text_color='white')
        if t2.is_alive():
            t2.cancel() #cancel timer if it's still running
    started = False

def shuffle():
    global started, convert
    if started: #do nothing if started is false
        if values['-SHUFFLE-']==True:
            pyautogui.press('1')
        time.sleep(10)
        shuffle()

config = cf.config()
SERVER = "irc.twitch.tv"
PORT = 6667

scores = {}
badguess = {}
started = False
convert = False
endtime = datetime.datetime.now()

#Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + config.irc_token + "\n" +
        "NICK " + config.nick + "\n" +
        "JOIN #" + config.channel + "\n").encode())

sg.theme(config.theme) #default is Dark Black
sg.theme_input_background_color(config.input_background)

# Define the window's contents
layout = [[sg.Text('Bot has not joined the channel.',size=(40,1), key='-BOTSTATUS-', font=config.font)], #default font is Arial
    [sg.Text('Aerolith On Stream is not running.', size=(40,2), key='-OUTPUT-', font = config.font)],
    [sg.Text('Guesses:', font = config.font)],
    [sg.MLine(size=(40,config.box_height[0]+1), disabled=True, key='-MESSAGES-' + sg.WRITE_ONLY_KEY, font = config.font)], #+1 to height because there is an empty line at the end
    [sg.Text('Leaderboard:', font = config.font)],
    [sg.MLine(size=(40,config.box_height[1]+1), disabled=True, key='-SCORES-'+ sg.WRITE_ONLY_KEY, font = config.font)], #+1 to height because there is an empty line at the end
    [sg.Text('Nopeboard:', font = config.font)],
    [sg.MLine(size=(40,config.box_height[2]+1), disabled=True, key='-BADGUESS-'+ sg.WRITE_ONLY_KEY, font = config.font)], #+1 to height because there is an empty line at the end
    [sg.Text('Room Number', font = config.font), sg.InputText(key='-ROOM-', size=(8,1), font = config.font, enable_events=True)], 
    [sg.Checkbox('Retain scores across rounds', key='-SAVESCORE-', default=True, font = config.font)], 
    [sg.Checkbox('Shuffle letters every 10 seconds', key='-SHUFFLE-', default=False, font = config.font, enable_events=True)], 
    [sg.Checkbox('Convert special characters into English letters', key='-CONVERT-', default=False, font = config.font, enable_events=True)], 
    [sg.Button('Start', font = config.font), sg.Button('End', font = config.font)]]

# Create the window
window = sg.Window('Aerolith On Stream', layout, finalize=True)
window.FindElement("-MESSAGES-" + sg.WRITE_ONLY_KEY).Autoscroll = False
joinChat()
irc.setblocking(False)

t1 = threading.Thread(target = twitch)
t1.start()

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        islive=False
        print("window closed!")
        break
    elif event == '-ROOM-' and values['-ROOM-'] and values['-ROOM-'][-1] not in ('0123456789.'):
        window['-ROOM-'].update(values['-ROOM-'][:-1])
    elif event == 'Start':
        try:
            room = int(values['-ROOM-'])
        except ValueError:
            sg.popup('Key in your Aerolith room number!')
            
        client = requests.session()
        r = client.get('https://aerolith.org/wordwalls/api/answers/?tablenum=' + values['-ROOM-'])
        if r.status_code == 400:
            sg.popup('Invalid or inactive Aerolith room number!')
            continue
        elif r.status_code != 200:
            sg.popup('Error!')
            continue
        data = json.loads(r.content)
        gameTime = data['time_remaining']
        alpha = []
        words = []
        for question in data['questions']:
            alpha.append(question['a'])
            words.extend(question['ws'])
        blank = any('?' in string for string in alpha) #checks if this is a blank quiz
        polish = any(any(elem in string for elem in 'ĄĆĘŁŃÓŚŹŻ') for string in alpha) #checks if this is a polish quiz
        spanish = any(any(elem in string for elem in '123Ñ') for string in alpha) #checks if this is a spanish quiz
        if values['-CONVERT-']==True:
            alpha = [sub.translate(str.maketrans('ÑĄĆĘŁŃÓŚŹŻ', 'NACELNOSZZ')) for sub in alpha] 
            words = [sub.translate(str.maketrans('ÑĄĆĘŁŃÓŚŹŻ', 'NACELNOSZZ')) for sub in words]
        if spanish:
            dictionary = {"1": "CH", "2": "LL", "3": "RR"}
            alpha = [sub.translate(str.maketrans(dictionary)) for sub in alpha]
            alpha = [''.join(sorted(s)) for s in alpha] #sorting for CH
            words = [sub.translate(str.maketrans(dictionary)) for sub in words] 
        if polish:
            alpha = [''.join(sorted(s)) for s in alpha] #sorting special language characters
        subword = len(alpha)==1 and not all(len(x) == len(words[0]) for x in words) #checks if this is a subword quiz
        blank_length = len(alpha[0]) #get length of first alphagram for blank quizzes
        alpha = [s.replace('?', '') for s in alpha]
        window['-OUTPUT-'].update('Aerolith On Stream has started!', text_color = 'red')
        sendMessage(irc, "Starting Aerolith On Stream!")
        solved = []
        started = True
        window['-MESSAGES-' + sg.WRITE_ONLY_KEY].update('')
        if values['-SAVESCORE-'] == False:
            scores = {}
            badguess = {}
            window['-SCORES-' + sg.WRITE_ONLY_KEY].update('')
            window['-BADGUESS-' + sg.WRITE_ONLY_KEY].update('')
        t2 = threading.Timer(float(gameTime), endGame, ["Time's up!"])
        t2.start()
        t3 = threading.Timer(10, shuffle)
        t3.start()
    elif event == '-SHUFFLE-': #needed to update value so it can be read by shuffle thread.
        print('Shuffle turned {status}.'.format(status='on' if values['-SHUFFLE-'] else 'off'))
    elif event == '-CONVERT-': #needed to update value so it can be read by shuffle thread.
        convert = not convert
        print('Conversion of special language characters into English characters turned {status}.'.format(status='on' if values['-CONVERT-'] else 'off'))
    elif event == 'End':
        endGame('Game ended by streamer!')
# Finish up by removing from the screen
window.close()
