
from kolyre import Kolyre
Kolyre.enable_ansi_support()
import time, sys
poke = """
██████╗  ██████╗ ██╗  ██╗███████╗
██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝
██████╔╝██║   ██║█████╔╝ █████╗  
██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  
██║     ╚██████╔╝██║  ██╗███████╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                 """
flight = """
███████╗██╗     ██╗ ██████╗ ██╗  ██╗████████╗
██╔════╝██║     ██║██╔════╝ ██║  ██║╚══██╔══╝
█████╗  ██║     ██║██║  ███╗███████║   ██║   
██╔══╝  ██║     ██║██║   ██║██╔══██║   ██║   
██║     ███████╗██║╚██████╔╝██║  ██║   ██║   
╚═╝     ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                             """
ball= """
         ▄░░░░░░░░░▄
       ▄░░░████████░░░▄
      ░░░████████████░░░
     ░░████████████████░░
    ░░██████░░░░░░██████░░
    ░░░░░░░░░████░░░░░░░░░
    ░░██████░░░░░░█████░░░
     ░░████████████████░░
      ░░██████████████░░
       ▀░░░████████░░░▀
          ▀░░░░░░░░░▀
"""

esc = "\x1b"
def clear():
    sys.stdout.write(f'{esc}[2J')

def goto(r,c):
    sys.stdout.write(f"{esc}[{r};{c}H")

def draw_art(r,c,text):
    line = text.strip("\n").splitlines()
    for k, l in enumerate(line):
        goto(r+k,c)
        sys.stdout.write(l)
def color_split(ascii_art: str, split_rows: int, top=Kolyre.RED, bottom=Kolyre.foreground_256(15)):
    raw_lines = ascii_art.splitlines()
    # Find the real text
    start = 0
    end = len(raw_lines) - 1
    while start < len(raw_lines) and raw_lines[start] == "":
        start += 1
    while end >= 0 and raw_lines[end] == "":
        end -= 1
    # return print(start),print(end)
    text = []
    index_ascii = -1
    for i, line in enumerate(raw_lines):
        if start <= i <= end:
            index_ascii += 1
            paint = top if index_ascii <= split_rows else bottom
        else:
            paint = top
        text.append(f"{paint}{line}{Kolyre.RESET}")

    return "\n".join(text)

clear()
# draw_art(10,40,color_split(poke,3))
def animation(poke_xy,flight_xy,ball_xy):
    poke_fixed =False
    flight_fixed =False
    ball_fixed =False
    poke_col = 0
    flight_row = 0
    ball_col = 150
    while not poke_fixed:
        clear()
        poke_col +=2
        draw_art(poke_xy[0],poke_col,color_split(poke,2))
        sys.stdout.flush()
        time.sleep(0.01)
        if poke_col >= poke_xy[1]+10:
            poke_col = poke_xy[1]+10
            poke_fixed = True
    while not ball_fixed:
        clear()
        draw_art(poke_xy[0],poke_xy[1]+10,color_split(poke,2))
        ball_col -=7
        draw_art(ball_xy[0],ball_col,color_split(ball,4))
        sys.stdout.flush()
        time.sleep(0.03)
        sys.stdout.write(f'{esc}[?25l')

        if ball_col <= poke_xy[1]+45:
            ball_col = poke_xy[1]+45
            ball_fixed = True
    while not flight_fixed:
        clear()
        draw_art(poke_xy[0],poke_xy[1],color_split(poke,2))
        draw_art(ball_xy[0],ball_xy[1],color_split(ball,4))
        flight_row += 1
        draw_art(flight_row, flight_xy[1],color_split(flight,2))
        sys.stdout.flush()
        time.sleep(0.03)
        sys.stdout.write(f'{esc}[?25l')

        if flight_row >= flight_xy[0]:
            flight_row = flight_xy[0]
            flight_fixed = True
# lm = 0
# while lm != 5:
#     lm=+1
animation([10,30],[10,70],[7,120])



