import re

def extract_module_name(verilog_code):
    pattern = re.compile(r'\bmodule\b\s*(\w+)')
    match = pattern.search(verilog_code)
    
    if match:
        return match.group(1)  # Return the module name
    else:
        return None  # Return None if no module name is found

def extract_input_names(verilog_code):
    
    input_pattern = re.compile(r'(?:\binput\b)\s*(?:reg|wire)?\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,; ]|$)')
    matches = input_pattern.findall(verilog_code)
    
    return matches

def extract_output_names(verilog_code):

    # Use a different pattern to match inputs and outputs
    pattern = re.compile(r'(?:\boutput\b)\s*(?:reg|wire)?\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,; ]|$)')
    matches = pattern.findall(verilog_code)

    return matches

def extract_reg_names(verilog_code):
    # Match reg declarations with or without bit width
    pattern = re.compile(r'(?<!output\s)\breg\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,;]|$)')
    matches = pattern.findall(verilog_code)

    return matches

def extract_wire_names(verilog_code):
    # Match wire declarations with or without bit width
    pattern = re.compile(r'(?<!input\s)\bwire\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,;]|$)')
    matches = pattern.findall(verilog_code)

    return matches

def extract_bit_width(verilog_code, signal_name):
    pattern = re.compile(r'\b(?:input|output|reg|wire)\s*\[([0-9]+)\s*:\s*[0-9]+\]\s*' + re.escape(signal_name) + r'\s*[,; ]')
    match = pattern.search(verilog_code)
    
    if match:
        return int(match.group(1)) + 1  # Adding 1 to account for zero-based indexing
    else:
        return 1  # Default bit width is 1

    
def assign_bits_to_signals(names):
    signals_with_bits = {}
    for name in names:
        bits = extract_bit_width(rtl_code, name)
        signals_with_bits[name] = bits

    return signals_with_bits

# This script generates a Verilog testbench file for a given Verilog file
def search_word_in_verilog(verilog_code, search_word):
    # Split the Verilog code into lines
    lines = verilog_code.split('\n')

    # Search for the specific word in each line
    for line_number, line in enumerate(lines, start=1):
        if search_word in line:
            print(f'Found "{search_word}" in line {line_number}: {line.strip()}')


def remove_comments(verilog_code):
    # Remove single-line comments
    while "//" in verilog_code:
        start_index = verilog_code.find("//")
        end_index = verilog_code.find("\n", start_index)
        verilog_code = verilog_code[:start_index] + verilog_code[end_index:]

    # Remove multi-line comments
    while "/*" in verilog_code:
        start_index = verilog_code.find("/*")
        end_index = verilog_code.find("*/") + 2
        verilog_code = verilog_code[:start_index] + verilog_code[end_index:]

    return verilog_code

def extract_case_conditions(verilog_code):
    case_conditions = {}

    # Find all case statements along with their bodies
    case_pattern = re.compile(r'\bcase\s*\((\w+)\)\s*(.*?)\bendcase\b', re.DOTALL)
    matches = case_pattern.finditer(verilog_code)

    for match in matches:
        condition_variable = match.group(1)
        case_body = match.group(2)
        
        # Extract individual conditions from the case body
        condition_values = re.findall(r'([^\s:]+)\s*:', case_body)

        case_conditions[condition_variable] = condition_values

    return case_conditions

def parse_if_statements(verilog_code):
    pattern = re.compile(r'\bif\s*\((.*?)\)\s*|else\s*if\s*\((.*?)\)\s*', re.DOTALL)
    matches = pattern.findall(verilog_code)

    parsed_conditions = []
    for match in matches:
        if_condition, elseif_condition = match
        condition = if_condition if if_condition else elseif_condition

        # Check if the condition is a single variable
        if re.fullmatch(r'\w+', condition):
            # If so, assume the operator is '==' and the value is '1'
            parsed_conditions.append({
                'variable': condition.strip(),
                'operator': '==',
                'value': '1'
            })
        elif re.fullmatch(r'~\w+', condition):
            # Handle unary operator like '~', interpreted as '!=' to '1'
            parsed_conditions.append({
                'variable': condition[1:].strip(),  # Strip off the unary operator
                'operator': '!=',
                'value': '1'
            })
        else:
            # Split the condition into variable, operator, and value
            condition_parts = re.split(r'(\W+)', condition)
            if len(condition_parts) >= 3:
                variable = condition_parts[0].strip()
                operator = condition_parts[1].strip()
                value = ''.join(condition_parts[2:]).strip()

                parsed_conditions.append({
                    'variable': variable,
                    'operator': operator,
                    'value': value
                })

    return parsed_conditions

