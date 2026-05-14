import curses

filename = "untitled.txt"

status_message = ""

def _editor(stdscr):
    global filename, status_message

    curses.start_color()
    curses.use_default_colors()

    curses.curs_set(1)

    try:
        with open(filename, "r") as f:
            lines = f.readlines()

    except FileNotFoundError:
        lines = [""]

    y = 0
    x = 0

    while True:

        stdscr.clear()

        # draw text
        for i, line in enumerate(lines):
            stdscr.addstr(i, 0, line.rstrip(), curses.A_NORMAL)

        # status bar
        h, w = stdscr.getmaxyx()

        status = f"MPython Nano | {filename} | ~ Save | ESC Quit"

        if status_message:
            status += f" | {status_message}"

        stdscr.addstr(
            h - 1,
            0,
            status[:w-1]
        )

        stdscr.move(y, x)

        if status_message == "Saved!":
            stdscr.refresh()
            curses.napms(1000)
            status_message = ""
        key = stdscr.getch()

        # quit
        if key == 27:  # Ctrl+Q
            break

        # save
        elif key == ord("~"):

            save_name = filename
            saving = True

            while saving:

                stdscr.clear()

                # draw editor text
                for i, line in enumerate(lines):
                    stdscr.addstr(i, 0, line.rstrip())

                h, w = stdscr.getmaxyx()

                # save ui
                save_bar = (
                    f"Save as: {save_name}"
                    " | ENTER Save | ESC Cancel"
                )

                stdscr.addstr(
                    h - 1,
                    0,
                    save_bar[:w-1]
                )

                stdscr.move(h - 1, len("Save as: ") + len(save_name))

                stdscr.refresh()

                k = stdscr.getch()

                # ENTER
                if k == 10:

                    filename = save_name

                    with open(filename, "w") as f:
                        f.write("\n".join(lines))

                    status_message = "Saved!"

                    saving = False

                # ESC
                elif k == 27:

                    saving = False

                # backspace
                elif k in (8, 127, curses.KEY_BACKSPACE):

                    save_name = save_name[:-1]

                # normal typing only
                elif 32 <= k <= 126:

                    save_name += chr(k)
        # enter
        elif key == 10:

            current = lines[y]

            lines.insert(y + 1, current[x:])

            lines[y] = current[:x]

            y += 1
            x = 0

        # backspace
        elif key in (8, 127, curses.KEY_BACKSPACE):

            if x > 0:

                lines[y] = (
                    lines[y][:x-1] +
                    lines[y][x:]
                )

                x -= 1

        elif key == curses.KEY_UP:
            y = max(0, y - 1)

        elif key == curses.KEY_DOWN:
            y = min(len(lines)-1, y + 1)

        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)

        elif key == curses.KEY_RIGHT:
            x = min(len(lines[y]), x + 1)

        # normal typing
        elif 32 <= key <= 126:

            lines[y] = (
                lines[y][:x] +
                chr(key) +
                lines[y][x:]
            )

            x += 1

def editor(file_name="untitled.txt"):

    global filename

    filename = file_name

    curses.wrapper(_editor)