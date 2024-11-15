from datetime import datetime
from operator import truediv

import telegram_bot

#FORMAT: -- 2024-10-24 08:07:12.457018 --
def check_date(string, date, hour):
    if string.split()[1] == str(date) and string.split()[2][:2] == str(hour):
        return True
    else:
        return False

def report(date, hour):
    # Checks errors and warning msgs in logbook and sends a report as a telegram msg
    try:
        with open("logbook.txt", "r") as logbook:
            nr_devices, nr_errors, nr_warnings = 0,0,0
            warnings = []
            flag = False
            for line in logbook:
                #Checks the initialization date and hour
                if line[:2] == "--" and line.split()[1] == str(date) and line.split()[2][:2] == str(hour):
                    flag = True

                if flag and len(line) > 0:
                    nr_devices += 1
                    if "error" in line.lower():
                        nr_errors += 1
                    elif "warning" in line.lower():
                        nr_warnings += 1
                        warnings.append(line)
                # Stops reading the logs when finds another init line
                if flag and line[:2] == "--":
                    break

    except Exception as e:
        exception_message = f"Prob couldn't find logbook.txt file to read from | Exception: {e}"
        print(exception_message)
        telegram_bot.send_message(exception_message.splitlines()[0])

    telegram_bot.send_message(f"📝 Report from {date}\n✅ Devices status: {nr_devices-nr_warnings} / {nr_devices} online")

    if nr_errors > 0:
        telegram_bot.send_message(f"❌ Couldn't view the popup content on {nr_errors} / {nr_devices} devices")

    if nr_warnings > 0:
        for line in warnings:
            message = " ".join(line.split()[2:]).replace("|","\n")
            telegram_bot.send_message(f"⚠️ {message}")

def init():
    #stamps the log with current date & time
    with open("logbook.txt", "a+") as logbook:
        logbook.write(f"-- {datetime.now()} --\n")

def write_log(text):
    # records the text in the loogbook.txt file
    with open("logbook.txt","a+") as logbook:
        logbook.write(f"{datetime.now()}: {text}\n")
