from ..syntacticalanalyzer.semanticanalyzer.syntacticstructure import SyntacticsStructure
from ..syntacticalanalyzer.semanticanalyzer.syntacticstructure import NodeStruct


class CodeGenerator:

    def translate(self, node: NodeStruct):
        if node.name == 'PROGRAMM':
            expression = ''
            for i in node.childs:
                expression += '\n' + self.__translate_expression(i)
            return self.__add_main_program(expression)

    def __translate_expression(self, node: NodeStruct):
        if node.name in ['OPERATOR', 'ASSIGNMENT']:
            return self.__translate_bin_op(node)
        elif node.name in 'IDENTIFICATOR':
            return self.__translate_name(node)
        elif node.name == 'PROGRAMM IDENTIFICATOR':
            return ''
        elif node.name in ['INTEGER NUMBER', 'REAL NUMBER', 'BOOL VALUE']:
            return self.__translate_type_value(node)
        elif node.name == 'DECLARE A VARIABLES':
            return self.__translate_declare_a_variables(node)
        elif node.name == 'OUTPUT FUNCTION':
            pass
        elif node.name == 'STRING':
            pass
        elif node.name in ['CYCLE DO', 'CYCLE FOR', 'CYCLE WHILE']:
            pass
        elif node.name == 'IF OPERATOR':
            pass
        else:
            raise ValueError('Node {} is not supported'.format(str(node)))

    def __add_main_program(self, expression):
        return "package main\nimport \"fmt\"\nfunc main() {{\n{expression}\n}}".format(expression=expression)

    def __translate_bin_op(self, node: NodeStruct):
        operand = node.value
        return self.__translate_expression(node.childs[0]) + ' ' + operand + ' ' + self.__translate_expression(
            node.childs[1])

    def __translate_type_value(self, node: NodeStruct):
        return node.value + ' '

    def __translate_unary_op(self, node: NodeStruct):
        pass

    def __translate_num(self, node: NodeStruct):
        pass

    def __translate_name(self, node: NodeStruct):
        return node.value

    def __translate_declare_a_variables(self, node: NodeStruct):
        vars = self.__translate_expression(node.childs[0])
        l_child = len(node.childs)
        for i in range(1, l_child - 1):
            vars += ' ,' + self.__translate_expression(node.childs[i])
        vars += ' ,' + self.__translate_expression(node.childs[l_child - 1])
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

        return 'var ' + vars + ' ' + go_type[node.value]
