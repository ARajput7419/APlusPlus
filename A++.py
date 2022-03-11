import sys
import re
import time

f = None
lines = None
data = {}


def readFile() -> None:
    """
    It takes file name from command line arguments
    and open that file with read permission
    and raise Exception if file name is not mentioned
    or file does not exist

    """

    global f, lines
    if len(sys.argv) == 1:
        raise Exception("Error : File Name is not mentioned ")
    f = open(sys.argv[1])
    lines = f.readlines()
    lines.append("EXIT")


def checker() -> bool:
    """
    It checks whether user program contains un-matched parenthesis or not

    """

    count = 0
    for line in lines:
        for ch in line:
            if ch == '{':
                count += 1
            elif ch == '}':
                if count > 0:
                    count -= 1
                else:
                    return False
    return count == 0


def isnumber(num: str) -> int:
    """
    It takes a valid token.
    :return 1 if it is of integer type
    :return 2 if it is of float type
    :return 0 if it is not of numerical type
    """

    try:
        if num.find(".") != -1:
            float(num)
            return 2
        else:
            int(num)
            return 1
    except Exception as e:
        return 0


def isboolean(a: str) -> bool:
    """
    It checks whether type of the data is boolean or not
    """

    if a in data:
        return type(data[a]) == bool
    else:
        return a == 'TRUE' or a == 'FALSE'


def ope(a: 'any', op: str, b: 'any', line: int) -> bool:
    """
    It takes two operands , one operator and line number .
    It evaluates only [ < , <= , > , >= , == , != ] and returns boolean value .
    It also raise Exception if invalid operator is found

    """

    if op == '<':
        return a < b
    elif op == '<=':
        return a <= b
    elif op == '==':
        return a == b
    elif op == '>':
        return a > b
    elif op == '>=':
        return a >= b
    elif op == '!=':
        return a != b
    else:
        raise Exception(f"Invalid Operator at line {line + 1}")


def getValue(a: str) -> 'any type of data':
    """
    It takes a  token and returns value that can be literal or stored in dictionary [ DATA STRUCTURE USED
    HERE FOR STORING THE USER DEFINED VARIABLES ]

    """

    if a in data:
        return data[a]
    else:
        if a == 'TRUE':
            return True
        elif a == 'FALSE':
            return False
        elif isnumber(a) == 1:
            return int(a)
        elif isnumber(a) == 2:
            return float(a)
        elif isString(a):
            return a[1:len(a) - 1]
        else:
            raise Exception(f"There is some error ")


def return_valid_function(op: str, line: int) -> 'function':
    """
    It takes operator and returns corresponding method for evaluations of the expression
    and also raise exception if invalid operator is found
    """

    if op == '+':
        return add
    elif op == '-':
        return sub
    elif op == '/':
        return divide
    elif op == '*':
        return mul
    elif op == '^':
        return pow
    elif op == '%':
        return mod
    else:
        raise Exception(f"Invalid Operator used at line {line + 1}")


def for_handler(c, line):
    """
       It deals with the for loop .
       It takes list of tokens and line number where for loop starts
       It returns the line number to be executed after executing for loop block .
       It also deals with BREAK and CONTINUE statements .
       It use executor method to execute lines except BREAK and CONTINUE .

    """

    if line + 1 >= len(lines):
        raise Exception("There is some error ")
    t = return_list_for_a_line(line + 1)
    if len(t) == 0:
        raise Exception(f"There is some error at line {line + 2}")
    t = t[0]
    if t != '{':
        raise Exception(f"There is some error at line {line + 2}")
    else:
        i = line + 2
        open_b = 1
        for k in range(i, len(lines)):
            temp = return_list_for_a_line(k)
            if len(temp) == 0:
                raise Exception(f"There is some error at line {k + 1}")
            temp = temp[0]
            if temp == '}' and open_b == 1:
                last_i = k
                break
            elif temp == '}' and open_b > 1:
                open_b -= 1
            elif temp == '{':
                open_b += 1

    if ope(getValue(c[4]), c[5], getValue(c[6]), line):

        while i <= last_i:
            temp = return_list_for_a_line(i)
            c1 = temp
            if len(temp) == 0:
                raise Exception(f"There is some error at line {i + 1}")
            temp = temp[0]
            if temp == 'BREAK':
                return last_i
            elif temp == 'CONTINUE':
                fun = return_valid_function(c[10], line)
                fun(c[7:], line)
                for_handler(c, line)
                return last_i
            elif temp in ['{', '}']:
                i = i + 1
                continue
            elif temp == 'CHECK':
                i = check_handler(c1, i)
            i = executor(i)
        fun = return_valid_function(c[10], line)
        fun(c[7:], line)
        for_handler(c, line)
    return last_i


