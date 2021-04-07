from ..syntacticalanalyzer.semanticanalyzer.syntacticstructure import SyntacticsStructure
from ..syntacticalanalyzer.semanticanalyzer.syntacticstructure import NodeStruct


class CodeGenerator:

    def translate(self, node: NodeStruct) -> str:
        if node.name == 'PROGRAMM':
            expression = ''
            for i in node.childs:
                expression += '\n   ' + self.__translate_expression(i)
            return self.__add_main_program(expression)

    def __translate_expression(self, node: NodeStruct) -> str:
        if node.name in ['OPERATOR', 'ASSIGNMENT']:
            return self.__translate_bin_op(node)
        elif node.name in 'IDENTIFICATOR':
            return self.__translate_name(node)
        elif node.name == 'PROGRAMM IDENTIFICATOR':
            return '//' + self.__translate_name(node)
        elif node.name in ['INTEGER NUMBER', 'REAL NUMBER', 'BOOL VALUE']:
            return self.__translate_type_value(node)
        elif node.name == 'DECLARE A VARIABLES':
            return self.__translate_declare_a_variables(node)
        elif node.name == 'OUTPUT FUNCTION':
            return self.__translate_output_function(node)
        elif node.name == 'STRING':
            return self.__translate_string(node)
        elif node.name in ['CYCLE DO', 'CYCLE FOR', 'CYCLE WHILE']:
            return self.__translate_cycle(node)
        elif node.name == 'IF OPERATOR':
            return self.__translate_if(node)
        elif node.name == "STANDARD FUNCTIONS":
            return self.__translate_standart_func(node)
        elif node.name == "ARGUMENTS":
            return self.__translate_arguments(node)
        else:
            raise ValueError('Node {} is not supported'.format(str(node)))

    def __add_main_program(self, expression) -> str:
        return "package main\nimport (\n\"fmt\"\n\"math\"\n)\nfunc main() {{ {expression}\n}}".format(
            expression=expression)

    def __translate_bin_op(self, node: NodeStruct) -> str:
        operand = node.value
        return self.__translate_expression(node.childs[0]) + ' ' + operand + ' ' + self.__translate_expression(
            node.childs[1])

    def __translate_type_value(self, node: NodeStruct) -> str:
        return node.value + ' '

    def __translate_name(self, node: NodeStruct) -> str:
        return node.value

    def __translate_declare_a_variables(self, node: NodeStruct) -> str:
        go_type = {
            'boolean': 'bool',
            'byte': 'int8',
            'short': 'int16',
            'int': 'int32',
            'long': 'int64',
            'double': 'float32',
            'float': 'float64',
            'char': 'string'
        }

        def insert_type(declare: str, type: str) -> str:
            if declare.find('=') != -1:
                return declare.replace("=", "{} =".format(type))
            else:
                return declare + ' ' + type

        vars = insert_type(self.__translate_expression(node.childs[0]), go_type[node.value])

        l_child = len(node.childs)
        for i in range(1, l_child):
            vars += '\n' + insert_type(self.__translate_expression(node.childs[i]), go_type[node.value])

        return 'var (\n' + vars + '\n)'

    def __translate_output_function(self, node: NodeStruct) -> str:
        bodyout = self.__translate_expression(node.childs[0])
        for i in range(1, len(node.childs)):
            bodyout += ',' + self.__translate_expression(node.childs[i])
        return "fmt.Print({})".format(bodyout)

    def __translate_if(self, node: NodeStruct) -> str:
        cond = self.__translate_expression(node.childs[0])
        body = ''
        elseflag = False
        elsebody = ''
        for i in range(1, len(node.childs)):
            if node.childs[i].name == "else":
                elseflag = True
                continue
            if elseflag:
                elsebody += '\n' + self.__translate_expression(node.childs[i])
            else:
                body += '\n' + self.__translate_expression(node.childs[i])
        if elseflag:
            return "\nif {} {{ {} \n}}else{}\n}}".format(cond, body, elsebody)
        return "\nif {} {{ {} \n}}".format(cond, body)

    def __translate_string(self, node: NodeStruct) -> str:
        return "\"" + node.value + "\""

    def __translate_cycle(self, node: NodeStruct) -> str:
        if node.childs[0].name == "DECLARE A VARIABLES":
            initialization = self.__translate_initialization(node.childs[0])
            condition = self.__translate_expression(node.childs[1])
            count = self.__translate_expression(node.childs[2])
            body = ''
            for i in range(3, len(node.childs)):
                body += self.__translate_expression(node.childs[i])
            return "\nfor {};{};{}{{\n{}\n}}".format(initialization, condition, count, body)
        elif node.childs[0].name == "OPERATOR":
            condition = self.__translate_expression(node.childs[0])
            body = ''
            for i in range(1, len(node.childs)):
                body += self.__translate_expression(node.childs[i])
            return "\nfor {}{{\n{}\n}}".format(condition, body)
        else:
            body = ''
            l_node = len(node.childs)
            for i in range(0, l_node - 1):
                body += self.__translate_expression(node.childs[i])
            condition = self.__translate_expression(node.childs[l_node - 1])
            return "for {{\n    {}\n    if {} {{\n      break\n }}\n}}".format(body, condition)

    def __translate_initialization(self, node: NodeStruct) -> str:
        initialization = self.__translate_expression(node.childs[0]).replace('=', ':=')
        return initialization

    def __translate_standart_func(self, node: NodeStruct) -> str:
        funcs_go = {
            "Math.pow": "math.Pow",
            "Math.log": "math.Log",
            "Math.sqrt": "math.Sqrt"
        }

        func = funcs_go[node.childs[0].name]
        args = self.__translate_expression(node.childs[1])
        return func + "({})".format(args)

    def __translate_arguments(self, node: NodeStruct) -> str:
        args_body = self.__translate_expression(node.childs[0])
        l_child = len(node.childs)
        for i in range(1, l_child):
            args_body += ',' + self.__translate_expression(node.childs[i])
        return args_body
