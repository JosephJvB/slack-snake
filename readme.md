# Me make snake robot for slack

### todo
- !banger : gives points to the person who had requested the song
	- Ah problem...I cant query Jukebots db
	- !banger, my bot send command to Jukebot in DM and uses response to allocate point
	- or: !banger, my bot send /whom in playlist and allocate point - ending whom round

    https://github.com/ErikKalkoken/slackApiDoc


	I cant get my bot to message jukebot
	I can get my bot to call /whom in public playlist
	OR: says marc, I can get my bot to message me - and jukebot will respond there? to try

    banger release notes:
    1. run redis migration

### TIL:
 - https://github.com/os/slacker: I can have my bot send commands with `chat.command`
    - user types !whom @user
    - my bot message JukeBot in a private chat and check if guess was correct
    - I can tell the user to guess again, whatever, 3 guesses, then reveal later? Something like that.
    - Not much benefit to gain from it though I think, to be honest. But I now know I can do that.
- Enzo used a slack app: Simple Poll.
    - used an 'rich-embed' with buttons, like fancy emoji responses
    - also something I can do
