// Testbench for BinaryCounter
`timescale 1ns / 1ps

module BinaryCounter_tb;

  reg clock;
  clock = 0;
  always #5 clock = ~clock;

  reg clock;
  reg reset;
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
    .clock(clock),
    .reset(reset),
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
    reset = 0;
    x = 0;
    y = 0;
    a = 0;
    c = 0;
    d = 0;
    g = 0;
    f = 0;
    b = 0;
    #10;

    // Random Test Cases
    integer i;
    for (i = 0; i < 5000; i = i + 1) begin
      #10;
      x = $random();
      y = $random();
      a = $random();
      c = $random();
      d = $random();
      g = $random();
      f = $random();
      b = $random();
    end

  end

  // Monitoring signals
initial begin
 $monitor("x = %b, y = %b, a = %b, c = %b, d = %b, g = %b, f = %b, b = %b, count = %b, result = %b", x, y, a, c, d, g, f, b, count, result);
end
endmodule