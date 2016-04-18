A simple compiler for [Whitespace][], for compiling from something that looks vaguely like assembly language into Whitespace.

Instructions are as follows, one per line:

*   Stack manipulation:
    *   `PUSH <num>`: Push `<num>` onto the stack.
    *   `DUPE`: Duplicate the top item on the stack.
    *   `SWAP`: Swap the top two items on the stack.
    *   `DROP`: Discard the top item on the stack.
*   Arithmetic:  Arithmetic commands operate on the top two items on the stack, and replace them with the result of the operation.  The first item pushed is considered to be _left_ of the operator.
    *   `ADD`: Addition.
    *   `SUB`: Subtraction.
    *   `MUL`: Multiplication.
    *   `DIV`: Integer division.
    *   `MOD`: Modulo.
*   Heap access: Heap access commands look at the stack to find the address of items to be stored or retrieved.  To store an item, push the address then the value and run the store command. To retrieve an item, push the address and run the retrieve command, which will place the value stored in the location at the top of the stack.
    *   `STORE`: Store.
    *   `RETRV`: Retrieve.
*   Flow control:
    *   `<label>:` or `LABEL <label>`: Mark a location in the program.
    *   `GOSUB <label>`: Call a subroutine.
    *   `JMP <label>`: Jump unconditionally to a label.
    *   `JEZ <label>`: Jump to a label if the top of the stack is zero.
    *   `JLZ <label>`: Jump to a label if the top of the stack is negative.
    *   `RETURN`: End a subroutine and transfer control back to the caller.
    *   `END`: End the program.
*   I/O:
    *   `PUTC`: Output the character at the top of the stack.
    *   `PUTN`: Output the number at the top of the stack.
    *   `GETC`: Read a character and place it in the location given by the top of the stack.
    *   `GETN`: Read a number and place it in the location given by the top of the stack.

Labels can be arbitrary strings of alphanumeric characters, plus `-` and `_`; the compiler will automatically convert them to Whitespace labels.  Numbers should be decimal, optionally preceded by `-`.

Thus the annotated example given at the bottom of [the Whitespace homepage][Whitespace] is as follows:

    PUSH 1      # Put a 1 on the stack
    LABEL loop  # Set a Label at this point
    DUPE        # Duplicate the top stack item
    PUTN        # Output the current value
    PUSH 10     # Put 10 (newline) on the stack...
    PUTC        # ...and output the newline
    PUSH 1      # Put a 1 on the stack
    ADD         # Addition. This increments our current value.
    DUPE        # Duplicate the value so we can test it
    PUSH 11     # Push 11 onto the stack
    SUB         # Subtraction. So if we've reached the end, we have a zero on the stack.
    JEZ end     # If we have a zero, jump to the end
    JMP loop    # Jump to the start
    LABEL end   # Set the end label
    DROP        # Discard our accumulator, to be tidy
    END         # Finish

[Whitespace]: http://compsoc.dur.ac.uk/whitespace/tutorial.html
