## Ideas for implementation:
- Grand Prix cipher for grids from 2x2 to 36x36
- Caesar cipher with shift by ASCII table (symbols 33-126) and by alphabet
- Mathematical puzzle about remainders
- Modified DNA cipher (parser for decode and encode)

## _v.0.0.3_
## Features

- Menu Ciphers with submenus Encode and Decode (same functionality for now)
- Window for Help (call F1)
- Improved Ciphers tabs with closure and numbering
- Grand Prix and Caesar ciphers window with almost full functionality
  - Number of words/Shift input validation (also for empty input)
  - Text with words for dictionary input validation
  - Re-encode plain text ability

## _v.0.1.0_
## Implementation plan

* [x] Separate functionality to Encode and Decode
* [ ] Pop-up menu for left-clicking on text widget to save to file
* [x] Add ability to select modes to Caesar: alphabet and ASCII
* [ ] Add information in window Help
* [ ] Add tab scrollbar when tabs go off screen
* [x] Add autocomplete entry in choice window
* [x] BUGFIX: When opening multiple tabs with the same functionality, correct input occurs only in the last created one
* [x] BUGFIX: When clicking the cross on a tab and releasing the mouse elsewhere, the cross begin to light up red instead of yellow when hovering

