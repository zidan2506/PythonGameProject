from kolyre import Kolyre

def airport_ani(name):

    a = r"""
                                                   _
                     ___                          (_)
                   _/XXX\        
    _             /XXXXXX\_                                    __
    X\__    __   /X XXXX XX\                          _       /XX\__      ___
        \__/  \_/__       \ \                       _/X\__   /XX XXX\____/XXX\
      \  ___   \/  \_      \ \               __   _/      \_/  _/  -   __  -  \
     ___/   \__/   \ \__     \\__           /  \_//  _ _ \  \     __  /  \____/
    /  __    \  /     \ \_   _//_\___    __/    //           \___/  \/     __/
    __/_______\________\__\_/________\__/_/____/_____________/_______\____/____
                                      ___
                                     /L|0\
                                    /  |  \
                                   /       \
                                  /    |    \
                                 /           \
                                /  __  | __   \
                               /  __/    \__   \
                              /  /__   |  __\   \
                             /___________________\
                            /          |          \
                           /           |           \
    """
    b= r"""
                 _|_ 
            ____/___\____      
     ___________[o0o]___________
              O   O   O
    """
    esc = "\x1b"
    import itertools,sys,time
    def clear():
        sys.stdout.write(f"{esc}[2J")
    def goto(r,c):
        sys.stdout.write(f"{esc}[{r};{c}H")
    def draw_art(r, c, text):
        line = text.strip("\n").splitlines()
        for k, l in enumerate(line):
            goto(r + k, c)
            sys.stdout.write(l)
    def animation(x,y,):
        ani_condi =False
        ani_row = 20
        ani_col = y
        color = itertools.cycle([14,15,3,2,13,1])

        while not ani_condi:
            clear()
            ani_row -=1
            draw_art(1,70,a)
            draw_art(ani_row,ani_col, b)

            draw_art(4, 106, f"{Kolyre.foreground_256(next(color))}{Kolyre.BOLD}\r{name}{Kolyre.RESET}")

            sys.stdout.flush()
            time.sleep(0.1)
            if ani_row <= x:
                ani_condi = True
                ani_row = x

    animation(10,91)
    # draw_art(15,91,b)
# airport_ani()