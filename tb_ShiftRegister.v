// Testbench for ShiftRegister
`timescale 1ns / 1ps

module ShiftRegister_tb;

  reg clk;
  initial clk = 0;
  always #5 clk = ~clk;

  reg rst;
  reg enable;
  reg [7:0] dataIn;
  integer i;

  wire [7:0] dataOut;

  ShiftRegister DUT (
    .clk(clk),
    .rst(rst),
    .enable(enable),
    .dataIn(dataIn),
    .dataOut(dataOut)
  );

  initial begin
  // Initialize inputs
    rst = 1;
    enable = 0;
    dataIn = 0;
		@(negedge clk);
  // Unactivating reset
    rst = 0;


	//Direct Case

		enable = 1;
		dataIn = 30;
		@(negedge clk);


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
		@(negedge clk);
      enable = $random();
      dataIn = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("enable = %b, dataIn = %b, dataOut = %b", enable, dataIn, dataOut);
end
endmodule