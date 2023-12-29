module ShiftRegister (
    input wire clk,         // Clock input
    input wire reset,       // Reset input
    input wire shiftEnable, // Shift enable input
    input wire [3:0] dataIn, // 4-bit data input
    output reg [3:0] dataOut // 4-bit data output
);

    reg [3:0] shiftReg; // 4-bit shift register

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            shiftReg <= 4'b0000; // Reset the shift register to 0
        end else if (shiftEnable) begin
            shiftReg <= {shiftReg[2:0], dataIn[0]}; // Shift dataIn into the shift register
        end
    end

    assign dataOut = shiftReg; // Output the current state of the shift register

endmodule
