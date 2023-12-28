// Testbench for BinaryCounter
`timescale 1ns / 1ps

module BinaryCounter_tb;

  reg clk;
  initial clk = 0;
  always #5 clk = ~clk;

  reg clk;
  reg [2:0] rst;
  reg x;
  reg y;
  reg a;
  reg c;
  reg d;
  reg g;
  reg f;
  reg [31:0] b;

  wire [5:0] count;
  wire result;

  BinaryCounter DUT (
    .clk(clk),
    .rst(rst),
    .x(x),
    .y(y),
    .a(a),
    .c(c),
    .d(d),
    .g(g),
    .f(f),
    .b(b),
    .count(count),
    .result(result)
  );

  initial begin
    // Initialize inputs
    clk = 0;
    rst = 0;
    x = 0;
    y = 0;
    a = 0;
    c = 0;
    d = 0;
    g = 0;
    f = 0;
    b = 0;
    #10;

    // Directed Test Cases
    // TODO: Fill in directed test cases

    // Random Test Cases
    integer i;
    for (i = 0; i < 5000; i = i + 1) begin
      #10;
      clk = $random();
      rst = $random();
      x = $random();
      y = $random();
      a = $random();
      c = $random();
      d = $random();
      g = $random();
      f = $random();
      b = $random();
    end

    // Monitor outputs and check against expected values
    // TODO: Implement monitoring and checking logic

  end
endmodule