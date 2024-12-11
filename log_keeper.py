from datetime import datetime
import telegram_bot

def report_last_session():
    # Checks errors and warning msgs in logbook and sends a report as a telegram msg
    try:
        session_delimiter = "-- "
        nr_devices, nr_errors, nr_warnings = 0,0,0
        warnings = []

        with open("logbook.txt", "r") as file:
            for line in reversed(list(file)):
                line = line.strip()
                if line.startswith(session_delimiter):
                    # We found the last session delimiter; stop collecting
                    break
                if line:
                    nr_devices += 1
                    if "error" in line.lower():
                        nr_errors += 1
                    elif "warning" in line.lower():
                        nr_warnings += 1
                        warnings.append(line)

    except Exception as e:
        exception_message = f" Exception: {e}"
        print(exception_message)
        telegram_bot.send_message(exception_message.splitlines()[0])

    telegram_bot.send_message(f"📝 Report from {datetime.now().date()}\n✅ Devices status: {nr_devices-nr_warnings} / {nr_devices} online")

    if nr_errors > 0:
        telegram_bot.send_message(f"❌ Couldn't view the popup content on {nr_errors} / {nr_devices} devices")

    if nr_warnings > 0:
        for line in warnings:
            message = " ".join(line.split()[2:]).replace("|","\n")
            telegram_bot.send_message(f"⚠️ {message}")

def init():
    #stamps the log with current session "-- date & time --"
    with open("logbook.txt", "a+") as logbook:
        logbook.write(f"-- {datetime.now()} --\n")

def write_log(text):
    # records the text (including emojis) in the loogbook.txt file
    with open("logbook.txt","a+") as logbook:
        logbook.write(f"{datetime.now()}: {text}\n")
