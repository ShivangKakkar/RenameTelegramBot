# Change 'running' attribute to False for everyone in Database,
# everytime I stop the bot as it will be True for people who are currently renaming files.

# That's bad coding way. Know any other way ? ~ @StarkProgrammer [Telegram]


"""
from sqlalchemy.inspection import inspect
from RenameBot.database.users_sql import Users
from RenameBot.database import SESSION

keys = [key.name for key in inspect(Users).primary_key]

for key in keys:
    q = SESSION.query(Users).get(key)
    q.running = False
    SESSION.commit()
"""
