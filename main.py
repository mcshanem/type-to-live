from tkinter import *
from tkinter import ttk
import tkinter.font as tk_font

WINDOW_TITLE = 'Type to Live'
WINDOW_DIMENSIONS = '1000x550'
START_TEXT = "Click here to begin typing. Don't stop!"
SUCCESS_TEXT = ('\n\n\n******************************\n\n\n🎉\nYou completed a session.\nWell done!\nCopy/paste to '
                'save your work.')
TIMEOUT_SECONDS = 5
SESSION_MINUTES = 5
ONE_SECOND = 1000


def clear(event):
    current_state = text.cget('state')
    text.config(state='normal')
    text.delete('1.0', END)
    text.config(state=current_state)


def reset_session():
    global timeout_timer, session_timer
    # Reset timers
    timeout_timer = ''
    session_timer = ''

    # Disable reset button
    reset_button.config(state='disabled')

    # Reset text entry box
    text.config(state='normal', foreground='black')
    clear(None)
    text.insert(index='1.0', chars="Click here to begin typing. Don't stop!")

    # Reset the countdown labels
    session_count_down_label.config(text='Session\n5 min')
    timeout_count_down_label.config(text='💀')

    # Reset the bindings
    text.bind('<FocusIn>', clear)
    text.bind('<KeyRelease>', start_timers)


def reset_timeout_timer():
    if timeout_timer:
        root.after_cancel(timeout_timer)


def start_timers(event):
    # Start Session timer if it's not started already
    if session_timer == '':
        run_session_timer(SESSION_MINUTES * 60)

    # Start or restart Timeout timer
    reset_timeout_timer()
    run_timeout_timer(TIMEOUT_SECONDS)


def run_timeout_timer(sec):
    global timeout_timer
    timeout_count_down_label.config(text=f'💀\n{sec}')
    if sec > 0:
        timeout_timer = root.after(ONE_SECOND, run_timeout_timer, sec-1)
    else:
        # Disable the session timer
        root.after_cancel(session_timer)

        # Lock the text box and turn text red
        text.config(foreground='red', state='disabled')
        text.unbind('<KeyRelease>')
        text.unbind('<FocusIn>')

        # Update the timeout countdown label
        timeout_count_down_label.config(text=f'💀\nYou died...')

        # Activate the reset button
        reset_button.config(state='normal')

        # Clear the text box after a second
        root.after(ONE_SECOND, clear, None)


def run_session_timer(sec):
    global session_timer
    session_count_down_label.config(text=f'Session\n{sec}')
    if sec > 0:
        session_timer = root.after(ONE_SECOND, run_session_timer, sec-1)
    else:
        # Disable the timeout timer
        root.after_cancel(timeout_timer)

        # Update the timeout countdown label to the success text
        text.insert(index=END, chars=SUCCESS_TEXT)
        text.see(END)

        # Lock the text box
        text.config(state='disabled')
        text.unbind('<KeyRelease>')
        text.unbind('<FocusIn>')

        # Activate the reset button
        reset_button.config(state='normal')


# Create the root window and main frame
root = Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_DIMENSIONS)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Configure style and font
default_font = tk_font.nametofont('TkDefaultFont')
default_font.configure(size=16)

main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0, sticky=NSEW)
main_frame.columnconfigure((0, 2), weight=1, uniform='main')
main_frame.columnconfigure(1, weight=5, uniform='main')
main_frame.rowconfigure(0, weight=1)

# Create console frame
console_frame = ttk.Frame(main_frame)
console_frame.grid(column=0, row=0, sticky=NSEW)
console_frame.columnconfigure(0, weight=1)
console_frame.rowconfigure((0, 1, 2), weight=1)

# Create countdown labels
timeout_count_down_label = ttk.Label(console_frame, justify='center')
timeout_count_down_label.grid(column=0, row=0)

session_count_down_label = ttk.Label(console_frame, justify='center')
session_count_down_label.grid(column=0, row=1)

# Create reset button
reset_button = ttk.Button(console_frame, text='Reset', command=reset_session)
reset_button.grid(column=0, row=2)

# Create writing text box
text = Text(main_frame,
            width=1,
            height=1,
            font=default_font,
            wrap='word')
text.grid(column=1, row=0, sticky=NSEW)

# Initialize the timers
timeout_timer = ''
session_timer = ''

reset_session()

root.mainloop()
