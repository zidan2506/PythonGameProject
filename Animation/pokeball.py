
pokeball = """

         ▄██████████▄
       ▄███▓▓▓▓▓▓▓▓███▄
      ███▓▓▓▓▓▓▓▓▓▓▓▓███
     ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
    ██▓▓▓▓▓▓██████▓▓▓▓▓▓██
    ████████░░██░░████████
    ██░░░░░░██████░░░░░░██
     ██░░░░░░░░░░░░░░░░██
      ██░░░░░░░░░░░░░░██
       ▀███░░░░░░░░░███▀
          ▀█████████▀


"""
print(pokeball)
import sys, time
esc = "\x1b"

def goto(r, c, text=""):
    sys.stdout.write(f"{esc}[{r};{c}H{text}")
    sys.stdout.flush()

def clear():
    sys.stdout.write(f"{esc}[2J{esc}[H")
    sys.stdout.flush()

# dữ liệu logo
poke_text = "POKE"
flight_text = "FLIGHT"

def animate_poke_and_flight():
    clear()
    screen_width = 80
    center_col = (screen_width - len(poke_text)) // 2
    row_poke = 5
    row_flight_final = row_poke

    # --- Animation 1: POKE chạy ngang ---
    for col in range(0, center_col + 1, 2):
        clear()
        goto(row_poke, col, poke_text)
        time.sleep(0.05)

    # giữ chữ POKE tại vị trí cuối
    poke_fixed_col = center_col
    for row in range(0, row_flight_final + 1):
        clear()
        goto(row_poke, poke_fixed_col, poke_text)  # giữ nguyên POKE
        goto(row, poke_fixed_col + len(poke_text) + 1, flight_text)  # FLIGHT rớt xuống
        time.sleep(0.05)

    # dừng lại với cả 2 chữ cố định
    goto(row_poke, poke_fixed_col, poke_text)
    goto(row_flight_final, poke_fixed_col + len(poke_text) + 1, flight_text)

animate_poke_and_flight()
