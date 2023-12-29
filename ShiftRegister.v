module ShiftRegister (
    input wire clk,         // Clock input
    input wire reset,       // Reset input
    input wire shiftEnable, // Shift enable input
    input wire enable,      // Enable input for shifting left by 2
    input wire [5:0] dataIn, // 6-bit data input
    output reg [5:0] dataOut // 6-bit data output
);

    reg [5:0] shiftReg; // 6-bit shift register

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            shiftReg <= 6'b000000; // Reset the shift register to 0
        end else if (shiftEnable) begin
            if (enable) begin
                shiftReg <= {shiftReg[3:0], dataIn[1:0]}; // Shift dataIn left by 2 when enabled
            end else begin
                shiftReg <= {shiftReg[4:0], dataIn[0]}; // Shift dataIn into the shift register
            end
        end
    end

    assign dataOut = shiftReg; // Output the current state of the shift register

endmodule
