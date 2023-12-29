// Testbench for SimpleCounter
`timescale 1ns / 1ps

module SimpleCounter_tb;

  reg clk;
  initial clk = 0;
  always #5 clk = ~clk;

  reg reset;
  integer i;

  wire [3:0] count;

  SimpleCounter DUT (
    .clk(clk),
    .reset(reset),
    .count(count)
  );

  initial begin
  // Initialize inputs
    reset = 1;
		@(negedge clk);
  // Unactivating reset
    reset = 0;


	//Direct Case

		@(negedge clk);


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
		@(negedge clk);
    end

  end

  // Monitoring signals
initial begin
	$monitor("count = %b", count);
end
endmodule