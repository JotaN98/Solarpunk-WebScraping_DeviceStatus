import telegram_bot

def report(date):
    try:
        with open("logbook.txt", "r", encoding="utf-8") as logbook:
            nr_devices, nr_errors, nr_warnings = 0,0,0
            errors, warnings = [],[]

            for line in logbook:
                if len(line.split()) > 0 and line.split()[0] == str(date):
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
        telegram_bot.send_message(exception_message.splitlines()[0])

    telegram_bot.send_message(f"🤖📝 Report from {date}\nDevices status: {nr_devices-nr_warnings} / {nr_devices} online \nCouldn't view the popup content on {nr_errors} / {nr_devices} devices")

    if nr_warnings != 0:
        for line in warnings:
            message = " ".join(line.split()[2:]).replace("|","\n")
            telegram_bot.send_message(message)