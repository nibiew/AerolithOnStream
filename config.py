import json
def json_decoder(obj):
    try:
        return Config(obj['irc_token'], 
                    obj['nick'],
                    obj['channel'],
                    obj['theme'],
                    obj['font'],
                    obj['colours'],
                    obj['box_height']
                    )
    except KeyError:
        return obj
      
class Config:
    def __init__(self,irc_token,nick,channel,theme,font,colours,box_height):
       self.irc_token = irc_token
       self.nick = nick
       self.channel = channel
       self.theme = theme
       self.font = font
       self.colours = colours
       self.box_height = box_height
def config():       
    f = open('config.json', 'r')
    config = json.loads(f.read(), object_hook=json_decoder)
    f.close()
    return config