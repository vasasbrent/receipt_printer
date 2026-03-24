import sys

from escpos import printer

PRINTER_PROFILE = "TM-T88V"
PRINTER_LOCAL_IP = "192.168.1.178"


headers = {
    "note": "\
   ______________________________________\n\
  |   __    _   ___    _______ .____     |\n\
  |   |\\   |  .'   `. '   /    /         |\n\
  |   | \\  |  |     |     |    |__.      |\n\
  |   |  \\ |  |     |     |    |         |\n\
  |   |   \\|   `.__.'     /    /----/    |\n\
  |______________________________________|",
    "poem": "\
   ______________________________________\n\
  |    .-.                               |\n\
  |   (_) )-.                            |\n\
  |     .:   \\  .-.    .-.  . ,';.,';.   |\n\
  |    .:'    );   ;'.;.-'  ;;  ;;  ;;   |\n\
  |  .-:. `--' `;;'   `:::'';  ;;  ';    |\n\
  | (_/                   _;        `-'  |\n\
  |______________________________________|",
    "memo": "\
   ______________________________________\n\
  |    __  __  ______  __  __   ____     |\n\
  |   |  \\/  ||  ____||  \\/  | / __ \\    |\n\
  |   | \\  / || |__   | \\  / || |  | |   |\n\
  |   | |\\/| ||  __|  | |\\/| || |  | |   |\n\
  |   | |  | || |____ | |  | || |__| |   |\n\
  |   |_|  |_||______||_|  |_| \\____/    |\n\
  |______________________________________|",
}


def normalize_apostrophes(message: str) -> str:
    # Replace iOS/smart quote apostrophes with standard ASCII apostrophe
    return message.replace("\u2018", "'").replace("\u2019", "'")


def strip_unprintable(message: str) -> str:
    # Keep printable ASCII (0x20–0x7E) and newlines only.
    # Characters outside this range are either control bytes (which could
    # trigger unintended ESC/POS commands) or Unicode that the printer's
    # default PC437 code page cannot represent.
    return "".join(c for c in message if 0x20 <= ord(c) <= 0x7E or c == "\n")

def sanitize_string(in_string: str) -> str:
    in_string = normalize_apostrophes(in_string)
    in_string = strip_unprintable(in_string)
    return in_string

def format_message(message: str) -> str:
    output_lines = []
    for line in message.split("\n"):
        if not line:
            output_lines.append("")
            continue
        while len(line) > 38:
            break_at = line.rfind(" ", 0, 38)
            if break_at <= 0:
                break_at = 38
            output_lines.append("  " + line[:break_at].rstrip())
            line = line[break_at:].lstrip(" ")
        output_lines.append("  " + line)
    return "\n".join(output_lines)


if len(sys.argv) != 6:
    print("Usage: print_script.py <theme> <message> <sender_name> <ip> <device_info>", file=sys.stderr)
    sys.exit(1)

theme = sys.argv[1]
message = sys.argv[2]
sender_name = sys.argv[3].strip()
ip = sys.argv[4]
device_info = sys.argv[5]

sender_name = sanitize_string(sender_name)
message = sanitize_string(message)
message = format_message(message)

header = headers.get(theme)
if not header:
    print(f"Unknown theme: {theme}", file=sys.stderr)
    sys.exit(1)

p = printer.Network(PRINTER_LOCAL_IP, profile=PRINTER_PROFILE)
p.set(align="left")
p.text(header + "\n\n")
p.text(message + "\n\n")
p.set(align="right")
p.text(f"- {sender_name}  \n\n")
p.set(align="center")
p.text(f"- {ip} | {device_info} -\n")
p.cut()
