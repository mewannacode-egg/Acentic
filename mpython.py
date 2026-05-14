from os import system
import readline #to move with arrows
import difflib
import builtins
import json
from MEdit import editor #NEWWW UI
system("clear")

# Defined Variables

available_cmds = {}

env = {} # Command history so you can type "a = 1", then "print(a)"
env["__builtins__"] = builtins
history = []

settings = {
    "feedback": True,
    "jokes": False,
    "help": True,

    "badge-colour": "\033[92m",
    "input-colour": "\033[0m",
    "badge": "[Python]",

    "prefix": "!"
}

try:
    with open("configs.json", "r") as f:
        saved_settings = json.load(f)

    settings.update(saved_settings)

except FileNotFoundError:
    pass

def save_configs():
    with open("configs.json", "w") as f:
        json.dump(settings, f, indent=4)

badge = settings["badge-colour"]+settings["badge"]+settings["input-colour"]
#Helpers
def sync_badge():
    global badge
    badge = settings["badge-colour"]+settings["badge"]+settings["input-colour"]

import re

def highlight(line):
    # ANSI escape codes
    RESET = "\033[0m"
    GREENWHITE = "\033[92m" 
    PURPLE = "\033[95m"
    PINK = "\033[38;5;213m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"

    patterns = {
        "string": r'(\".*?\"|\'.*?\')',
        "keyword": r'\b(while|if|import|from)\b',
        "bool_op": r'\b(True|False|is|in)\b',
        "function": r'\b([a-zA-Z_][a-zA-Z0-9_]*)(?=\()',
        "number": r'\b(\d+)\b',
        "bracket": r'([\(\)\[\]\{\}])',
    }

    master_regex = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in patterns.items()))

    def replace_match(match):
        if match.group("string"): return f"{YELLOW}{match.group(0)}{RESET}"
        if match.group("keyword"): return f"{PINK}{match.group(0)}{RESET}"
        if match.group("bool_op"): return f"{BLUE}{match.group(0)}{RESET}"
        if match.group("function"): return f"{PURPLE}{match.group(0)}{RESET}"
        if match.group("number"): return f"{GREENWHITE}{match.group(0)}{RESET}"
        if match.group("bracket"): return f"{YELLOW}{match.group(0)}{RESET}"
        return match.group(0)

    return master_regex.sub(replace_match, line)

def completer(text, state):  #Tab auto completion!!! finally!!!
    options = []

    # commands
    for cmd in available_cmds:
        full = settings["prefix"] + cmd

        if full.startswith(text):
            options.append(full)

    # variables/functions/imports
    for name in env.keys():

        if name.startswith(text):
            options.append(name)

    # builtins
    for name in dir(builtins):

        if name.startswith(text):
            options.append(name)

    if state < len(options):
        return options[state]

    return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


# Functions
def perror(type, error_or_text): #print pretty errors!
    if settings["feedback"]:
        print(f"\033[91m-> [Error] \033[93m{type} | \033[0m{error_or_text}")

def pfeedback(badge, feedback, col="\033[96m"):
    if settings["feedback"]:
        print(f"{col}-> [{badge}] \033[0m{feedback}")

#Helper functions to make commands
def command(name): #decorator to make my life easier | register commands
    def wrapper(func):
        available_cmds[name] = func
        return func
    return wrapper

def handle_command(cmd):
    cmd = cmd[len(settings["prefix"]):].strip()
    parts = cmd.split()

    if not parts:
        return

    name = parts[0]
    args = parts[1:]

    func = available_cmds.get(name)

    if func:
        func(args)
    else:
        if settings["help"]:

            suggestion = difflib.get_close_matches(
                name,
                available_cmds.keys(),
                n=1
            )

            if suggestion:
                perror(
                    "Unknown Command",
                    f"Did you mean '{suggestion[0]}'?"
                )
                return

        perror(
            "Unknown Command",
            f"'{name}' does not exist"
        )

# REAL COCMMANDS!!
@command("clear")
def cmd_clear_terminal(args):
    system("clear")
    if settings["jokes"]:
        pfeedback("Feedback", "Terminal has been cleared (You dirty freak!)")
    else:
        pfeedback("Feedback", "Terminal has been cleared")

@command("medit")
def cmd_medit(args):

    env_file = "__env__.py"

    # EDIT ENV MODE
    if args and args[0] == "--env":

        # write current history snapshot
        with open(env_file, "w") as f:
            for line in history:
                f.write(line + "\n")

        # open editor
        editor(env_file)

        # ask reload after edit
        choice = input("\n[Reload] Apply edited env? (y/n): ").lower()

        if choice == "y":

            # reset runtime
            history.clear()
            env.clear()
            env["__builtins__"] = builtins

            # reload from edited file
            with open(env_file, "r") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()

                if not line:
                    continue

                history.append(line)

                try:
                    exec(line, env)
                except Exception as e:
                    perror("ReloadError", f"{line} -> {e}")

            pfeedback("Medit", "Env reloaded from editor")

        elif args:
            editor(args[0])

        else:
            editor()

        return

@command("config")
def cmd_config(args):
    save_configs()
    if len(args) < 2:
        perror(
            "Invalid Usage",
            "Usage: !config <setting> <value>"
        )
        return

    setting = args[0]

    if setting not in settings:
        perror(
            "Unknown Setting",
            f"Setting does not exist: {setting}"
        )
        return

    value = " ".join(args[1:])

    true_vals = ("true", "on", "yes", "fat") #shhs
    false_vals = ("false", "off", "no", "skinny")

    #boolean settings
    if isinstance(settings[setting], bool):

        val = value.lower()

        if val in true_vals:
            settings[setting] = True

        elif val in false_vals:
            settings[setting] = False

        else:
            if settings["jokes"]:
                perror(
                    "Invalid Value",
                    "Use true/false | on/off | yes/no | fat/skinny"
                )
            else:
                perror(
                    "Invalid Value",
                    "Use true/false | on/off | yes/no"
                )
            return

    # badge
    else:

        colours = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "cyan": "\033[96m",
            "reset": "\033[0m"
        }

        # automatic colour conversion
        if setting.endswith("colour"):
            value = colours.get(value.lower(), value)

        settings[setting] = value

    sync_badge()

    pfeedback(
        "Feedback",
        f"'{setting}' has been updated to '{value}'"
    )

