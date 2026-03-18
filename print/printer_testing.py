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

santa_clue = "\n\n\
Where cola once flowed,\n\
the plant all but forgotten,\n\
yet left us a Splash.\n\
\n\
Carbonated waves,\n\
a frothy sea of soda,\n\
on a Sandy shore.\n\
\n\
Liquid silver face,\n\
two seven near the zipper,\n\
solve and hit Paydirt.\n\n"

p = printer.Network(PRINTER_LOCAL_IP, profile=PRINTER_PROFILE)

p.set(align='center')

image = "/home/brentvasas/documents/projects/receipt_printer/tmp/santa.jpg"

p.image(image)

p.text(santa_clue)

p.image(image)

#p.text("\n\nThe quick brown fox jumped over the lazy dog 0123456789\n\n")

p.cut()


#im = EscposImage("/home/brentvasas/downloads/test_apple.png")