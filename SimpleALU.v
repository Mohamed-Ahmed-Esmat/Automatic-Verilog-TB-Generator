module SimpleALU (
    input wire [3:0] operandA, // 4-bit input operand A
    input wire [3:0] operandB, // 4-bit input operand B
    input wire [2:0] aluOp,     // 3-bit ALU operation code
    output reg [3:0] result     // 4-bit ALU output
);

    always @* begin
        case (aluOp)
            3'b000: result = operandA + operandB; // Addition
            3'b001: result = operandA - operandB; // Subtraction
            3'b010: result = operandA & operandB; // Bitwise AND
            3'b011: result = operandA | operandB; // Bitwise OR
            3'b100: result = operandA ^ operandB; // Bitwise XOR
            // Add more cases for additional operations if needed
            default: result = 4'bxxxx; // Output all 1's for undefined operation
        endcase
    end

endmodule


