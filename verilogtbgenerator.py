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

def write_testbench(module_name, inputs_with_bits, outputs_with_bits, case_conditions, parsed_ifs, extracted_clock, extracted_reset):
    testbench = f"// Testbench for {module_name}\n"
    testbench += f"`timescale 1ns / 1ps\n\n"
    testbench += f"module {module_name}_tb;\n\n"

    # Generate a clock with the name specified in extracted_clock
    testbench += f"  reg {extracted_clock};\n"
    testbench += f"  {extracted_clock} = 0;\n"
    testbench += f"  always #5 {extracted_clock} = ~{extracted_clock};\n\n"

    # Declare regs for inputs and wires for outputs
    for name, bits in inputs_with_bits.items():
        if name == extracted_clock:
            continue
        if bits == 1:
            testbench += f"  reg {name};\n"
        else:
            testbench += f"  reg [{bits-1}:0] {name};\n"
    testbench += "\n"
    
    for name, bits in outputs_with_bits.items():
        if bits == 1:
            testbench += f"  wire {name};\n"
        else:
            testbench += f"  wire [{bits-1}:0] {name};\n"
    testbench += "\n"

    # Instantiate the DUT
    testbench += f"  {module_name} DUT (\n"
    all_ports = [f".{name}({name})" for name in list(inputs_with_bits.keys()) + list(outputs_with_bits.keys())]
    testbench += ",\n".join(f"    {port}" for port in all_ports)
    testbench += "\n  );\n\n"

    # Add test logic
    testbench += "  initial begin\n"
    testbench += "    // Initialize inputs\n"
    for name in inputs_with_bits.keys():
        if name not in [extracted_clock]:
            testbench += f"    {name} = 0;\n"
    testbench += "    #10;\n\n"

    # Random Test Cases
    testbench += "    // Random Test Cases\n"
    testbench += "    integer i;\n"
    testbench += "    for (i = 0; i < 5000; i = i + 1) begin\n"
    testbench += "      #10;\n"
    for name, bits in inputs_with_bits.items():
        if name not in [extracted_clock, extracted_reset]:
            testbench += f"      {name} = $random();\n"
    testbench += "    end\n\n"

    testbench += "  end\n"
    testbench += "endmodule"

    return testbench



verilog_file = "binaryCounter.v"
file = open(verilog_file, 'r')
rtl_code = file.read()
rtl_code = remove_comments(rtl_code) # Remove comments from the Verilog code
rtl_code = " ".join(rtl_code.split()) # Remove extra spaces from the Verilog code
module_name = extract_module_name(rtl_code) # Extract the module name from the Verilog code
input_names = extract_input_names(rtl_code) # Extract the input names from the Verilog code
output_names = extract_output_names(rtl_code) # Extract the output names from the Verilog code
reg_names = extract_reg_names(rtl_code) # Extract the reg names from the Verilog code
wire_names = extract_wire_names(rtl_code) # Extract the wire names from the Verilog code
inputs_with_bits = assign_bits_to_signals(input_names) # Assign bit widths to the input signals
output_with_bits = assign_bits_to_signals(output_names) # Assign bit widths to the output signals
reg_with_bits = assign_bits_to_signals(reg_names) # Assign bit widths to the input signals
wire_with_bits = assign_bits_to_signals(wire_names) # Assign bit widths to the output signals
case_conditions = extract_case_conditions(rtl_code)
extracted_continuous_assignments = extract_continuous_assignments(rtl_code)
parsed_ifs = parse_if_statements(rtl_code)
extracted_non_blocking_assignments = extract_non_blocking_assignments(rtl_code)

extracted_always_blocks = extract_always_blocks(rtl_code)
tb_file = "binarytb.v"
tbfile = open(tb_file, "w")
extracted_clock = 'clock'
extracted_reset = 'reset'
testbench_code = write_testbench(module_name, inputs_with_bits, output_with_bits, case_conditions, parsed_ifs,extracted_clock, extracted_reset)
tbfile.write(testbench_code)

# TODO 
# extract_clock(), extract_reset()
# monitoring
# instead #10 make it @(negedge clk)
# reset = 1; or reset = 0;
# directed cases
