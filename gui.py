from tkinter import (Button, Frame, Label, Menu, Tk, messagebox)
import logic,  random


# set colours to be used in game
COLOURS = {
    "absent": "#3a3a3c",
    "present": "#b59f3b",
    "correct": "#538d4e",
    "text": "#ffffff",
    "bg": "#121213",
}

def main():

    # get valid 5 letter words
    all_words = open("words.txt", 'r+')
    valid_words = [word.strip('\n') for word in all_words.readlines()]
    all_words.close()

    # current puzzle
    room = 0

    # background for game
    # story = "The Great Star of Africa, the world's largest diamond, \
# is normally the most well-guarded treasure in the entire world. \
# Many thieves have tried and failed to even come close to this prized possession. \
# Buried behind layers and layers of security, there's no way in or out. \
# Everything changed when the news broke that a deal was signed to sell this diamond \
# to a rich Vegas Baron. The diamond will be transferred to a neutral vault \
# in a Vegas casino before being taken to lockdown - a once-in-a-lifetime chance. \
# As a master thief, you cannot miss this opportunity to go down in history \
# completing the greatest heist of all time.\n\n\
# To steal the diamond, you must go through a series of rooms. \
# Each room has a code word which must be entered to unlock the next room. \
# You have 6 guesses in each room - every guess reveals information about the code word. \
# If you do not find the code within this number of guesses, \
# an alarm will go off and you will be caught. Good luck!"

    # how to play
    instructions = "You have 6 attempts to guess the word. \
The guess must be a real word. Press enter/return to submit a guess. \
If a square turns grey, this letter is not in the word. \
A yellow square indicates that a letter is present but not \
in the correct position. A green square indicates that \
a letter is in the correct position."

    # display intro
    # def intro():
    #     messagebox.showinfo("Intro", story)

    # display instructions
    def help():
        messagebox.showinfo("How to play", instructions)

    # create prize window (only done if all puzzles solved successfully)
    def prize():
        # create window
        win = Tk()
        width = 500
        height = 200
        x, y = int((win.winfo_screenwidth() - width)/2), int((win.winfo_screenheight() - height)/2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        win.config(bg=COLOURS["bg"])
        win.focus_force()
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        # add winning label
        label = Label(win,
            text="Congratulations! You won!",
            fg=COLOURS["text"],
            bg=COLOURS["bg"],
            font=("Bahnschrift Bold", 20)
        )
        label.grid(pady=16, sticky="news")
        # add colour animation (this is super cool)
        colours = ["red", "orange", "yellow", "lightgreen", "lightblue", "violet"]
        current = 0
        def change():
            nonlocal current
            if current < len(colours):
                label.config(fg=colours[current])
            else:
                current = 0
                label.config(fg=colours[current])
            current += 1
            win.after(80, change)
        change()
        win.mainloop()

    def newgame():
        nonlocal room

        # initialize game
        room += 1
        entered = []
        guess = []
        over = False
        answer = random.choice(valid_words)

        # create window
        win = Tk()
        win.title("Wordle")
        width = 460
        height = 500
        x, y = int((win.winfo_screenwidth() - width)/2), int((win.winfo_screenheight() - height)/2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        win.config(bg=COLOURS["bg"])
        win.focus_force()

        # display room number
        room_label = Label(win,
            text=f"Room {room}",
            fg=COLOURS["text"],
            bg=COLOURS["bg"],
            font=("Bahnschrift Bold", 30)
        )
        room_label.grid(pady=16, sticky="news")

        # store tiles (labels) to update throughout game
        guessframe = Frame(win, bg=COLOURS["bg"])
        guessframe.grid(padx=80, pady=(0, 10))

        # create tiles
        mat = [[] for x in range(logic.NUMGUESSES)]
        for x in range(logic.NUMGUESSES):
            for y in range(logic.NUMLETTERS):
                square = Frame(guessframe,
                    width=52,
                    height=52,
                    bg = COLOURS["bg"],
                    highlightthickness=1,
                    highlightbackground=COLOURS["absent"]
                )
                square.grid_propagate(False)
                square.grid_rowconfigure(0, weight=1)
                square.grid_columnconfigure(0, weight=1)
                square.grid(row=x, column=y, padx=4, pady=4)
                text = Label(square,
                    font=("Clear Sans", 26, "bold"),
                    justify="center",
                    bg=COLOURS["bg"],
                    fg=COLOURS["text"]
                )
                text.grid(sticky="news")
                # add squares to matrix to change later
                mat[x].append(text)

        # handle keyboard events
        def keypress(event):
            nonlocal guess, over, win
            # if the puzzle is not solved
            if not over:
                # check for letter and update window
                if event.char.isalpha() and len(guess) < 5:
                    logic.add_letter(event.keysym, guess)
                    mat[len(entered)][len(guess)-1].config(text=guess[-1])
                elif event.keysym == "Return":
                    # check word validity
                    if logic.valid(guess, valid_words) is True:
                        entered.append(guess)
                        # get result of comparison to answer
                        test = logic.test(guess, answer)
                        # update win
                        for x in range(logic.NUMLETTERS):
                            mat[len(entered)-1][x].config(bg=COLOURS[test[x]])
                        # check for loss
                        if logic.loss(entered, answer):
                            over = True
                            messagebox.showinfo("Uh-oh!", "The alarm went off! You were caught!")
                            win.destroy()
                        # check for win
                        elif logic.win(test):
                            over = True
                            messagebox.showinfo("Congratulations!", "You entered the correct word!", parent=win)
                            # go to next room if there are more
                            if room < 9:
                                # button to advance
                                button = Button(win,
                                    text=f"Unlock room {room+1}",
                                    bg=COLOURS["bg"],
                                    fg=COLOURS["text"],
                                    font=("Bahnschrift", 12),
                                    command=lambda: [win.destroy(), newgame()]
                                )
                                button.grid()
                            # unlock vault if all codes solved
                            else:
                                button = Button(win,
                                    text=f"Unlock vault",
                                    bg=COLOURS["bg"],
                                    fg=COLOURS["text"],
                                    font=("Bahnschrift", 12),
                                    command=lambda: [win.destroy(), prize()]
                                )
                                button.grid()
                        guess = []
                    else:
                        messagebox.showerror("Error", "Invalid word")
                # delete letter
                elif event.keysym == "BackSpace" and len(guess) > 0:
                    logic.delete(guess)
                    # update win
                    mat[len(entered)][len(guess)].config(text="")
        
        # add menubar
        menubar = Menu(win)
        game_menu = Menu(menubar, tearoff=False)
        # game_menu.add_command(label="Intro", command=intro)
        game_menu.add_command(label="Help", command=help)
        menubar.add_cascade(label="Game", menu=game_menu)
        win.config(menu=menubar)
        
        # bind all keyboard events to keypress function
        win.bind("<Key>", keypress)

        # display window
        win.mainloop()

    # display intro
    # intro()

    # display first puzzle window
    newgame()

# run program
main()
