    module ShiftRegister(
    input wire clk,
    input wire rst,
    input wire enable,
    input wire [7:0] dataIn,
    output reg [7:0] dataOut
    );

    always @(posedge clk or posedge rst) begin
        if (rst) begin
        dataOut <= 8'b00000000;
        end else if (enable) begin
        // Shift dataIn to the left by two bits
        dataOut <= {dataIn[5:0], 2'b00};
        end
        else begin
            dataOut <= dataIn;
        end
    end

    endmodule
