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





ESC = "\x1b"

def goto(r, c):
    sys.stdout.write(f"{ESC}[{r};{c}H")

def clear_line_at(row):
    # tới đầu dòng rồi xóa cả dòng
    sys.stdout.write(f"{ESC}[{row};1H{ESC}[2K")

def draw_art(row, col, text):
    lines = text.strip("\n").splitlines()
    for k, line in enumerate(lines):
        goto(row + k, col)
        sys.stdout.write(line)

def erase_art(row, text):
    # xóa *mỗi dòng* của block
    lines = text.strip("\n").splitlines()
    for k in range(len(lines)):
        clear_line_at(row + k)