@command("undo")
def cmd_undo(args):

    if not history:
        perror("UndoError", "Nothing to undo")
        return

    history.pop()

    env.clear()
    env["__builtins__"] = builtins

    for line in history:
        try:
            exec(line, env)
        except:
            pass

    if settings["jokes"]:
        pfeedback("Feedback", "Last line of enviorment is GONE!!")
    else:
        pfeedback("Feedback", "Last line of enviorment has been deleted")

@command("save")
def cmd_save(args):

    if not args:
        perror(
            "Invalid Usage",
            "Usage: !save <file>"
        )
        return

    filename = args[0]

    confirm = input(
        f"\033[91m-> [Confirmation] \033[0mSave env as '{filename}'? (y/n): "
    ).lower()

    if confirm != "y":
        pfeedback("Feedback", "Save canceled")
        return

    try:

        with open(filename, "w") as f:

            for line in history:
                f.write(line + "\n")

        pfeedback(
            "Feedback",
            f"Saved env to '{filename}'"
        )

    except Exception as e:
        perror("SaveError", str(e))

@command("load")
def cmd_load(args):

    if not args:
        perror(
            "Invalid Usage",
            "Try: !load <file>"
        )
        return

    filename = args[0]

    confirm = input(
        f"\033[91m-> [Confirmation] \033[0mLoad '{filename}'? This action will \033[91mreplace \033[0myour \033[91mentire \033[0menv (y/n): "
    ).lower()

    if confirm != "y":
        pfeedback("Feedback", "Load canceled")
        return

    try:

        with open(filename, "r") as f:
            lines = f.readlines()

        history.clear()

        env.clear()
        env["__builtins__"] = builtins

        for line in lines:

            line = line.strip()

            if not line:
                continue

            history.append(line)

            try:
                exec(line, env)

            except Exception as e:
                perror(
                    "LoadError",
                    f"{line} -> {e}"
                )

        pfeedback(
            "Feedback",
            f"Loaded '{filename}'"
        )

    except FileNotFoundError:
        perror(
            "LoadError",
            f"File not found: {filename}"
        )

@command("reset")
def cmd_reset(args):

    env.clear()
    env["__builtins__"] = builtins

    history.clear()

    pfeedback(
        "Feedback",
        "Environment and history cleared"
    )

@command("env")
def cmd_env(args):

    if not history:
        pfeedback("Feedback", "Nothing stored")
        return

    count = 1

    CYAN = "\033[96m"
    RESET = "\033[0m"

    for line in history:

        print(
            f"{CYAN}[{count}]{RESET} "
            f"{highlight(line)}"
        )

        count += 1

@command("rerun")
def cmd_rerun(args):

    for line in history:

        try:
            exec(line, env)

        except Exception as e:
            perror(
                "RerunError",
                f"{line} -> {e}"
            )


    if settings["jokes"]:
        pfeedback("Feedback", "Reran env(i.e 9/11)")
    else:
        pfeedback("Feedback", "Reran env")

@command("about")
def cmd_version(args):  #tells you the everything about this Python REPL
    print("-----> About! <-----")
    print("- Name: MPython (Mini Python)")
    print("- Version: 0.02")
    print("- Language: Python (for now...)")
    print("-----> End... <-----")

@command("changelog")
def cmd_changelog(args):

    print("-----> Changelog <-----")

    print("[0.01]")
    print("- Basic REPL")
    print("- eval() + exec()")
    print("- Custom commands")

    print()

    print("[0.02]")
    print("- Config system(updated)")
    print("- Undo system")
    print("- !env(tells you the written code)")
    print("- Syntax highlighting(in env)")
    print("- Suggestions/help")
    print("- Tab-auto completion!!")
    print("- Save and Load commands!")
    print("- Auto-save config settings in configs.json")

    print()

    print("[0.03]")
    print("- New UI editor like nano(but better)")
    print("- !medit <file>")
    print("- Type !myenv --env to edit current env")

    print("-----> End... <-----")

def suggest_name(error):

    missing = error.name

    possible_names = list(env.keys()) + dir(builtins)

    suggestion = difflib.get_close_matches(
        missing,
        possible_names,
        n=1
    )

    if settings["help"] and suggestion:

        perror(
            "NameError",
            f"Did you mean '{suggestion[0]}'?"
        )

    else:
        perror("NameError", str(error))

def run(): #Take input > exeute > handle errors, a side-main
    try:
        cmd = input(badge + " ")

        if cmd.startswith(settings["prefix"]): #check for commands
            handle_command(cmd)
            return

        try:
            if "=" in cmd or cmd.startswith(("print", "def", "class", "import", "from")):
                history.append(cmd)
            result = eval(cmd, env)
            if result is not None:
                print(result)

        except SyntaxError:
            try:
                exec(cmd, env)
            except SyntaxError as e:
                perror("SyntaxError", str(e))
            except NameError as e:
                suggest_name(e)
            except ModuleNotFoundError as e:
                perror("ModuleNotFoundError", str(e))

        except NameError as e:
            suggest_name(e)

    except KeyboardInterrupt:
        print()
        perror("KeyboardInterrupt", "Type 'exit()' to quit instead")

#Main Loop
while True:
    run()