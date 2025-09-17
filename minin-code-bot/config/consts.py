from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = os.getenv("API_ADDRESS")
LLAMA = os.getenv("LLAMA_ADDRESS")
GREETING = "Приветствую! Здесь ты сможешь просто и быстро познакомиться с миром IT в  Нижнем Новгороде!"
