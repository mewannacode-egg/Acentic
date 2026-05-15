from MCommands import *
# Its sooooooo readable now!!

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
