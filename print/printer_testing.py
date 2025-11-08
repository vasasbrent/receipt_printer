from escpos import *
#from escpos import config

PRINTER_PROFILE='TM-T88V'
PRINTER_LOCAL_IP='192.168.1.178'

note_header = "\
   ______________________________________\n\
  |   __    _   ___    _______ .____     |\n\
  |   |\   |  .'   \`. '   /    /        |\n\
  |   | \  |  |     |     |    |__.      |\n\
  |   |  \ |  |     |     |    |         |\n\
  |   |   \|   `.__.'     /    /----/    |\n\
  |______________________________________|"

poem_header = "\
   ______________________________________\n\
  |    .-.                               |\n\
  |   (_) )-.                            |\n\
  |     .:   \  .-.    .-.  . ,';.,';.   |\n\
  |    .:'    );   ;'.;.-'  ;;  ;;  ;;   |\n\
  |  .-:. `--' `;;'   `:::'';  ;;  ';    |\n\
  | (_/                   _;        `-'  |\n\
  |______________________________________|"

memo_header = "\
   ______________________________________\n\
  |    __  __  ______  __  __   ____     |\n\
  |   |  \/  ||  ____||  \/  | / __ \    |\n\
  |   | \  / || |__   | \  / || |  | |   |\n\
  |   | |\/| ||  __|  | |\/| || |  | |   |\n\
  |   | |  | || |____ | |  | || |__| |   |\n\
  |   |_|  |_||______||_|  |_| \____/    |\n\
  |______________________________________|"


p = printer.Network(PRINTER_LOCAL_IP, profile=PRINTER_PROFILE)

p.text(poem_header)

#p.text("\n\nThe quick brown fox jumped over the lazy dog 0123456789\n\n")

p.cut()


#im = EscposImage("/home/brentvasas/downloads/test_apple.png")