import os

# as it turns out, pipenv auto adds .env files
# so this is useless, besides learning pythons APIs hehe :)

def set_env ():
    added = []
    with open(".env") as f:
        raw = f.readlines()
        for line in raw:
            key, value = line.split("=") 
            os.environ[key] = value
            added.append(key)
        print("added to env:", added)
        return