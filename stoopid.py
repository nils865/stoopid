import time, sys, os, subprocess
from sys import exit

# initialize some default variables
configPath = "%appdata%\\stoopid"
libs = {}
## list of all the default usable operators and comparators
operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "^": lambda x, y: x**y,
}
comparators = {
    "<<": lambda x, y: x < y,
    ">>": lambda x, y: x > y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
}
orderOfOps = [["+", "-"], ["*", "/"], ["%", "^"]]

## saves all used variables
vars = {}
arrs = {}
bools = {}
labels = {}

## line the interpreter is currently on
current_line = 0

# helper functions
def isnumber(string):
    """Test if given string is a number

    Args:
        string (string): input string

    Returns:
        boolean: if given string is number
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_float(number):
    """Test if given number is a float

    Args:
        number : number to test

    Returns:
        boolean: if number is a float
    """
    try:
        if float(number) == int(number):
            return False
        else:
            return True
    except ValueError:
        return False


def get_nonum(inp, lineNum):
    """Test if given input is not a number

    Args:
        inp : input string
        lineNum (int): current line

    Returns:
        string: input as not a number
    """
    global current_line
    if isnumber(inp):
        print(f"Error in line {lineNum + 1}: String expected, but got number: {inp}")
    return inp


def get_value(inp):
    """Gets current value of any variable

    Args:
        inp (string): variable name

    Returns:
        any: value of given variable
    """
    global vars, bools
    inp = str(inp).strip()

    if isnumber(inp):
        if is_float(inp):
            return float(inp)
        else:
            return int(inp)
    else:
        if inp in vars:
            return vars[inp]
        elif inp in bools:
            if bools[inp]:
                return 1
            elif bools[inp] == 0:
                return 0
        else:
            try:
                return solvemath(inp)
            except:
                return inp


def getline(line):
    """returns a list of all pieces in the line

    Args:
        line (string): the full line to be split

    Returns:
        string list: list of all pieces in a line
    """
    line.strip()
    if line == "" or line.startswith("'"):
        return ""
    line = line.split("#")[0]
    linepieces = line.split(":")
    for k in range(len(linepieces)):
        linepieces[k] = linepieces[k].strip()
    return linepieces


def search_array(string, array):
    """tests if an element in an array is in the string

    Args:
        string (string): string which should include something
        array (string array): list of values which the string could include

    Returns:
        string or int: value which is included in the string or -1
    """
    for k in range(len(array)):
        if array[k] in string:
            return array[k]
    return -1


def convertToBool(val):
    """Converts booleans as string to real booleans

    Args:
        val (string): Value to convert to boolean

    Returns:
        string or bool: the boolean which was given or if it isnt a boolean it just returns the value
    """
    if val == "True" or val == "False":
        return {"True": 1, "False": 0}[val]
    else:
        return val


def solvemath(equasion):
    try:
        global operators, vars, orderOfOps, current_line
        if "(" in equasion:
            for k in range(len(equasion)):
                if equasion[k] == "(":
                    start = k

                    break
            for k in range(len(equasion) - 1, 0, -1):
                if equasion[k] == ")":
                    stop = k

                    break
            tmpequasion = equasion[:start]
            tmpequasion += str(int(solvemath(equasion[start + 1 : stop])))
            tmpequasion += equasion[stop + 1 :]
            return solvemath(tmpequasion)
        equasion = str(equasion)
        for i in vars:
            equasion = equasion.replace(i, str(vars[i]))
        ops = []
        values = []

        x = 0
        while x < len(equasion):
            if isnumber(equasion[x]):
                if x > 0 and (
                    isnumber(equasion[x - 1])
                    or values[len(values) - 1][len(values[len(values) - 1]) - 1]
                    in ["-", "."]
                ):
                    values[len(values) - 1] += equasion[x]
                else:
                    values.append(str(equasion[x]))
            elif equasion[x] in [o for o in operators]:
                if (x == 0 and equasion[x] == "-") or (
                    x > 0 and not isnumber(equasion[x - 1])
                ):
                    values.append(equasion[x])
                else:
                    ops.append(str(equasion[x]))
            elif equasion[x] == ".":
                if x > 0 and isnumber(equasion[x - 1]):
                    values[len(values) - 1] += "."
                else:
                    values.append("0.")
            x += 1

        # print(str(ops) + "\n" + str(values))
        # now we have the values and the operators, find the order in which they should be solved
        order = []
        for i in range(len(ops)):
            for k in range(len(orderOfOps)):
                if ops[i] in orderOfOps[k]:
                    order.append(k)

        # print(order)

        # now we have the order in which the operators should be solved, we need to solve them
        minorder = max(order)
        for i in range(len(ops)):
            if order[i] == minorder:
                values[i] = float(
                    operators[ops[i]](float(values[i]), float(values[i + 1]))
                )
                values.pop(i + 1)
                ops.pop(i)

                order.pop(i)
                break
        # print(f"{values} uwu {ops} owo")
        # after we have solved the first operator, we need to solve the rest
        if len(ops) > 1:
            # recreate the equation
            equasion = ""
            for i in range(len(ops)):
                equasion += str(values[i]) + str((ops[i]))
            equasion += str(values[-1])
            # print(equasion)
            # print(equasion)
            # print("bigg recursion!")
            return getAsNumtype((solvemath(equasion)))

        elif len(ops) == 1:
            # print("sussywussy")
            return getAsNumtype(operators[ops[0]](float(values[0]), float(values[1])))
        else:
            return getAsNumtype(values[0])
    except Exception as e:
        raise e
        # print(f"Error in line {current_line + 1}: Math error, {e}")
        # print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        # exit()


def findNextBracket(string, start):
    """finds the next bracket in a string

    Args:
        string (string): string which should include something
        start (int): index of the bracket whose closing bracket is searched for

    Returns:
        int: index of the next bracket in the string
    """
    count = 1
    for i in range(start + 1, len(string)):
        if string[i] == "(":
            count += 1
        elif string[i] == ")":
            count -= 1
        if count == 0:
            return i

    for i in range(start, len(string)):

        if string[i] == "(":
            return i
    return -1


def boolSolv(pieces):
    """checks bools and resolves them

    Args:
        pieces (string array): Pieces of current lines

    Returns:
        boolean: returns the solved condition
    """
    global current_line, comparators
    try:
        # get clean linepieces
        for k in range(len(pieces)):
            pieces[k] = pieces[k].replace("{", "").replace("}", "").replace(" ", "")

        cons = 1
        results = []
        combs = []

        # get all conditions to solve
        for k in pieces:
            if k.startswith("or") or k.startswith("and"):
                cons += 1
                combs.append(k)

        # solve all single conditions
        for k in range(cons):
            mop = pieces[k * 2 + 0].replace("{", "").replace("}", "")

            comp = search_array(mop, [c for c in comparators])
            if comp == -1:
                if mop in vars:
                    mop = vars[mop]
                if mop in bools:
                    results.append(get_value(mop))
                elif mop.lower() == "true" or mop == "1":
                    results.append(1)
                elif mop.lower() == "false" or mop == "0":
                    results.append(0)
                else:
                    print(
                        f"Error in line {current_line + 1}: Invalid data type or comparitor not found: {mop}"
                    )
                    exit()
            else:
                var1 = get_value(mop.split(comp)[0])
                var2 = get_value(mop.split(comp)[1])

                var1 = convertToBool(var1)
                var2 = convertToBool(var2)

                results.append(comparators[comp](var1, var2))

        # solve the whole conditions
        res = results[0]
        for k in range(len(combs)):

            if combs[k].startswith("or"):
                if results[k + 1] or res != 0:
                    res = 1
                else:
                    res = 0
            if combs[k].startswith("and"):
                if res == 1 and results[k + 1] == 1:
                    res = 1
                else:
                    res = 0

        return res
    except Exception as e:
        print(f"Error in line {current_line + 1}: Boolean error, {e}")
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()


def getAsNumtype(num):
    try:
        if is_float(num):
            return float(num)
        else:
            return int(num)
    except:
        raise Exception("Invalid data type")


def getPath(path):
    """resolves the given path

    Args:
        path (string): path as string

    Returns:
        string: resolved path
    """
    try:
        pathlist = path.replace("%", "").split("\\")

        for p in range(len(pathlist)):
            if os.getenv(pathlist[p]) != None:
                pathlist[p] = os.getenv(pathlist[p])

        fetchedPath = os.path.join(pathlist[0])
        p = 1
        while p < len(pathlist):
            fetchedPath = os.path.join(fetchedPath, pathlist[p])
            p += 1
        subprocess.run(
            f"mkdir {fetchedPath}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )

        return fetchedPath
    except Exception as e:
        print(
            f"Interpreter Error: {e}\nCould not resolve Path {path}\nCrashed in line {e.__traceback__.tb_lineno}"
        )
        exit()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller

    Args:
        relative_path (string): relative path to the resource

    Returns:
        string: path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# keyword functions


def kwVar(pieces):
    """Adds a variable to the list of variables

    Args:
        pieces (String List): list of all pieces in the line
    """
    global vars, current_line

    vars[get_nonum(pieces[1], current_line).split("=")[0].strip()] = get_value(
        "".join((pieces[1]).split("=")[1:])
    )
    # print(vars)


def kwArr(pieces):
    """Adds an array to the list of arrays

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[get_nonum(pieces[1], current_line)] = [0 for i in range(int(pieces[2]))]


