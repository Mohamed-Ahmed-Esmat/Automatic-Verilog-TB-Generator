module SimpleCounter (
    input wire clk,      // Clock input
    input wire reset,    // Reset input
    output reg [3:0] count // 4-bit counter output
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            count <= 4'b0000; // Reset the counter to 0
        end else begin
            count <= count + 1; // Increment the counter on each rising edge of the clock
        end
    end

endmodule
