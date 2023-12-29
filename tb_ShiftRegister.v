// Testbench for ShiftRegister
`timescale 1ns / 1ps

module ShiftRegister_tb;

  reg clk;
  initial clk = 0;
  always #5 clk = ~clk;

  reg reset;
  reg shiftEnable;
  reg [3:0] dataIn;
  integer i;

  wire [3:0] dataOut;

  ShiftRegister DUT (
    .clk(clk),
    .reset(reset),
    .shiftEnable(shiftEnable),
    .dataIn(dataIn),
    .dataOut(dataOut)
  );

  initial begin
  // Initialize inputs
    reset = 1;
    shiftEnable = 0;
    dataIn = 0;
		@(negedge clk);
  // Unactivating reset
    reset = 0;


	//Direct Case

		shiftEnable = 1;
		dataIn = 6;
		@(negedge clk);


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
		@(negedge clk);
      shiftEnable = $random();
      dataIn = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("shiftEnable = %b, dataIn = %b, dataOut = %b", shiftEnable, dataIn, dataOut);
end
endmodule