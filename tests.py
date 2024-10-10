def find_online_line(text):
    for line in text.splitlines():
        if "online" in line.lower():
            return line

with open("text.txt","r") as f:
    print(find_online_line(f.read()))