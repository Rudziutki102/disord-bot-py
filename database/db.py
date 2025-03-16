from mongoengine import connect,errors
from config.settings import MONGO_URI
def connect_db():
    try:
        connect(db='discord-py',host=MONGO_URI)
        print("Połączono z MongoDB")
        return True
    except errors.ConnectionFailure as e:
        print(f"Błąd z mongo DB : {e}")
        return False
    
connect_db()
