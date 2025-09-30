# import Intro
import sys,time
from loading import loading_ani
from airport import airport_ani
plane = r"""
        ______
        _\ _~-\___
=  = ==(____AA____D
            \_____\___________________,-~~~~~~~`-.._
            /     o O o o o o O O o o o o o o O o  |\_
            `~-.__        ___..----..                  )
                  `---~~\___________/------------`````
== =  =    =      =  ===(_________D
"""
esc = "\x1b"
sys.stdout.write(f"{esc}[?25l")
def del_row():
    sys.stdout.write(f"{esc}[2K")
def clear():
    sys.stdout.write(f'{esc}[2J')
def goto(r,c):
    sys.stdout.write(f"{esc}[{r};{c}H")
def draw_art(r,c,text):
    line = text.strip("\n").splitlines()
    for k, l in enumerate(line):
        goto(r+k,c)
        sys.stdout.write(l)
def animation_fly(x,y,str):
    ani_condi =False
    ani_row = x
    ani_col = 0
    while not ani_condi:
        clear()
        ani_col +=10
        draw_art(ani_row,ani_col,str)

        if ani_row <=0:
            goto(1,1)
            del_row()
        sys.stdout.flush()
        time.sleep(0.05)
        if ani_col >= y:
            ani_col = y
            ani_row = x
            ani_condi = True
            clear()
        ani_row -=1
def animation_down(x,y,str):
    ani_condi =False
    ani_row = 0
    ani_col = 0
    while not ani_condi:
        clear()
        ani_col +=10
        ani_row+=1
        draw_art(ani_row,ani_col,str)
        if ani_row <=0:
            goto(1,1)
            del_row()
        sys.stdout.flush()
        time.sleep(0.05)
        if ani_col >= y:
            ani_col = y
            ani_row = x
            ani_condi = True
            clear()
airport_ani("Espoo")
animation_fly(10,170,plane)
loading_ani()
animation_down(10,170,plane)
airport_ani("Helsinki")