p = """
██████╗ 
██╔══██╗
██████╔╝
██╔═══╝ 
██║     
╚═╝     







        """
o = """
 ██████╗ 
██╔═══██╗
██║   ██║
██║   ██║
╚██████╔╝
 ╚═════╝ 
         """
k = """
██╗  ██╗
██║ ██╔╝
█████╔╝ 
██╔═██╗ 
██║  ██╗
╚═╝  ╚═╝
        """
e = """
███████╗
██╔════╝
█████╗  
██╔══╝  
███████╗
╚══════╝

        """
f = """
███████╗
██╔════╝
█████╗  
██╔══╝  
██║     
╚═╝     
        """
l = """
██╗     
██║     
██║     
██║     
███████╗
╚══════╝
        """
i = """
██╗
██║
██║
██║
██║
╚═╝
   """
g = """
 ██████╗ 
██╔════╝ 
██║  ███╗
██║   ██║
╚██████╔╝
 ╚═════╝ 
         """
h = """
██╗  ██╗
██║  ██║
███████║
██╔══██║
██║  ██║
╚═╝  ╚═╝
        """
t = """
████████╗
╚══██╔══╝
   ██║   
   ██║   
   ██║   
   ╚═╝   
         """

from kolyre import Kolyre
import time
import sys

Kolyre.enable_ansi_support()
import time, os, sys


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


esc = "\x1b"


def clear():
    sys.stdout.write(f"{esc}[2J")


def goto(r, c, text):
    sys.stdout.write(f"{esc}[{r};{c}H")

    for i in range(0,r):
        sys.stdout.write(f"{esc}[{i};{c}H")
        sys.stdout.write(text)
        sys.stdout.flush()
        # for z in range(0,i):
        sys.stdout.write(f"{esc}[{i+1};1H{esc}[2K")
        sys.stdout.write(f"{esc}[{i+2};1H{esc}[2K")



        time.sleep(0.1)
    # sys.stdout.write(f"{esc}[{r};{c + 10}H")
    clear()
    sys.stdout.write(color_split(text, split_rows=2))


clear()
# sys.stdout.write(f"{esc}[?25l")
# goto(9, 10, color_split(p, 2))
# goto(1,10,o)
pokeball_mini = """

   ▄███████████▄
  ██▓▓▓▓▓▓▓▓▓▓▓██
 ██▓▓▓▓▓███▓▓▓▓▓██
 ██████░░█░░██████
 ██░░░░░███░░░░░██
  ██░░░░░░░░░░░██
   ▀███████████▀
     █████████        
"""
print(pokeball_mini)