def while_handler(c: list, line: int) -> int:
    """
    It deals with the while loop .
    It takes list of tokens and line number where while loop starts
    It returns the line number to be executed after executing while loop block .
    It also deals with BREAK and CONTINUE statements
    It use executor method to execute lines except BREAK and CONTINUE .

    """

    if line + 1 >= len(lines):
        raise Exception("There is some error ")
    t = return_list_for_a_line(line + 1)
    if len(t) == 0:
        raise Exception(f"There is some error at line {line + 2}")
    t = t[0]
    if t != '{':
        raise Exception(f"There is some error at line {line + 2}")
    else:
        i = line + 2
        open_b = 1
        for k in range(i, len(lines)):
            temp = return_list_for_a_line(k)
            if len(temp) == 0:
                raise Exception(f"There is some error at line {k + 1}")
            temp = temp[0]
            if temp == '}' and open_b == 1:
                last_i = k
                break
            elif temp == '}' and open_b > 1:
                open_b -= 1
            elif temp == '{':
                open_b += 1
    if len(c) == 2:
        test = getValue(c[1])
    else:
        test = ope(getValue(c[1]), c[2], getValue(c[3]), line)
    if test:
        while i <= last_i:
            temp = return_list_for_a_line(i)
            if len(temp) == 0:
                raise Exception(f"There is some error at line {i + 1}")
            c1 = temp
            temp = temp[0]
            if temp == 'BREAK':
                return last_i
            elif temp == 'CONTINUE':
                while_handler(c, line)
                return last_i
            elif temp == 'CHECK':
                i = check_handler(c1, i)
            i = executor(i)
        while_handler(c, line)
    return last_i


def numeric(n: 'any') -> bool:
    """
    It checks whether data is numerical or not
    """

    return type(n) == int or type(n) == float


def isString(a: str) -> bool:
    """
    It checks whether a token is string literal or not

    """

    return len(a) >= 2 and a[0] == '"' and a[len(a) - 1] == '"'


