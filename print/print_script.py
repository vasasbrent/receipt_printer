import sys
from escpos import printer

PRINTER_PROFILE = 'TM-T88V'
PRINTER_LOCAL_IP = '192.168.1.178'

headers = {
    'note': "\
   ______________________________________\n\
  |   __    _   ___    _______ .____     |\n\
  |   |\\   |  .'   `. '   /    /        |\n\
  |   | \\  |  |     |     |    |__.      |\n\
  |   |  \\ |  |     |     |    |         |\n\
  |   |   \\|   `.__.'     /    /----/    |\n\
  |______________________________________|",
    'poem': "\
   ______________________________________\n\
  |    .-.                               |\n\
  |   (_) )-.                            |\n\
  |     .:   \\  .-.    .-.  . ,';.,';.   |\n\
  |    .:'    );   ;'.;.-'  ;;  ;;  ;;   |\n\
  |  .-:. `--' `;;'   `:::'';  ;;  ';    |\n\
  | (_/                   _;        `-'  |\n\
  |______________________________________|",
    'memo': "\
   ______________________________________\n\
  |    __  __  ______  __  __   ____     |\n\
  |   |  \\/  ||  ____||  \\/  | / __ \\    |\n\
  |   | \\  / || |__   | \\  / || |  | |   |\n\
  |   | |\\/| ||  __|  | |\\/| || |  | |   |\n\
  |   | |  | || |____ | |  | || |__| |   |\n\
  |   |_|  |_||______||_|  |_| \\____/    |\n\
  |______________________________________|",
}

if len(sys.argv) != 3:
    print("Usage: print_script.py <theme> <message>", file=sys.stderr)
    sys.exit(1)

theme = sys.argv[1]
message = sys.argv[2]

header = headers.get(theme)
if not header:
    print(f"Unknown theme: {theme}", file=sys.stderr)
    sys.exit(1)

p = printer.Network(PRINTER_LOCAL_IP, profile=PRINTER_PROFILE)
p.set(align='left')
p.text(header + '\n\n')
p.text(message + '\n')
p.cut()
