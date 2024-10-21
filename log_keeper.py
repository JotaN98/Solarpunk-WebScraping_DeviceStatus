from datetime import datetime
import telegram_bot

def report(date):
    # Checks errors and warning msgs in logbook and sends a report as a telegram msg
    try:
        with open("logbook.txt", "r") as logbook:
            nr_devices, nr_errors, nr_warnings = 0,0,0
            warnings = []

            for line in logbook:
                if len(line.split()) > 0 and line.split()[0] == str(date):
                    nr_devices += 1
                    if "error" in line.lower():
                        nr_errors += 1
                    elif "warning" in line.lower():
                        nr_warnings += 1
                        warnings.append(line)
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
    # records the text (including emojis) in the loogbook.txt file
    with open("logbook.txt","a+") as logbook:
        logbook.write(f"{datetime.now()}: {text}\n")
