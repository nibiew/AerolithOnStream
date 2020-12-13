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

config = cf.config()

SERVER = "irc.twitch.tv"
PORT = 6667
message = ""
scores = {}
badguess = {}

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + config.irc_token + "\n" +
        "NICK " + config.nick + "\n" +
        "JOIN #" + config.channel + "\n").encode())
        
def twitch():
    global window
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
        global user
        separate = line.split(":", 2) #split by colon, up to two times
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(line):
        global message
        try:
            message = line.split(":", 2)[2] #split by colon, up to two times
        except:
            message = ""
        return message

    joinChat()

    while True:
        try:
            readbuffer = irc.recv(1024).decode() #receiving 1024 bits/bytes at a time, save in readbuffer join
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

def containsAll(string1, string2): #longer string is string1
    for c in string2:
        if c not in string1: return False
        string1 = string1.replace(c, '', 1)
    return True
        
def gameControl(t, alpha, words, blank, blank_length):
    global message, user, event, window, values, scores, badguess
    endtime = datetime.datetime.now() + datetime.timedelta(seconds = float(t))
    window['-OUTPUT-'].update('Aerolith On Stream has started!', text_color = 'red')
    sendMessage(irc, "Starting Aerolith On Stream!")
    solved = []
    window['-MESSAGES-'+sg.WRITE_ONLY_KEY].update('')
    if values['-SAVESCORE-'] == False:
        scores = {}
        badguess = {}
        window['-SCORES-'+sg.WRITE_ONLY_KEY].update('')
        window['-BADGUESS-'+sg.WRITE_ONLY_KEY].update('')
    while datetime.datetime.now() < endtime:
        if (message == "!end" and user == config.channel) or event == 'End':
            sendMessage(irc, "Ending Aerolith On Stream!")
            break
        elif message != "":
            message = ''.join(message.split()).upper() #remove spaces
            sortedMessage = ''.join(sorted(message))
            if not blank:
                if not sortedMessage in alpha: #wrong letters
                    message = ""
                    continue
            elif len(message) != blank_length or not any(containsAll(sortedMessage, string) for string in alpha): #blank quiz - probably slower.
                message = ""
                continue
            try:
                pyautogui.typewrite(message)
                pyautogui.press('enter')
                if message in words:
                    window['-MESSAGES-'+sg.WRITE_ONLY_KEY].print(user + ": " + message, background_color='green')
                    solved.append(message)
                    if message in words: words.remove(message) #if statement added to reduce crashes
                    if not user in scores:
                        scores[user] = 1
                    else:
                        scores[user]+= 1
                    window['-SCORES-'+sg.WRITE_ONLY_KEY].update('')
                    rank = 1
                    for u in sorted(scores, key=scores.get):
                        if rank > len(scores)-3:
                            window['-SCORES-'+sg.WRITE_ONLY_KEY].print(u + ': ' + str(scores[u]), text_color=config.colours[len(scores) - rank]) #default is ["yellow", "black", "sandy brown"]
                        else:
                            window['-SCORES-'+sg.WRITE_ONLY_KEY].print(u + ': ' + str(scores[u]))
                        rank += 1
                elif message.upper() in solved: #guessed before
                    window['-MESSAGES-'+sg.WRITE_ONLY_KEY].print(user + ": " + message, background_color='grey')
                else: #wrong guess
                    window['-MESSAGES-'+sg.WRITE_ONLY_KEY].print(user + ": " + message, background_color='red')
                    if not user in badguess:
                        badguess[user] = 1
                    else:
                        badguess[user]+= 1
                    window['-BADGUESS-'+sg.WRITE_ONLY_KEY].update('')
                    for u in sorted(badguess, key=badguess.get):
                        window['-BADGUESS-'+sg.WRITE_ONLY_KEY].print(u + ': ' + str(badguess[u]))
            except:
                print("There was some issue with this message: " + message)
            finally:
                message = ""
    window['-OUTPUT-'].update('Aerolith On Stream is not running.', text_color='white')



def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + config.channel + " :" + message
    irc.send((messageTemp + "\n").encode())


sg.theme(config.theme) #default is Dark Black

# Define the window's contents
layout = [[sg.Text('Bot has not joined the channel.',size=(40,1), key='-BOTSTATUS-', font=config.font)], #default font is Arial
    [sg.Text('Aerolith On Stream is not running.', size=(40,2), key='-OUTPUT-', font = config.font)],
    [sg.Text('Guesses:', font = config.font)],
    [sg.MLine(size=(40,5), disabled=True, key='-MESSAGES-' + sg.WRITE_ONLY_KEY, font = config.font)], 
    [sg.Text('Scoreboard:', font = config.font)],
    [sg.MLine(size=(40,5), disabled=True, key='-SCORES-'+ sg.WRITE_ONLY_KEY, font = config.font)], 
    [sg.Text('Nopeboard:', font = config.font)],
    [sg.MLine(size=(40,5), disabled=True, key='-BADGUESS-'+ sg.WRITE_ONLY_KEY, font = config.font)], 
    [sg.Text('Room Number', font = config.font), sg.InputText(key='-ROOM-', size=(8,1), font = config.font)], 
    [sg.Checkbox('Retain scores across rounds', key='-SAVESCORE-', default=True, font = config.font)], 
    [sg.Button('Start', font = config.font), sg.Button('End', font = config.font)]]

# Create the window
global window
window = sg.Window('Aerolith On Stream', layout, finalize=True)

if __name__ == "__main__":
    t1 = threading.Thread(target = twitch)
    t1.start()

# Display and interact with the Window using an Event Loop
while True:
    global event, values
    
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
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
        time = data['time_remaining']
        alpha = []
        words = []
        for question in data['questions']:
            alpha.append(question['a'])
            words.extend(question['ws'])
        blank = any('?' in string for string in alpha) #checks if this is a blank quiz
        blank_length = len(alpha[0]) #get length of first alphagram for blank quizzes
        alpha = [s.replace('?', '') for s in alpha]
        t2 = threading.Thread(target = gameControl, args=(time,alpha,words,blank,blank_length,))
        t2.start()
# Finish up by removing from the screen
window.close()