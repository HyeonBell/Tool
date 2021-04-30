"""
    # Made by hyeonbell
    # 2021. 04. 30
    # version 0.1
    # purpose : Trace whole argument of java instance with infomation made by hooking code that causing exception call stack trace infomation

"""

import frida, sys
import asyncio

global status_program
global is_running

def flush():
    sys.stdin.flush()
    sys.stdout.flush()


class Menu:
    def __init__(self):
        program_log("v", "Create Menu Object")
        self.choice = None
        self.banner = "-------------------------------------------------\n" \
                 "\tTrace exception argument in runtime \n" \
                 "-------------------------------------------------"
        self.menu = "\n1. Setup target\n"\
                    "2. Show current JS code\n"\
                    "3. Setup script\n"\
                    "4. Run script\n"\
                    "5. Overloading Calculate\n"\
                    "6. Exit\n"\

    def __del__(self):
        program_log("v", "Deallocate Menu Object")

    @staticmethod
    def show_status():
        global status_program
        if status_program:
            program_log("v", "Status : " + status_program)
        else:
            print("")

    def show_menu(self):
        print(self.banner)
        Menu.show_status()
        print(self.menu)
        self.choice = input("\n> ")

    def choice_check(self):
        if self.choice == "1":
            return 1
        elif self.choice == "2":
            return 2
        elif self.choice == "3":
            return 3
        elif self.choice == "4":
            return 4
        elif self.choice == "5":
            return 5
        elif self.choice == "6":
            return 6
        else:
            program_log("a", "Please retry with normally input value that scope of menu number")