def clean_expression(expression):
    # Encode to bytes, ignore non-ascii characters, then decode back to string
    cleaned_expression = expression.encode('ascii', 'ignore').decode()

    # Remove any non-alphanumeric and non-operator characters
    cleaned_expression = re.sub(r'[^\w\s\+\-\*/&|~^<>=?:\.,\[\]]', '', cleaned_expression)

    return cleaned_expression.strip()

def extract_continuous_assignments(verilog_code):
    # Regular expression to match continuous assignments
    continuous_assignment_pattern = re.compile(r'\bassign\b\s+(\w+)\s*=\s*([^;]*);')

    # Find all matches in the Verilog code
    matches = continuous_assignment_pattern.findall(verilog_code)

    # Extract variable and operands from each match
    continuous_assignments = []
    for variable, expression in matches:
        # Clean the expression and extract operands
        cleaned_expression = clean_expression(expression)
        operands = re.findall(r'\b(\w+)\b', cleaned_expression)
        operands = [operand for operand in operands if not operand[0].isdigit()]  # Ignore operands that start with a digit
        continuous_assignments.append({'variable': variable, 'operands': list(set(operands))})

    return continuous_assignments
    
def extract_always_blocks(verilog_code):
    always_blocks = []

    # Find all always blocks along with their bodies
    always_pattern = re.compile(r'\balways\s*@\s*\((.*?)\)\s*(.*?)\bend\b', re.DOTALL)
    matches = always_pattern.finditer(verilog_code)

    for match in matches:
        sensitivity_list = match.group(1)
        always_body = match.group(2)

        # Check if the always block is combinational or clock based
        # A combinational always block has a sensitivity list with only signals and operators
        # A clock based always block has a sensitivity list with at least one posedge or negedge keyword
        if 'posedge' in sensitivity_list or 'negedge' in sensitivity_list:
            block_type = 'clock based'
        else:
            block_type = 'combinational'

        # Extract the variables and expressions from the always body
        # Assume the always body is a series of if-else statements
        variables = []
        expressions = []
        if_pattern = re.compile(r'\bif\s*\((.*?)\)\s*(.*?)\belse\b', re.DOTALL)
        if_matches = if_pattern.findall(always_body)
        for condition, statement in if_matches:
            # Clean the condition and statement and extract operands
            cleaned_condition = clean_expression(condition)
            cleaned_statement = clean_expression(statement)
            condition_operands = re.findall(r'\b(\w+)\b', cleaned_condition)
            statement_operands = re.findall(r'\b(\w+)\b', cleaned_statement)
            condition_operands = [operand for operand in condition_operands if not operand[0].isdigit()]  # Ignore operands that start with a digit
            statement_operands = [operand for operand in statement_operands if not operand[0].isdigit()]  # Ignore operands that start with a digit
            variables.extend(statement_operands)
            expressions.append({'condition': condition_operands, 'statement': statement_operands})

        # Store the always block information in a dictionary
        always_block = {'type': block_type, 'sensitivity_list': sensitivity_list, 'variables': list(set(variables)), 'expressions': expressions}
        
        # Add begin and end keywords to the always block body
        always_body = 'begin\n' + always_body + '\nend'
        
        # Add the modified always block to the list
        always_blocks.append({'always_body': always_body, 'always_block': always_block})

    return always_blocks

