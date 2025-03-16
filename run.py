from bot.main import run_bot
from database.db import connect_db

if __name__ == "__main__":
    if connect_db():
        run_bot()