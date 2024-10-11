import telegram_bot
from datetime import datetime


def report(date):
    try:
        with open("logbook.txt", "r", encoding="utf-8") as logbook:
            nr_devices, nr_errors, nr_warnings = 0,0,0
            errors, warnings = [],[]

            for line in logbook:
                if len(line) > 0:
                    if line.split()[0] == str(date):
                        nr_devices += 1
                        if "error" in line.lower():
                            nr_errors += 1
                            errors.append(line)
                        elif "warning" in line.lower():
                            nr_warnings += 1
                            warnings.append(line)
    except Exception as e:
        exception_message = f"Prob couldn't find logbook.txt file to read from | Exception: {e}"
        print(exception_message)
        print(exception_message.splitlines()[0])

    if nr_warnings != 0:
        for line in warnings:
            print(line)

    print(f"🤖 Report from {date}\nDevices status: {nr_devices-nr_warnings} / {nr_devices} online \nCouldn't view the popup on {nr_errors} / {nr_devices} devices")

report(datetime.now().date())