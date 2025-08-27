from dotenv import load_dotenv, find_dotenv

if not load_dotenv(find_dotenv()):
    raise RuntimeError("Failed to load .env file")