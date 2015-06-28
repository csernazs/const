import sys
import dis
import functools
from code import Code, command_to_string

UNPACK_SEQUENCE = dis.opmap["UNPACK_SEQUENCE"]
STORE_FAST = dis.opmap["STORE_FAST"]
STORE_GLOBAL = dis.opmap["STORE_GLOBAL"]
STORE_NAME = dis.opmap["STORE_NAME"]
STORE_DEREF = dis.opmap["STORE_DEREF"]

STORE_COMMANDS = {STORE_FAST, STORE_GLOBAL, STORE_NAME, STORE_DEREF}

NAMING = {}

PERMITTED = "permitted"

class UnknownCommand(Exception):
    pass

def assigned_names():
    frame = sys._getframe(2)
    code = Code(frame.f_code.co_code, frame.f_lasti)
    # skip first command
    code.next()

    names = []
    sequence_length = 1
    unpack = False
    for command, arg in code:
        if len(names) >= sequence_length:
            break

        if command == UNPACK_SEQUENCE:
            sequence_length = arg
            unpack = True

        elif command in STORE_COMMANDS:
            name_index = arg
            name_list = frame.f_code.co_names
            if command == STORE_DEREF:
                name_list = frame.f_code.co_freevars

            names.append(name_list[name_index])
        else:
            raise UnknownCommand(command_to_string(command, arg))

    assert len(names) == sequence_length
    return (names, unpack)


def register_naming(naming, callback):
    NAMING[naming] = callback

def naming(naming_id):
    def decorator(func):
        register_naming(naming_id, func)
        return func

    return decorator

@naming("DASH")
def dash(idx, value):
    return value.lower().replace("_", "-")

@naming("NUMBER0")
def number0(idx, value):
    return idx

@naming("NUMBER1")
def number1(idx, value):
    return idx+1

@naming("SAME")
def same(idx, value):
    return value

def const(naming, prefix=None):
    if not callable(naming):
        naming = NAMING[naming]

    names, unpack = assigned_names()
    if unpack:
        values = [naming(idx, value) for idx, value in enumerate(names)]
        if prefix == PERMITTED:
            return [set(values[1:])] + values[1:]
        else:
            return values
            
    else:
        return naming(0, names[0])



if __name__ == '__main__':
    class Example(object):
        CONST_A, CONST_B, CONST_C = const("NUMBER1")
        CONST_D = const("DASH")
        CONST_E, CONST_F = const("SAME")


    print Example.CONST_A
    print Example.CONST_B
    print Example.CONST_C
    print Example.CONST_D
    print Example.CONST_E
    print Example.CONST_F


