# Me make snake robot for slack

### User Flow - requirements
1. `/guesswho` @name
2. somehow lookup jukebot: who added the song
3. if name matches the user who added song to jukebot, guesser-tally++
- Mitches idea:
1. `/guesswho` @name
2. my bot provides a poll, some way for users to guess which user has added the song
3. after time interval, lookup /whom and show which users were the winners

### Tech Specs
- Python
- Heroku
- SQL database to store tallys

### Blocks
- How the hecka am I going to lookup from my bot, which user added the current song to jukebot
- Ideal: my bot responds with /whom, and parse JukeBot response
- Block: I dont think JukeBot will respond to bot users
- More likely: have to authenticate with JukeBot API to make /whom request


# Side-Quest:
- See: ~/Workspace/Journal/.bin/rename.py
I saved a file I dont want as .lol file extension
Github then said that the repo was LOLCODE was the main language used

If you ever wanna moonlight as being a ${language} developer, just push a huge file and label it with the ${language.fileExtension} extension.
OK only works for some languages: lolcode is one.
tried for rust and go, but I think for rust and go, github has better language "recognition" (bro you got some AI going on bro?) and neither of those really worked