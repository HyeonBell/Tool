"""
    # Made by hyeonbell
    # 2021. 05. 03
    # version 0.2
    # purpose : Trace whole argument of java instance with infomation made by hooking code that causing exception call stack trace infomation

"""

import frida, sys
import asyncio
import re
import copy

global status_program
global is_running
global g_count

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
        self.menu = "\n1. Setup\n"\
                    "2. Show data\n"\
                    "3. Setup to script\n"\
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
        self.exception_data_list = list()
        self.temp_class_exception_data = None
        self.temp_run_check_g_count = 0
        self.max_payload = 0
        self.selected_exception = None
        self.selected_exception_list = list()


    class ClassExceptionData:
        def __init__(self):
            program_log("v", "Create ClassExceptionData Object")
            self.arg_dict = dict()
            self.except_dict = dict()

        def __del__(self):
            program_log("v", "Deallocate ClassExceptionData Object")

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

    # Check the Send word to synchronize the send method number and the payload value number.
    def check_send(self):
        self.max_payload = len(re.findall("send\(.*\);",self.jscode))

    def check_exception_run_count(self):
        global g_count
        if self.max_payload == self.temp_run_check_g_count:
            g_count = g_count + 1
            self.temp_run_check_g_count = 0

    def monitor_exception(self, *args, **kwargs):
        if 'payload' in args[0]:
            self.temp_run_check_g_count = self.temp_run_check_g_count + 1
            if re.match("^argument : .*\#sig_argend", args[0]['payload']):
                self.temp_class_exception_data.arg_dict[g_count] = args[0]['payload']
            if re.match("^java\.lang\.Exception([.\s].*)*\#sig_exceptend$", args[0]['payload']):
                self.temp_class_exception_data.except_dict[g_count] = args[0]['payload']
        self.check_exception_run_count()

    def monitor_exception_trace(self, *args, **kwargs):
        print(args)

    def template_check_object_jscode(self):
        jscode = """
            function check_object(check){
                if (check == "[object Arguements]"){
                console.log("type!! : " + typeof check + ", " + check.$className);
                }
            }"""
        return jscode

    def template_jscode(self):
        def closer_template_jscode(parse_info, count):
            dot = list(filter(lambda x: parse_info[x] == ".", range(len(parse_info))))
            dot.reverse()
            class_name = parse_info[:dot[0]]
            method_name = parse_info[dot[0]:]
            jscode = """
                var target"""+count+""" = Java.use(\"""" + class_name + """\");
                var overloadCount"""+count+""" = target"""+count+"""[\""""+method_name[1:]+"""\"].overloads.length;
                
                for (var i=0; i < overloadCount"""+count+"""; i++) {
                    target"""+count+"""[\""""+method_name[1:]+"""\"].overloads[i].implementation = function() {
                    
                    var ret_val = this[\""""+method_name[1:]+"""\"].apply(this, arguments);
                    send(\""""+parse_info+""" arguments : \" + arguments);
                    check_object(arguments);
                    send(\""""+parse_info+""" ret : \"+ ret_val);
                    check_object(ret_val);

                    return ret_val;    
                    }
                } 
            """
            return jscode
        return closer_template_jscode

    def create_tracing_exception_args_jscode(self):
        if len(self.selected_exception_list) == 0:
            program_log("v", "Error - No Exception Infomation")
            return 0
        self.jscode = self.template_check_object_jscode()
        self.jscode += "Java.perform(function() { "
        template_jscode = self.template_jscode()

        for i in range(0, len(self.selected_exception_list)):
            self.jscode += template_jscode(self.selected_exception_list[i], str(i))
        self.jscode += "});"
        program_log("v", "Finished create tracing exception args code")
        program_log("v", "Setup to script from jscode")
        try:
            self.script = self.session.create_script(self.jscode)
            program_log("v", "Finished Setup to script")
        except frida.InvalidOperationError as e:
            program_log("e", "ERROR - Retry after Session Created.")

    def parse_selected_exception_data(self):
        self.selected_exception_list = []
        found = re.findall("at .*", self.selected_exception)
        for i in range(0, len(found)):
            temp = found[i][3:found[i].find("(")]
            if "<init>" in temp:
                self.selected_exception_list.append(temp[:temp.find("<init>")]+"$init")
            else:
                self.selected_exception_list.append(temp)

    def setup_selected_exception_data(self, selected):
        print(self.exception_data_list[selected])
        while (1):
            print("1. Show argument")
            print("2. Exit")
            choice = input(" > ")
            if choice == "1":
                for k in self.exception_data_list[selected].arg_dict.keys():
                    print(str(k+1) + ". " + str(self.exception_data_list[selected].arg_dict[k]))
                w = int(input("Which one choices?\n > ")) - 1
                if w >= 0 and w <= len(self.exception_data_list[selected].arg_dict):
                    print(self.exception_data_list[selected].except_dict[w])
                    d = input("Are you going to choose this one?(Y/n)")
                    if d.lower() == "y" or d.lower() == "":
                        self.selected_exception = self.exception_data_list[selected].except_dict[w]
                        program_log("a", "Finished setup to data that have to trace.")
                    else:
                        break
                else:
                    program_log("e", "ERROR - Selected value is not correct")
            elif choice == "2":
                break
            else:
                program_log("e", "ERROR - Selected value is not correct")

        self.parse_selected_exception_data()

    def setup_exception_data(self):
        if len(self.exception_data_list) != 0:
            for i in range(0, len(self.exception_data_list)):
                print(str(i+1) + ". " + str(self.exception_data_list[i]))
            selected = int(input(" > ")) - 1
            if selected <= len(self.exception_data_list) and selected >= 0:
                self.setup_selected_exception_data(int(selected))
            else:
                program_log("e", "Error - selected scope is not correct.")
        else:
            program_log("a", "No setup exception data")

    def submenu_setup_frida(self):
        print("1. Setup to target")
        print("2. Setup to data that have to trace in exception result")
        selected = input(" > ")
        if selected == "1":
            self.setup_frida()
        elif selected == "2":
            self.setup_exception_data()
        else:
            program_log("a", "No selectable number.")

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

    def submenu_show_data(self):
        print("1. Show current JS code")
        print("2. Show exception data")
        selected = input(" > ")
        if selected == "1":
            self.show_script()
        elif selected == "2":
            self.show_exception_data()
        else:
            program_log("a", "No selectable number.")

    def show_script(self):
        if self.script is None:
            program_log("a", "didn't setup script yet.")
        else:
            program_log("v", "Showing script : " + str(self.script))
            print(self.jscode)

    def show_selected_exception(self, selected):
        print(self.exception_data_list[selected])
        while (1):
            print("1. Show argument")
            print("2. Exit")
            choice = input(" > ")
            if choice == "1":
                for k in self.exception_data_list[selected].arg_dict.keys():
                    print(str(k+1) + ". " + str(self.exception_data_list[selected].arg_dict[k]))
                w = int(input("Which one choices?\n > ")) - 1
                if w >= 0 and w <= len(self.exception_data_list[selected].arg_dict):
                    print(self.exception_data_list[selected].except_dict[w])
                else:
                    program_log("e", "ERROR - Selected value is not correct")
            elif choice == "2":
                break
            else:
                program_log("e", "ERROR - Selected value is not correct")

    def show_exception_data(self):
        if len(self.exception_data_list) != 0:
            for i in range(0, len(self.exception_data_list)):
                print(str(i+1) + ". " + str(self.exception_data_list[i]))
            selected = int(input(" > ")) - 1
            if selected <= len(self.exception_data_list) and selected >= 0:
                self.show_selected_exception(int(selected))
            else:
                program_log("e", "Error - selected scope is not correct.")
        else:
            program_log("a", "No setup exception data")

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
        output_argument = "+ " + self.argument.replace(", ", " + \", \" + ") + " + \" #sig_argend\""
        self.jscode = """
            // Trace Exception 
            Java.perform(function() {
                var target = Java.use(\"""" + self.class_name + """\");
                var imp = target""" + self.method_name + self.parameter + """;

                imp.implementation = function("""+self.argument+"""){
                    console.log(\"""" + self.class_name + """ hooked!\");
                    send(\"argument : \" """ + output_argument + """);
                    send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()) + "#sig_exceptend");
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
                program_log("v", "Setup to error overloading script.")
                self.setup_err_js_code()
                self.number_script = 1
            elif temp == "2":
                program_log("v", "Setup to exception trace create code.")
                self.setup_exception_trace_code()
                self.number_script = 2
            elif temp == "3":
                program_log("v", "Setup to exception trace code")
                self.create_tracing_exception_args_jscode()
                self.number_script = 3
            else:
                print("No numbering of script ")
        else:
            program_log("a", "Please setup class name and method name at '1. Setup > 1. Setup to target'")

    async def run_script(self):
        global is_running
        global g_count
        is_running = 0
        g_count = 0

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
                        self.check_send()
                        self.temp_class_exception_data = ClassFrida.ClassExceptionData()
                        parent.script.on("message", parent.monitor_exception)
                    elif self.number_script == 3:
                        parent.script.on("message", parent.monitor_exception_trace)
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

                # 모니터링 종료시 temp 데이터 객체 저장 후 free
                if self.number_script == 2:
                    temp_copy = copy.deepcopy(self.temp_class_exception_data)
                    self.exception_data_list.append(temp_copy)
                    del self.temp_class_exception_data

            else:
                program_log("a", "Please setup script at '3. Setup to script'")
        else:
            program_log("a", "Please setup class name and method name at '1. Setup > 1. Setup to target'")


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
            cfrida.submenu_setup_frida()
        elif choice_return == 2:
            cfrida.submenu_show_data()
        elif choice_return == 3:
            cfrida.select_script()
        elif choice_return == 4:
            try:
                asyncio.run(cfrida.run_script())
            except frida.InvalidOperationError as e:
                program_log("e", " Please setup target or setup script")
        elif choice_return == 5:
            print(cfrida.exception_data_list[0].arg_dict)
            print(cfrida.exception_data_list[0].except_dict)
        elif choice_return == 6:
            break
        else:
            continue
