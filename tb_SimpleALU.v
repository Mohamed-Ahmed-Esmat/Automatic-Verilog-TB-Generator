// Testbench for SimpleALU
`timescale 1ns / 1ps

module SimpleALU_tb;

  reg [3:0] operandA;
  reg [3:0] operandB;
  reg [2:0] aluOp;
  integer i;

  wire [3:0] result;

  SimpleALU DUT (
    .operandA(operandA),
    .operandB(operandB),
    .aluOp(aluOp),
    .result(result)
  );

  initial begin


	//Direct Case

		operandA = 14;
		operandB = 4;
		aluOp = 3'b010;
		#10;


    // Random Test Cases
    for (i = 0; i < 5000; i = i + 1) begin
      #10;
      operandA = $random();
      operandB = $random();
      aluOp = $random();
    end

  end

  // Monitoring signals
initial begin
	$monitor("operandA = %b, operandB = %b, aluOp = %b, result = %b", operandA, operandB, aluOp, result);
end
endmodule