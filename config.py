from enum import Enum


class BugTypeEnum(Enum):
    ENV_DEPENDENCY = 1
    REENTRANCY = 2
    INTEGER_ARITHMETIC = 3
    UNCHECKED_CALL = 4


def convert_to_enum(name):
    if name == "Dependence on predictable environment variable":
        return BugTypeEnum.ENV_DEPENDENCY
    elif name == "External Call To User-Supplied Address":
        return BugTypeEnum.REENTRANCY
    elif name == "Integer Arithmetic Bugs":
        return BugTypeEnum.INTEGER_ARITHMETIC
    elif name == "unchecked-transfer":
        return BugTypeEnum.UNCHECKED_CALL
    elif name == "State access after external call":
        return BugTypeEnum.REENTRANCY
    elif name == "reentrancy-no-eth":
        return BugTypeEnum.REENTRANCY
    elif name == "timestamp":
        return BugTypeEnum.ENV_DEPENDENCY
    elif name == "reentrancy-benign":
        return BugTypeEnum.REENTRANCY
    return name


class BugType:
    def __init__(self, name):
        self.name = convert_to_enum(name)


class Tool:
    def __init__(self, name):
        self.name = name


class BugInfo:
    def __init__(self, bug_type: BugType, tool: Tool, line_number: int, message: str, path: str, contract_name: str = "I_DONT_KNOW", function_name: str = "I_DONT_KNOW"):
        self.bug_type = bug_type
        self.tool = tool
        self.line_number = line_number[0] if isinstance(line_number, list) else line_number
        self.message = message
        self.path = path
        self.contract_name = contract_name
        self.function_name = function_name


class CsvReport:
    def __init__(self, bug_info: BugInfo):
        self.path = None
        self.contract_name = None
        self.function_name = None
        self.tool = None
        self.bug_line = None
        self.bug_type = None
        self.convert(bug_info)

    def convert(self, bug_info: BugInfo):
        self.path = bug_info.path
        self.contract_name = bug_info.contract_name
        self.function_name = bug_info.function_name
        self.bug_line = bug_info.line_number
        self.tool = bug_info.tool.name
        self.bug_type = bug_info.bug_type.name