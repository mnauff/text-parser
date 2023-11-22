class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute_command(self, inputs):
        commands = inputs.split("\n")

        def cetak_output(*args):
            formatted_result = ''.join(str(arg) for arg in args)
            print(formatted_result)

        def process_assignment(assign_command):
            parts = assign_command.split('=')
            variable_name = parts[0].strip()
            value = parts[1].strip().strip('"').strip("'")
            try:
                self.variables[variable_name] = self.evaluate_expression(value)
            except NameError:
                self.variables[variable_name] = self.evaluate_expression(value)

        i = 0
        while i < len(commands):
            command = commands[i].strip()

            if '=' in command:
                process_assignment(command)

            elif command.startswith('cetak'):
                arguments = command.split('(')[1].split(')')[0]
                cleaned_args = [arg.strip().strip('"').strip("'") for arg in arguments.split(',')]
                result_value = self.evaluate_expression(arguments)
                cetak_output(result_value)

            elif command.startswith('if'):
                condition = command.split('if ')[1].split(':')[0]
                block = command.split(':')[1:]
                if self.evaluate_expression(condition):
                    inner_commands = block[0].split('\n')
                    for inner_command in inner_commands:
                        inner_command = inner_command.strip()
                        if 'cetak' in inner_command:
                            arguments = inner_command.split('(')[1].split(')')[0]
                            result_value = self.evaluate_expression(arguments)
                            cetak_output(result_value)
                        elif '=' in inner_command:
                            process_assignment(inner_command)
                        elif inner_command.startswith('goto'):
                            label = inner_command.split(' ')[1]
                            goto_index = 0
                            for idx, line in enumerate(commands):
                                if label + ':' in line:
                                    goto_index = idx
                                    break
                            i = goto_index - 1  # set index to the label line

            elif command.startswith('goto'):
                label = command.split(' ')[1]
                goto_index = 0
                for idx, line in enumerate(commands):
                    if label + ':' in line:
                        goto_index = idx
                        break
                i = goto_index - 1  # set index to the label line

            i += 1

    def evaluate_expression(self, expression):
        try:
            return eval(expression, self.variables)
        except NameError as e:
            return str(e)


# Example string file with more complex 'goto' usage
input_string = """
a = 1
b = 2
c = a + b
cetak(c)

x = 10
label:
x = x + 10
cetak(x)
if (x < 100): goto label

d = 20
cetak(f"nilai d adalah {d}")

goto end

e = 30
cetak(e)

end:
cetak("Selesai")
"""

tester = Interpreter()
tester.execute_command(input_string)
