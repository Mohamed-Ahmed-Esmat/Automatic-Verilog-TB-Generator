// Testbench for ShiftRegister
`timescale 1ns / 1ps

module ShiftRegister_tb;

  reg clk;
  initial clk = 0;
  always #5 clk = ~clk;

  reg reset;
  reg shiftEnable;
  reg enable;
  reg [5:0] dataIn;
  integer i;

  wire [5:0] dataOut;

  ShiftRegister DUT (
    .clk(clk),
    .reset(reset),
    .shiftEnable(shiftEnable),
    .enable(enable),
    .dataIn(dataIn),
    .dataOut(dataOut)
  );

  initial begin
  // Initialize inputs
    reset = 1;
    shiftEnable = 0;
    enable = 0;
    dataIn = 0;
		@(negedge clk);
  // Unactivating reset
    reset = 0;


	//Direct Case

		shiftEnable = 1;
		enable = 1;
		dataIn = 49;
		@(negedge clk);


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
		@(negedge clk);
      shiftEnable = $random();
      enable = $random();
      dataIn = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("shiftEnable = %b, enable = %b, dataIn = %b, dataOut = %b", shiftEnable, enable, dataIn, dataOut);
end
endmodule