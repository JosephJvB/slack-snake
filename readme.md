# Me make snake robot for slack

- https://api.slack.com/events
- https://github.com/slackapi/python-slackclient
- https://github.com/slackapi/python-slackclient/tree/master/tutorial

### todo:
- Stop @ing people
    1. data migration, map user ids to real user names
    2. save real user names
    3. yah yeet yah

### User Flow
1. make it more like AirNZ quiz
    - Track starts
    - Whombot posts guess options: who added the track (or what the name of the track is)
    - Everyone can respond via reacts
    - Points are given to users at the end of the track
    - Bot posts correct answer
2. stuff quiz another thing i could try copy?

### Tech Specs
- Python
- Heroku
- SQL database to store tallys


# python notes
`ctrl` + `d` to end pipenv shell
- dicts, {}, dictVar['dictproperty']
- list, [], listVar[idx]
- class, class x:, class.property, class.method

# Side-Quest:
- See: ~/Workspace/Journal/.bin/rename.py
I saved a file I dont want as .lol file extension
Github then said that the repo was LOLCODE was the main language used

If you ever wanna moonlight as being a ${language} developer, just push a huge file and label it with the ${language.fileExtension} extension.
OK only works for some languages: lolcode is one.
tried for rust and go, but I think for rust and go, github has better language "recognition" (bro you got some AI going on bro?) and neither of those really worked





error:
```
2019-11-10T20:45:08.206195+00:00 app[worker.1]: File "./main.py", line 19, in on_message
2019-11-10T20:45:08.207561+00:00 app[worker.1]: elif data['text'].startswith(os.environ['WHOM_CMD']):
2019-11-10T20:45:08.207731+00:00 app[worker.1]: KeyError: 'text'
```
