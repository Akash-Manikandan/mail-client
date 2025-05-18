from sqlmodel import create_engine
from constants import DATABASE_URL

engine = create_engine(DATABASE_URL)