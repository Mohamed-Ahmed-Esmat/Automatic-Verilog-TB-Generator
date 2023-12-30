// Testbench for ShiftRegister
`timescale 1ns / 1ps

module ShiftRegister_tb;

  reg clk;
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


	//Direct Case

		clk = 0;
		reset = 1;
		shiftEnable = 1;
		enable = 1;
		dataIn = 32;
		#10;


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
      #10;
      clk = $random();
      reset = $random();
      shiftEnable = $random();
      enable = $random();
      dataIn = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("clk = %b, reset = %b, shiftEnable = %b, enable = %b, dataIn = %b, dataOut = %b", clk, reset, shiftEnable, enable, dataIn, dataOut);
end
endmodule