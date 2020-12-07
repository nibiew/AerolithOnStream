import json
def json_decoder(obj):
    try:
        return Config(obj['irc_token'], 
                    obj['nick'],
                    obj['channel'],
                    )
    except KeyError:
        return obj
      
class Config:
    def __init__(self,irc_token,nick,channel):
       self.irc_token = irc_token
       self.nick = nick
       self.channel = channel
def config():       
    f = open('config.json', 'r')
    config = json.loads(f.read(), object_hook=json_decoder)
    f.close()
    return config