from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", default="localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", default="3306"))
MYSQL_DB = "fast_track_db"
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mysqlking@02")
SECRET_KEY = os.getenv("SECRET_KEY")