class ClassFrida:
    def __init__(self):
        program_log("v", "Create Frida Object")
        self.PACKAGE_NAME = None
        self.class_name = None
        self.method_name = None
        self.device = None
        self.pid = None
        self.session = None
        self.script = None
        self.runcount = 0
        self.runtime_info = None
        self.jscode = None
        self.number_script = None
        self.parameter = None
        self.argument = ""
        self.error_overloading = ".overload('erRorError', 'erRorError')"
        self.is_init = 0
        self.script_list = ['Cause error overloading', 'Trace exception', 'Trace argument of exception']

    def __del__(self):
        program_log("v", "Deallocate Frida Object")

    def parse_from_parameter(self):
        count = self.parameter.count(',')
        for c in range(0, count):
            self.argument += "param" + str(c+1) + ", "
        self.argument = self.argument[:-2]


    def monitor_error(self, *args, **kwargs):
        global is_running
        program_log("v", "Select Overloading")

        temp = list(args[0]['description'].split("\n\t"))
        for i in range(1, len(temp)):
            print(str(i) + ". " + temp[i])
        flush()
        selected = input("> ")
        self.parameter = str(temp[int(selected)])
        print(self.parameter)
        self.parse_from_parameter()
        is_running = 0

    def monitor_exception(self, *args, **kwargs):
        global is_running

        #is_running = 0

    def setup_frida(self):
        global status_program
        program_log("i", "Put Application Info")
        self.PACKAGE_NAME = input("PACKAGE_NAME > ")
        self.class_name = input("Class Name > ")
        self.setup_is_init()
        if self.is_init == 0:
            self.method_name = input("Method Name > ")
            self.method_name = "['" + self.method_name+"']"
        else:
            self.method_name = ".$init"

        # test code
        self.PACKAGE_NAME = "viva.republica.toss"
        self.class_name = "o.afc"
        self.method_name = ".$init"

        try:
            program_log("v", "Try to connect device with USB connection")
            self.device = frida.get_usb_device(1)
            program_log("v", "Try to spawn app with process id.")
            self.pid = self.device.spawn([self.PACKAGE_NAME])
            program_log("v", "Try to attach process for creating session.")
            self.session = frida.get_usb_device(1).attach(self.pid)
            program_log("v", "Finished setup ")
            program_log("i", "Target Waiting for %resume.")
        except Exception as e:
            program_log("e", "Failed setup" + str(e.with_traceback()))

        if self.session:
            status_program = "SESSION : " + str(self.session)
            status_program += ", TARGET : " + str(self.PACKAGE_NAME)

    def setup_is_init(self):
        answer = input("Is method init constructor?(Y/n)")
        if answer.lower() == "y":
            program_log("i", "Targeting Init")
            self.is_init = 1
        elif answer.lower() == "n":
            program_log("i", "Targeting function")
            self.is_init = 0
        else:
            program_log("i", "Targeting Init")
            self.is_init = 1

    def show_script(self):
        if self.script is None:
            program_log("a", "didn't setup script yet.")
        else:
            program_log("v", "Showing script : " + str(self.script))
            print(self.jscode)

    def check_setup_target(self):
        if self.class_name is not None and self.method_name is not None and self.PACKAGE_NAME is not None:
            return True
        else:
            return False

    def check_setup_script(self):
        if self.script is not None and self.jscode is not None:
            return True
        else:
            return False

    def error_wrapper_setup_jscode(self):
        try:
            self.script = self.session.create_script(self.jscode)
        except Exception as e:
            program_log("e", "ERROR " + str(e.with_traceback()))
        finally:
            print("")

    def setup_err_js_code(self):
        self.jscode = """
            // For obtaining parameter of target, setup error parameter. 
            Java.perform(function() {
                var target = Java.use(\"""" + self.class_name + """\");
                var imp = target""" + self.method_name + self.error_overloading + """;

                imp.implementation = function(){
                    console.log(\"""" + self.class_name + """ hooked!\");
                    return target""" + self.method_name + """.call(this);
                }
            })
        """
        self.error_wrapper_setup_jscode()

    def setup_exception_trace_code(self):
        output_argument = "+ " + self.argument.replace(", ", " + \", \" + ")
        self.jscode = """
            // Trace Exception 
            Java.perform(function() {
                var target = Java.use(\"""" + self.class_name + """\");
                var imp = target""" + self.method_name + self.parameter + """;

                imp.implementation = function("""+self.argument+"""){
                    console.log(\"""" + self.class_name + """ hooked!\");
                    console.log(\"argument : \" """ + output_argument + """);
                    console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
                    return target""" + self.method_name + """.call(this, """+self.argument+""");
                }
            })
        
        """
        self.error_wrapper_setup_jscode()

    def select_script(self):
        if self.check_setup_target():
            for l in range(0,self.script_list.__len__()):
                print(str(l+1) + ". " + self.script_list[l])
            temp = input("> ")
            if temp == "1":
                program_log("v", "Setup error overloading script.")
                self.setup_err_js_code()
                self.number_script = 1
            elif temp == "2":
                self.setup_exception_trace_code()
                self.number_script = 2
            elif temp == "3":
                self.number_script = 3
                print("")
            else:
                print("No numbering of script ")
        else:
            program_log("a", "Please setup class name and method name at '1. Setup target'")

    async def run_script(self):
        global is_running
        is_running = 0

        if self.check_setup_target():
            if self.check_setup_script():
                async def wait_task(parent):
                    global status_program
                    global is_running
                    is_running = 1

                    program_log("v", "Upload monitor of script")
                    if self.number_script == 1:
                        parent.script.on("message", parent.monitor_error)
                    elif self.number_script == 2:
                        parent.script.on("message", parent.monitor_exception)
                    else:
                        # TODO :!!!
                        print("TEST!")

                    program_log("v", "Load script")
                    parent.script.load()
                    program_log("v", "Resume application.")
                    parent.device.resume(self.pid)
                    while is_running == 1:
                        if self.number_script != 1:
                            value = input("To exit, typing 'exit'\n > ")
                            if value == "exit":
                                break
                    status_program = None

                task = asyncio.create_task(wait_task(self))
                await task

            else:
                program_log("a", "Please setup script at '3. Setup target'")
        else:
            program_log("a", "Please setup class name and method name at '1. Setup target'")


def program_log(type, data):
    if type == "i" :
        print("[INFO] " + data)
    elif type == "a":
        print("[ALERT] " + data)
    elif type == "v":
        print("[*] " + data)
    elif type == "e":
        print("[ERROR]" + data)
    else:
        return


if __name__ == "__main__":
    program_log("v", "Loading Program")
    status_program = None
    menu = Menu()
    cfrida = ClassFrida()

    program_log("v", "Show up Menu")
    while (1):
        menu.show_menu()
        choice_return = menu.choice_check()
        if choice_return == 1:
            cfrida.setup_frida()
        elif choice_return == 2:
            cfrida.show_script()
        elif choice_return == 3:
            cfrida.select_script()
        elif choice_return == 4:
            try:
                asyncio.run(cfrida.run_script())
            except frida.InvalidOperationError as e:
                program_log("e", " Please setup target or setup script")
        elif choice_return == 5:
            continue
        elif choice_return == 6:
            break
        else:
            continue
