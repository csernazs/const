
import dis
import sys


class EndOfCode(Exception):
    pass

class Code(object):
    def __init__(self, code, ip=0):
        self.code = code
        self.ip = ip
        

    def get_code(self):
        try:
            return ord(self.code[self.ip])
        except IndexError:
            raise EndOfCode()

    def skip(self, cnt):
        self.ip = self.ip + cnt

    def read_code(self):
        retval = self.get_code()
        self.skip(1)
        return retval

    def read_argument(self):
        return self.read_code() + self.read_code()*256

    def __iter__(self):
        return self

    def read_command_arg(self):
        code = self.read_code()
        if code >= dis.HAVE_ARGUMENT:
            arg = self.read_argument()
        else:
            arg = None

        return (code, arg)

    def next(self):
        try:
            command, arg = self.read_command_arg()
        except EndOfCode:
            raise StopIteration()

        if command == dis.EXTENDED_ARG:
            offset = arg * 65536L
            command, arg = self.read_command_arg()
            return (command, offset+arg)
        else:
            return (command, arg)

def command_to_string(command, arg):
    if arg is not None:
        return "%s %s" % (dis.opname[command], arg)
    else:
        return dis.opname[command]
