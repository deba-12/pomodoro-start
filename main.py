from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
paused = False
remaining_time = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    window.after_cancel(timer)
    global reps, paused, remaining_time
    reps = 0
    paused = False
    remaining_time = 0
    canvas.itemconfig(timer_text, text="00:00")
    check.config(text="")
    Timer_label.config(text="Timer")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start():
    global reps, paused
    if paused:
        count_down(remaining_time)
        paused = False
    else:
        reps += 1
        if reps % 8 == 0:
            count_down(LONG_BREAK_MIN * 60)
            Timer_label.config(text="Long_Break", fg=RED)
        elif reps % 2 == 0:
            count_down(SHORT_BREAK_MIN * 60)
            Timer_label.config(text="Short_Break", fg=PINK)
        else:
            count_down(WORK_MIN * 60)
            Timer_label.config(text="Work", fg=GREEN)


#  ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, remaining_time
    minute = math.floor(count / 60)
    sec = count % 60
    if sec < 10:
        sec = f"0{sec}"
    canvas.itemconfig(timer_text, text=f"{minute}:{sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
        remaining_time = count - 1
    else:
        start()
    marks = ""
    for _ in range(math.floor(reps / 2)):
        marks += "✅"
    check.config(text=marks)

# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause():
    global paused
    if timer is not None:
        window.after_cancel(timer)
        paused = True

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=photo)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)
Timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 45, "bold"), bg=YELLOW)
Timer_label.grid(row=0, column=1)

Start = Button(text="Start", command=start, fg=GREEN, bg=RED, highlightthickness=0)
Start.grid(column=0, row=2)
Pause = Button(text="Pause", command=pause, fg=PINK, bg=GREEN, highlightthickness=0)
Pause.grid(column=1, row=2)
Reset = Button(text="Reset", highlightthickness=0, fg=RED, bg=GREEN, command=reset)
Reset.grid(column=2, row=2)
check = Label(fg=GREEN, bg=YELLOW)
check.grid(column=1, row=3)
window.mainloop()