def add(ins: list, line: int) -> None:
    """
        It evaluates addition operator + and makes appropriate changes in the variable .
        It also checks operand types and raise exceptions if valid operands are not found

    """

    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if type(data[ins[2]]) == str and type(data[ins[4]]) == str:
                data[ins[0]] = data[ins[2]] + data[ins[4]]
            elif numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] + data[ins[4]]
            else:
                raise Exception(f"Invalid Use of + operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isString(ins[2]) and type(data[ins[4]]) == str:
                data[ins[0]] = ins[2][1:len(ins[2]) - 1] + data[ins[4]]
            elif isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d + data[ins[4]]
            else:
                raise Exception(f"Invalid Use of + operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isString(ins[4]) and type(data[ins[2]]) == str:
                data[ins[0]] = data[ins[2]] + ins[4][1:len(ins[4]) - 1]
            elif isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = d + data[ins[2]]
            else:
                raise Exception(f"Invalid Use of + operator at line {line + 1}")
        else:
            if isString(ins[4]) and isString(ins[2]):
                data[ins[0]] = ins[2][1:len(ins[2]) - 1] + ins[4][1:len(ins[4]) - 1]
            elif isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = d + b
            else:
                raise Exception(f"Invalid Use of + operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def mul(ins: list, line: int) -> None:
    """
        It evaluates multiplication operator * and makes appropriate changes in the variable .
        It also checks operand types and raise exceptions if valid operands are not found

    """

    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] * data[ins[4]]
            else:
                raise Exception(f"Invalid Use of * operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d * data[ins[4]]
            else:
                raise Exception(f"Invalid Use of * operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = d * data[ins[2]]
            else:
                raise Exception(f"Invalid Use of * operator at line {line + 1}")
        else:
            if isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = d * b
            else:
                raise Exception(f"Invalid Use of * operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def sub(ins: list, line: int) -> None:
    """
        It evaluates minus operator - and makes appropriate changes in the variable .
        It also checks operand types and raise exceptions if valid operands are not found

    """

    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] - data[ins[4]]
            else:
                raise Exception(f"Invalid Use of - operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d - data[ins[4]]
            else:
                raise Exception(f"Invalid Use of - operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = data[ins[2]] - d
            else:
                raise Exception(f"Invalid Use of - operator at line {line + 1}")
        else:
            if isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = b - d
            else:
                raise Exception(f"Invalid Use of - operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def divide(ins: list, line: int) -> None:
    """
        It evaluates divide operator / and makes appropriate changes in the variable .
        It also checks operand types and raise exceptions if valid operands are not found

    """

    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] / data[ins[4]]
            else:
                raise Exception(f"Invalid Use of / operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d / data[ins[4]]
            else:
                raise Exception(f"Invalid Use of / operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = data[ins[2]] / d
            else:
                raise Exception(f"Invalid Use of / operator at line {line + 1}")
        else:
            if isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = b / d
            else:
                raise Exception(f"Invalid Use of / operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def mod(ins: list, line: int) -> None:
    """
        It evaluates mod operator % and makes appropriate changes in the variable .
        It also checks operand types and raise exceptions if valid operands are not found

    """
    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] % data[ins[4]]
            else:
                raise Exception(f"Invalid Use of % operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d % data[ins[4]]
            else:
                raise Exception(f"Invalid Use of % operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = data[ins[2]] % d
            else:
                raise Exception(f"Invalid Use of % operator at line {line + 1}")
        else:
            if isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = b % d
            else:
                raise Exception(f"Invalid Use of % operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def pow(ins: list, line: int) -> None:
    """
    It evaluates power operator ^ and makes appropriate changes in the variable .
    It also checks operand types and raise exceptions if valid operands are not found

    """

    if isValidIdentifier(ins[0]):
        if ins[2] in data and ins[4] in data:
            if numeric(data[ins[2]]) and numeric(data[ins[4]]):
                data[ins[0]] = data[ins[2]] ** data[ins[4]]
            else:
                raise Exception(f"Invalid Use of ^ operator at line {line + 1}")
        elif ins[2] not in data and ins[4] in data:
            if isnumber(ins[2]) != 0 and numeric(data[ins[4]]):
                if isnumber(ins[2]) == 1:
                    d = int(ins[2])
                else:
                    d = float(ins[2])
                data[ins[0]] = d ** data[ins[4]]
            else:
                raise Exception(f"Invalid Use of ^ operator at line {line + 1}")
        elif ins[2] in data and ins[4] not in data:
            if isnumber(ins[4]) != 0 and numeric(data[ins[2]]):
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])
                data[ins[0]] = data[ins[2]] ** d
            else:
                raise Exception(f"Invalid Use of ^ operator at line {line + 1}")
        else:
            if isnumber(ins[4]) != 0 and isnumber(ins[2]) != 0:
                if isnumber(ins[4]) == 1:
                    d = int(ins[4])
                else:
                    d = float(ins[4])

                if isnumber(ins[2]) == 1:
                    b = int(ins[2])
                else:
                    b = float(ins[2])
                data[ins[0]] = b ** d
            else:
                raise Exception(f"Invalid Use of ^ operator at line {line + 1}")
    else:
        raise Exception(f"Invalid Identifier at line {line + 1}")


def isValidIdentifier(id: str) -> bool:
    """
    It checks whether a token is valid identifier or not
    """

    return re.fullmatch("[a-zA-Z_$]+[a-zA-Z0-9]*", id) and (
            id not in ['TRUE', 'WHILE', 'FOR', 'FALSE', 'CHECK', 'BREAK', 'CONTINUE'])


def preprocessing(c: list) -> list:
    """
    It takes list of tokens and
    returns list of token after removing empty tokens
    """

    res = []
    for i in c:
        if i != '':
            res.append(i)
    return res


def helper(ins: str) -> list:
    """
    It is useful when code consist " characters .
    Because we want string literal as a single token so we are maintaining two pointers points to the both double
    quotes and split left and right parts on the basis of whitespace characters and appending string literal
    as a single token into the final resultant list .

    """

    res = []
    i = 0
    while ins[i] != '"':
        i += 1
    j = i + 1
    while ins[j] != '"':
        j = j + 1
    op = re.split(r"\s+", ins[:i])
    for k in op:
        res.append(k)
    res.append(ins[i:j + 1])
    op = re.split(r"\s+", ins[j + 1:])
    for k in op:
        res.append(k)
    return res


def return_list_for_a_line(line: int) -> list:
    """
    It takes line number convert code of that line into tokens
    by separating code using whitespaces . It also admit that all tokens would be having
    length at least one .

    """

    if lines[line].count('"') == 0:
        c = re.split(r"\s+", lines[line])
    elif lines[line].count('"') != 2:
        raise Exception(f"Error : Line Number {line + 1}")
    else:
        c = helper(lines[line])
    c = preprocessing(c)
    return c


def executor(line: int) -> int:
    """
    It takes the line number , executes code of that line and returns
    the next pointer [ line ] to be executed
    It executes instructions like :
    CAST_INT
    CAST_STR
    CAST_FLOAT
    CAST_BOOL
    READ
    TYPE
    PRINT
    EXIT
    SLEEP
    WHILE LOOP
    FOR LOOP
    CHECK BLOCK
    VARIABLE INITIALIZATION
    BINARY OPERATIONS


    [ Refer README file for the proper syntax ]
    """

    new = line
    c = return_list_for_a_line(line)
    if len(c) == 0:
        return new + 1
    if len(c) == 1:
        if c[0] == 'EXIT':
            print("Program is executed successfully ")
            exit(100)
        elif c[0] in ['{', '}']:
            return new + 1
        else:
            raise Exception(f"Error : Invalid Instructions [ Line : {line + 1} ] ")
    elif len(c) == 2:
        if c[0] == 'SLEEP':
            if isnumber(c[1]) != 0:
                time.sleep(int(c[1]))
            elif c[1] in data:
                if type(data[c[1]]) == int or type(data[c[1]]) == float:
                    time.sleep(int(data[c[1]]))
                else:
                    raise Exception(f"Variable is not of numeric type at line {line}")
            else:
                raise Exception(f"Error : {c[1]} is not a number ")
        elif c[0] == 'PRINT':
            if c[1] in data:
                print(data[c[1]])
            elif isnumber(c[1]) != 0:
                print(c[1])
            elif len(c[1]) >= 2 and c[1][0] == '"' and c[1][len(c[1]) - 1] == '"':
                print(c[1][1:len(c[1]) - 1])
            elif c[1] == 'TRUE' or c[1] == 'FALSE':
                print(c[1])
            else:
                raise Exception(f"Error : {c[1]} is not defined ")
        elif c[0] == 'READ':
            if isValidIdentifier(c[1]):
                data[c[1]] = input()
            else:
                raise Exception(f"Error : {c[1]} is not valid a Identifier ")
        elif c[0] == 'CAST_INT':
            if c[1] in data:
                try:
                    data[c[1]] = int(data[c[1]])
                except Exception as e:
                    raise Exception(f"Error [{line + 1}] : Can not cast into integer ")
            else:
                raise Exception(f"Error : Variable {c[1]} is not defined ")

        elif c[0] == 'CAST_STR':
            if c[1] in data:
                data[c[1]] = str(data[c[1]])
            else:
                raise Exception(f"Error : Variable {c[1]} is not defined ")
        elif c[0] == 'CAST_FLOAT':
            if c[1] in data:
                try:
                    data[c[1]] = float(data[c[1]])
                except Exception as e:
                    raise Exception(f"Error [{line + 1}] : Can not cast into float ")
            else:
                raise Exception(f"Error : Variable {c[1]} is not defined ")
        elif c[0] == 'CAST_BOOL':
            if c[1] in data:
                if not (data[c[1]] == True or data[c[1]] == False):
                    if data[c[1]] == 'TRUE':
                        data[c[1]] = True
                    elif data[c[1]] == 'FALSE':
                        data[c[1]] = False
                    else:
                        raise Exception(f"Error [{line + 1}] : Can not cast into bool")
            else:
                raise Exception(f"Error : Variable {c[1]} is not defined ")
        elif c[0] == 'TYPE':
            if c[1] in data:
                print(type(data[c[1]]))
            else:
                st = isnumber(c[1])
                if st == 0:
                    print(type(""))
                elif st == 1:
                    print(type(1))
                elif st == 2:
                    print(type(0.23))
                elif c[1] == 'TRUE' or c[1] == 'FALSE':
                    print(type(True))
                else:
                    raise Exception(f"Error Found at line {line + 1}")
        elif c[0] == 'WHILE':
            new = while_handler(c, line)
        elif c[0] == 'CHECK':
            new = check_handler(c, line)
        else:
            raise Exception(f"Invalid Instruction at line {line + 1}")
    elif len(c) == 3:
        if c[1] == '=':
            if isValidIdentifier(c[0]):
                if c[2] in data:
                    data[c[0]] = data[c[2]]
                elif isnumber(c[2]) == 1:
                    data[c[0]] = int(c[2])
                elif isnumber(c[2]) == 2:
                    data[c[0]] = float(c[2])
                elif c[2] == 'TRUE':
                    data[c[0]] = True
                elif c[2] == 'FALSE':
                    data[c[0]] = False
                elif len(c[2]) >= 2 and c[2][0] == '"' and c[2][len(c[2]) - 1] == '"':
                    data[c[0]] = c[2][1:len(c[2]) - 1]
                else:
                    raise Exception(f"Error: Variable is not defined at line {line + 1}")
            else:
                raise Exception(f"Error : {c[0]} is not a valid identifier ")
        else:
            raise Exception(f"Invalid Instruction at line {line + 1}")
    elif len(c) == 4:
        if c[0] == 'WHILE':
            new = while_handler(c, line)
        elif c[0] == 'CHECK':
            new = check_handler(c, line)
        else:
            raise Exception(f"Invalid Instruction at line {line + 1}")

    elif len(c) == 5:
        if c[1] == '=':
            if c[3] == '+':
                add(c, line)
            elif c[3] == '-':
                sub(c, line)
            elif c[3] == '^':
                pow(c, line)
            elif c[3] == '/':
                divide(c, line)
            elif c[3] == '*':
                mul(c, line)
            elif c[3] == '%':
                mod(c, line)
            else:
                raise Exception(f"Invalid Operator at line {line + 1}")
        else:
            raise Exception(f"Invalid Instruction at line {line + 1}")
    elif len(c) == 12:
        if c[0] == 'FOR':
            data[c[1]] = getValue(c[3])
            new = for_handler(c, line)
    else:
        raise Exception(f"Invalid Instruction at line {line + 1}")
    return new + 1


def check_handler(c: list, line: int) -> int:
    """
    It takes the line number where CHECK block starts and find the matching } .
    It returns the pointers from where the execution should be started after evaluating the conditions

    """

    if line + 1 >= len(lines):
        raise Exception("There is some error ")
    t = return_list_for_a_line(line + 1)
    if len(t) == 0:
        raise Exception(f"There is some error at line {line + 2}")
    t = t[0]
    if t != '{':
        raise Exception(f"There is some error at line {line + 2}")
    else:
        i = line + 2
        open_b = 1
        for k in range(i, len(lines)):
            temp = return_list_for_a_line(k)
            if len(temp) == 0:
                raise Exception(f"There is some error at line {k + 1}")
            temp = temp[0]
            if temp == '}' and open_b == 1:
                last_i = k
                break
            elif temp == '}' and open_b > 1:
                open_b -= 1
            elif temp == '{':
                open_b += 1
    if len(c) == 2:
        test = getValue(c[1])
    else:
        test = ope(getValue(c[1]), c[2], getValue(c[3]), line)
    if test:
        return line
    else:
        return last_i


def interpreter() -> None:
    """
    Execution of the program starts with this function.
    It guarantees the complete execution of the program by maintaining the current line
    to be executed pointer.
    """

    current = 0
    while current < len(lines):
        current = executor(current)


if __name__ == '__main__':
    readFile()
    if not checker():
        raise Exception("There is some error")
    interpreter()