def extract_non_blocking_assignments(verilog_code):
    # Regular expression to match non-blocking assignments
    non_blocking_assignment_pattern = re.compile(r'\b(\w+)\s*<=\s*([^;]*);')

    # Find all matches in the Verilog code
    matches = non_blocking_assignment_pattern.findall(verilog_code)

    # Extract variable and expression from each match
    non_blocking_assignments = []
    for variable, expression in matches:
        # Add the entire expression as an operand
        non_blocking_assignments.append({'variable': variable, 'expression': expression.strip()})

    return non_blocking_assignments

def extract_clock_reset(rtl_code):
    # Regular expression to match always blocks and their sensitivity lists
    always_block_pattern = re.compile(r'always\s*@\s*\((.*?)\)\s*begin(.*?)end', re.DOTALL)

    # Initialize the result dictionary
    result = {'clockName': '', 'clockEdge': '', 'resetName': '', 'resetEdge': ''}

    # Find all always blocks in the RTL code
    always_blocks = always_block_pattern.findall(rtl_code)

    for sensitivity_list, block_content in always_blocks:
        # Check for posedge or negedge in the sensitivity list
        edge_pattern = re.compile(r'(posedge|negedge)\s+(\w+)')
        edges = edge_pattern.findall(sensitivity_list)

        for edge, signal in edges:
            # Check if the signal is used in an if-statement (likely a reset)
            # Accommodate both 'if (reset)' and 'if (~reset)' conditions
            if re.search(rf'\bif\s*\(\s*!?{signal}\b|\bif\s*\(\s*~{signal}\b', block_content, re.IGNORECASE):
                result['resetName'] = signal
                result['resetEdge'] = edge
            else:
                # If not in an if-statement, it's likely a clock
                result['clockName'] = signal
                result['clockEdge'] = edge

        # Break if both clock and reset are found
        if result['clockName'] and result['resetName']:
            break

    return result

def moniter_displayer(monitor_signals, extracted_clock, extracted_reset):
    monitor_code = "\n  // Monitoring signals\n"
    monitor_format = ', '.join([f'{signal} = %b' for signal in monitor_signals if signal not in [extracted_clock, extracted_reset]])
    monitor_code += f"initial begin\n"
    monitor_code += f" $monitor(\"{monitor_format}\", {', '.join(signal for signal in monitor_signals if signal not in [extracted_clock, extracted_reset])});\n"
    monitor_code += "end\n"
    return monitor_code

def is_combinatonal(clock):
    if clock == "":
        return True
    else:
        return False

def generate_initial_block():  
    initialization_code = "  initial begin\n"
    return initialization_code

def generate_clock_signal(clock_name):
    if (clock_name == ""):
        return ""
    clock_signal = f"  reg {clock_name};\n"
    clock_signal += f"  {clock_name} = 0;\n"
    clock_signal += f"  always #5 {clock_name} = ~{clock_name};\n\n"
    return clock_signal

def generate_input_declarations(inputs_with_bits, extracted_clock):
    input_declarations = ""
    for name, bits in inputs_with_bits.items():
        if name == extracted_clock:
            continue
        if bits == 1:
            input_declarations += f"  reg {name};\n"
        else:
            input_declarations += f"  reg [{bits-1}:0] {name};\n"
    input_declarations += "\n"
    return input_declarations

def generate_output_declarations(output_with_bits):
    output_declarations = ""
    for name, bits in output_with_bits.items():
        if bits == 1:
            output_declarations += f"  wire {name};\n"
        else:
            output_declarations += f"  wire [{bits-1}:0] {name};\n"
    output_declarations += "\n"
    return output_declarations

def instantiate_dut(module_name, inputs_with_bits, output_with_bits):
    dut_instantiation = f"  {module_name} DUT (\n"
    all_ports = [f".{name}({name})" for name in list(inputs_with_bits.keys()) + list(output_with_bits.keys())]
    dut_instantiation += ",\n".join(f"    {port}" for port in all_ports)
    dut_instantiation += "\n  );\n\n"
    return dut_instantiation