def kwApp(pieces):
    """Appends to an array

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[get_nonum(pieces[1], current_line)].append(float(get_value(pieces[2])))


def kwGetArr(pieces):
    """Gets the value of an item in an array at a specific index

    Args:
        pieces (String List): list of all pieces in the line
    """
    global vars, arrs
    vars[str(pieces[3])] = arrs[str(pieces[1])][get_value(pieces[2])]


def kwSetArr(pieces):
    """Sets the value of a specific item in an array

    Args:
        pieces (String List): list of all pieces in the line
    """
    global arrs
    arrs[str(pieces[1])][get_value(pieces[2])] = get_value(pieces[3])


def kwOut(pieces):
    """Prints the given input

    Args:
        pieces (String List): list of all pieces in the line
    """
    global bools, logging, log
    if pieces[1] in bools:
        out = ["False", "True"][int(bools[pieces[1]])]
    else:
        out = get_value(pieces[1])
    if not silent:
        print(out)
    if logging:
        log.write(str(out) + "\n")


def kwGoTo(pieces):
    """Sets the current line of the interpreter

    Args:
        pieces (String List): list of all pieces in the line
    """
    global labels, current_line
    if pieces[1] in labels:
        current_line = labels[pieces[1]] - 1
        return
    try:
        current_line = int(pieces[1]) - 2
    except:
        print(f"Error in line {current_line + 1}: Label not found {pieces[1]}")
        exit()


def kwSleep(pieces):
    """Sleeps the given time

    Args:
        pieces (String List): list of all pieces in the line
    """
    time.sleep(float(pieces[1]))


def kwMath(pieces):
    global vars
    vars[str(pieces[1])] = get_value(pieces[2])


def kwGoIf(pieces):
    """Sets the current line of the interpreter if given condition is true

    Args:
        pieces (String List): list of all pieces in the line
    """
    global current_line, labels
    res = boolSolv(pieces[2:])

    if res == 1:
        if pieces[1] in labels:
            current_line = labels[pieces[1]] - 1
            return
        try:
            current_line = int(pieces[1]) - 2
        except:
            print(f"Error in line {current_line + 1}: Label not found {pieces[1]}")
            exit()


def kwIf(pieces):
    """Executes codeblock in curly brackets if condition is true

    Args:
        pieces (String List): list of all pieces in the line
    """
    global current_line
    res = boolSolv(pieces[1:])

    if not res:
        brackets = 1
        while not brackets == 0:
            current_line += 1
            if "}" in program_lines[current_line]:
                brackets -= 1
            if "{" in program_lines[current_line]:
                brackets += 1
            if brackets < 0:
                print(f"Error in line {current_line + 1}: Unmatched brackets")
                exit()


def kwBool(pieces):
    """Creates a boolean

    Args:
        pieces (String List): list of all pieces in the line
    """
    global bools
    name = get_nonum(pieces[1], current_line).split("=")[0].strip()
    value = get_value(pieces[1].split("=")[1])

    if value == "True":
        value = 1
    elif value == "False":
        value = 0
    else:
        value = boolSolv(get_nonum(pieces[1], current_line).split("=")[1:])

    bools[name] = value


def kwImport(pieces):
    """Imports a library

    Args:
        pieces (String List): list of all pieces in the line
    """
    global libs, keywords, configPath
    try:
        lib = pieces[1]

        path = os.path.join(getPath(configPath), "libs")

        subprocess.run(
            f"mkdir {path}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )

        if not path in sys.path:
            sys.path.append(path)

        imp = __import__(lib)
        if lib not in libs:
            libs[lib] = imp
            libkws = imp.main()

            for l in libkws:
                keywords[l] = libkws[l]
    except Exception as e:
        print(f"Error in line {current_line + 1}: Library {lib} not found")
        print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
        exit()


def kwEnd(pieces):
    """Ends the programm

    Args:
        pieces (String List): list of all pieces in the line
    """
    exit()


def NONE(pieces):
    """Placeholder for keywords that do nothing

    Args:
        pieces (String List): list of all pieces in the line
    """
    return


# get the system arguments

# config
## no config

## get the filename
## always the first argument
overwrite = ""  # this is used for debugging purposes only, and should be empty in production. It will force the interpreter to load a specific file, instead of the arguments.
if len(overwrite) == 0:
    try:
        file_name = sys.argv[1]
    except:
        print("see README.md for usage")
        time.sleep(5)
        exit()
else:
    print("Running in Override Mode")
    file_name = overwrite

with open(file_name, "r") as f:
    program_lines = f.readlines()

## prints the output of the stoopid script into a file
logging = 0
if "--log" in sys.argv:
    logging = 1
    # get the log file name
    try:
        log_file = sys.argv[sys.argv.index("--log") + 1]
    except:
        print("please specify filename for log file")
        time.sleep(5)
        exit()
    log = open(log_file, "w")

## disables output completely
silent = "--silent" in sys.argv

################
# dictionary for all keywords and their functions
# add a keyword here
# create a function for it called kw<Keyword>
################
keywords = {
    "var": kwVar,
    "arr": kwArr,
    "app": kwApp,
    "getarr": kwGetArr,
    "setarr": kwSetArr,
    "out": kwOut,
    "goto": kwGoTo,
    "sleep": kwSleep,
    # "math": kwMath,
    "goif": kwGoIf,
    "if": kwIf,
    "bool": kwBool,
    "import": kwImport,
    "end": kwEnd,
    "}": NONE,
}

# main loops

## resolve all lables
for i in range(len(program_lines)):
    try:
        linepieces = getline(program_lines[i])

        if linepieces[-1] == "label":  # :name:label at the end of the line
            labels[get_nonum(linepieces[-2], i)] = i
    except Exception as e:
        print(f"Error in line {i + 1} while resolving labels:\n{str(e)}")
        exit()

## runs the code
while current_line < len(program_lines):
    # get the line
    linepieces = getline(program_lines[current_line])

    if linepieces[0] == "":
        current_line += 1
        continue

    # run the code
    if linepieces[0] in keywords:
        try:
            keywords[linepieces[0].lower()](linepieces)
        except Exception as e:
            print(f"Error in line {current_line + 1}:\n{str(e)}")
            print("interpreter crashed at line: ", e.__traceback__.tb_lineno)
            exit()
    else:
        print(f"Error in line {current_line + 1}: Unknown keyword: {linepieces[0]}")
        exit()
    current_line += 1
