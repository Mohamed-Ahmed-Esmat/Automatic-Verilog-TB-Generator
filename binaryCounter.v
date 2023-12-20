module BinaryCounter(
    input clk,   // Clock input
    input [2:0] rst,   // Reset input
    input x,
    input y,
    input wire [31:0] b,
    output reg [5:0] count  // 4-bit binary counter output
);

    // Define a 4-bit register to hold the count
    always @(posedge clk or posedge rst)
    begin
        if (rst)  // Reset condition
            count <= 4'b0000;
        else      // Increment on each rising edge of the clock
            count <= count + 1;
    ends

endmodule
