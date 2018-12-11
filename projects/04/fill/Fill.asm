// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(BEGIN)
	@SCREEN
	D=A

	@cursor // this register will carry the current address of pixel we are goin to manipulate
	M=D

(LOOP)
	@KBD // set keyboard register RAM[24576]
	D=M // getting thevalue returned by kbd(0 or non-0)
	
	@BLANK //points to method supposed to make screen white
	D;JEQ // jump to  blank if kbd == 0

	@FILL // points to the method to make screen black 
	0;JMP  //both are working
//TODO: [! figure out difference between them]
	//D;JNE
	
(BLANK)
	@cursor 
	A=M // setting the address ofcursor to the destination
	M=0 //and set it's value to 0 , bcz we should print white
	@NEXT  // method to progress to next step
	0;JMP

(FILL)
	@cursor
	A=M // setting the address ofcursor to the destination
	M=-1 //and set it's value to -1(1111111111111111) , bcz we should print black
	
	@NEXT
	0;JMP
(NEXT)
	@cursor 
	D=M+1 // increase address to where to go by 1
	M=D
	
	@KBD
	D=A-D // such that it doesnt exceed the screen region in memory and overflow happens
	
	@BEGIN
	D;JEQ
	@LOOP
	0;JMP
