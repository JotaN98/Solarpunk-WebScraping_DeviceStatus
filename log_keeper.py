from datetime import datetime

def init():
    with open("logbook.txt", "a+", encoding="utf-8") as logbook:
        logbook.write(f"-- {datetime.now()} --\n")

def write_log(text):
    # records the text (including emojis) in the loogbook.txt file
    with open("logbook.txt","a+", encoding="utf-8") as logbook:
        logbook.write(f"{datetime.now()}: {text}\n")
