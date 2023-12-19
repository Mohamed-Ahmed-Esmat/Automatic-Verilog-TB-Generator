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

def extract_bit_width(verilog_code, signal_name):
    pattern = re.compile(r'\b(?:input|output)\s+(reg|wire)?\s*\[([0-9]+)\s*:\s*[0-9]+\]\s+' + re.escape(signal_name) + r'\s*[,; ]')
    match = pattern.search(verilog_code)

    if match:
        return int(match.group(2)) + 1  # Adding 1 to account for zero-based indexing
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
    

verilog_file = "C:/Users/moham/Documents/binaryCounter.v"
file = open(verilog_file, 'r')
rtl_code = file.read()
rtl_code = remove_comments(rtl_code) # Remove comments from the Verilog code
rtl_code = " ".join(rtl_code.split()) # Remove extra spaces from the Verilog code
input_names = extract_input_names(rtl_code) # Extract the input names from the Verilog code
output_names = extract_output_names(rtl_code) # Extract the output names from the Verilog code
inputs_with_bits = assign_bits_to_signals(input_names) # Assign bit widths to the input signals
output_with_bits = assign_bits_to_signals(output_names) # Assign bit widths to the output signals
print(inputs_with_bits)
print(output_with_bits)

