// Testbench for multiplexer_4to1
`timescale 1ns / 1ps

module multiplexer_4to1_tb;

  reg [1:0] sel;
  reg [3:0] in0;
  reg [3:0] in1;
  reg [3:0] in2;
  reg [3:0] in3;
  integer i;

  wire [3:0] out;

  multiplexer_4to1 DUT (
    .sel(sel),
    .in0(in0),
    .in1(in1),
    .in2(in2),
    .in3(in3),
    .out(out)
  );

  initial begin


	//Direct Case

		sel = 2'b00;
		in0 = 6;
		in1 = 2;
		in2 = 4;
		in3 = 1;
		#10;


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
      #10;
      sel = $random();
      in0 = $random();
      in1 = $random();
      in2 = $random();
      in3 = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("sel = %b, in0 = %b, in1 = %b, in2 = %b, in3 = %b, out = %b", sel, in0, in1, in2, in3, out);
end
endmodule