def initialize_inputs(inputs_with_bits, extracted_clock):
    initialization_code = "  // Initialize inputs\n"
    for name in inputs_with_bits.keys():
        if name not in [extracted_clock]:
            initialization_code += f"    {name} = 0;\n"
    initialization_code += "    #10;\n\n"
    return initialization_code


def generate_random_test_cases(inputs_with_bits, extracted_clock, extracted_reset):
    random_test_cases = "    // Random Test Cases\n"

    random_test_cases += "    integer i;\n"
    random_test_cases += "    for (i = 0; i < 5000; i = i + 1) begin\n"
    random_test_cases += "      #10;\n"
    for name, bits in inputs_with_bits.items():
        if name not in [extracted_clock, extracted_reset]:
            random_test_cases += f"      {name} = $random();\n"
    random_test_cases += "    end\n\n"
    return random_test_cases

def end_initial_block():
    return "  end\n"

def tb_generator(verilog_file, tb_file):
    isCombinational = True
    file = open(verilog_file, 'r')
    rtl_code = file.read()
    rtl_code = remove_comments(rtl_code)
    rtl_code = " ".join(rtl_code.split())
    module_name = extract_module_name(rtl_code)
    input_names = extract_input_names(rtl_code)
    output_names = extract_output_names(rtl_code)
    reg_names = extract_reg_names(rtl_code)
    wire_names = extract_wire_names(rtl_code)
    inputs_with_bits = assign_bits_to_signals(input_names)
    output_with_bits = assign_bits_to_signals(output_names)
    reg_with_bits = assign_bits_to_signals(reg_names)
    wire_with_bits = assign_bits_to_signals(wire_names)
    case_conditions = extract_case_conditions(rtl_code)
    extracted_continuous_assignments = extract_continuous_assignments(rtl_code)
    parsed_ifs = parse_if_statements(rtl_code)
    extracted_non_blocking_assignments = extract_non_blocking_assignments(rtl_code)
    extracted_always_blocks = extract_always_blocks(rtl_code)
    extracted_clock_reset = extract_clock_reset(rtl_code)
    extracted_clock = extracted_clock_reset["clockName"]
    extracted_reset = extracted_clock_reset["resetName"]
    extracted_clock_edge = extracted_clock_reset["clockEdge"]
    extracted_reset_edge = extracted_clock_reset["resetEdge"]
    isCombinational = is_combinatonal(extracted_clock)
    
    tbfile = open(tb_file, "w")

    # Generate testbench code
    testbench_code = ""
    testbench_code += f"// Testbench for {module_name}\n"
    testbench_code += f"`timescale 1ns / 1ps\n\n"
    testbench_code += f"module {module_name}_tb;\n\n"
    
    # Generate clock signal
    if (isCombinational == False):
        testbench_code += generate_clock_signal(extracted_clock)

    # Generate input and output declarations
    testbench_code += generate_input_declarations(inputs_with_bits, extracted_clock)
    testbench_code += generate_output_declarations(output_with_bits)

    # Instantiate the DUT
    testbench_code += instantiate_dut(module_name, inputs_with_bits, output_with_bits)
    
    #G
    testbench_code += generate_initial_block()
    
    # Initialize inputs
    if (isCombinational == False):
        testbench_code += initialize_inputs(inputs_with_bits, extracted_clock)

    # Generate random test cases
    testbench_code += generate_random_test_cases(inputs_with_bits, extracted_clock, extracted_reset)

    # End initial block
    testbench_code += end_initial_block()

    # Generate monitor code
    monitor_signals = list(inputs_with_bits.keys()) + list(output_with_bits.keys())
    testbench_code += moniter_displayer(monitor_signals, extracted_clock, extracted_reset)

    # End module
    testbench_code += "endmodule"

    tbfile.write(testbench_code)
    tbfile.close()






verilog_file = "binaryCounter.v"
file = open(verilog_file, 'r')
rtl_code = file.read()
tb_file = "binarytb.v"
testbench_code = tb_generator(verilog_file, tb_file)

# TODO 
# instead #10 make it @(negedge clk)
# reset = 1; or reset = 0;
# directed cases
