import re

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
    pattern = re.compile(r'\breg\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,;]|$)')
    matches = pattern.findall(verilog_code)

    return matches

def extract_wire_names(verilog_code):
    # Match wire declarations with or without bit width
    pattern = re.compile(r'\bwire\s*(?:\[[0-9]*:[0-9]*\])?\s*(\w+)\s*(?:[,;]|$)')
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
    
def extract_conditions_from_if(verilog_code):
    conditions = {}

    # Match if statements
    pattern = re.compile(r'\bif\s*\(([^)]+)\)')
    matches = pattern.findall(verilog_code)

    for condition in matches:
        conditions['if'] = conditions.get('if', []) + [condition.strip()]

    return conditions

def extract_conditions_from_case(verilog_code):
    conditions = {}

    # Match case statements
    pattern = re.compile(r'\bcase\s*\(([^)]+)\)')
    matches = pattern.findall(verilog_code)

    for condition in matches:
        conditions['case'] = conditions.get('case', []) + [condition.strip()]

    return conditions

def extract_conditions(verilog_code):
    conditions = {}
    
    # Extract conditions from if statements
    if_conditions = extract_conditions_from_if(verilog_code)
    conditions.update(if_conditions)

    # Extract conditions from case statements
    case_conditions = extract_conditions_from_case(verilog_code)
    conditions.update(case_conditions)

    return conditions

verilog_file = "binaryCounter.v"
file = open(verilog_file, 'r')
rtl_code = file.read()
rtl_code = remove_comments(rtl_code) # Remove comments from the Verilog code
rtl_code = " ".join(rtl_code.split()) # Remove extra spaces from the Verilog code
input_names = extract_input_names(rtl_code) # Extract the input names from the Verilog code
output_names = extract_output_names(rtl_code) # Extract the output names from the Verilog code
reg_names = extract_reg_names(rtl_code) # Extract the reg names from the Verilog code
wire_names = extract_wire_names(rtl_code) # Extract the wire names from the Verilog code
inputs_with_bits = assign_bits_to_signals(input_names) # Assign bit widths to the input signals
output_with_bits = assign_bits_to_signals(output_names) # Assign bit widths to the output signals
reg_with_bits = assign_bits_to_signals(reg_names) # Assign bit widths to the input signals
wire_with_bits = assign_bits_to_signals(wire_names) # Assign bit widths to the output signals
print(inputs_with_bits)
print(output_with_bits)
print(reg_with_bits)
print(wire_with_bits)

parsed_conditions = extract_conditions(rtl_code)
print("Parsed Conditions:", parsed_conditions)