import pyautogui
import socket
import threading
import string
import re
import config as cf

config = cf.config()

SERVER = "irc.twitch.tv"
PORT = 6667
message = ""

irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + config.irc_token + "\n" +
        "NICK " + config.nick + "\n" +
        "JOIN #" + config.channel + "\n").encode())

def runGame():
    global message
    global user
    while True:
        if message == "!end" and user == config.nick:
            break
        elif message != "":
            try:
                pyautogui.typewrite(message)
                pyautogui.press('enter')
                message = ""
            except:
                # There was some issue typing the msg. Print it out, and move on.
                print("Typing this particular message didn't work: " + message)

def gameControl():
    global message
    global user
    while True:
        if message == "!start" and user == config.nick:
            message = ""
            runGame()       


def twitch():
    def joinChat():
        loading = True
        while loading:
            readbuffer_join = irc.recv(1024).decode() #receiving 1024 bits/bytes at a time, save in readbuffer join
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                loading = loadingComplete(line)
    def loadingComplete(line):
        if ("End of /NAMES list" in line):
            print("Bot has joined " + config.channel + "'s channel!")
            #sendMessage(irc, "Chat room joined!")
            return False
        else:
            return True
    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + config.channel + " :" + message
        irc.send((messageTemp + "\n").encode())

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
                print(user + ": " + message)

if __name__ == "__main__":
    t1 = threading.Thread(target = twitch)
    t1.start()
    t2 = threading.Thread(target = gameControl)
    t2.start()