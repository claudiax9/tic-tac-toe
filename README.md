Iftimoaia Claudia Iuliana 3E1

Tic Tac Toe - B11

Phase 1 — Core board & rules
3×3 board model with players X and O, current-turn tracking
Move application with legality checks (empty cell only)
Win/draw detection (rows, columns, diagonals)
Text rendering helper for multi-line board display
Functional result: A small script can play in the console by applying legal moves, printing the board, and correctly reporting win or draw.

Phase 2 — GUI (Tkinter) interaction
Window with a 3×3 clickable grid; highlight current player
Click-to-place for the human; ignore clicks on occupied cells
Status bar: turn info, end-of-game message
“Play again” button that resets the board
Functional result: User clicks a square to place their symbol, the board updates live, and an end message appears on win/draw with a working reset.

Phase 3 — AI engines & difficulties
AI “random”: choose uniformly among empty cells
AI “best”: optimal move via minimax (or equivalent), with simple tie-breaks
Difficulty selector:
always random
alternate random & best
always best
Functional result: Selecting each difficulty changes AI behavior as specified; best-play AI never loses, alternating mode visibly switches strength every AI turn.

Phase 4 — Match flow & scoring
Track cumulative score across rounds: wins for X, wins for O, draws
After each game: show winner/draw and ask to play again
Scoreboard visible and updated after every match
Functional result: Finishing a game updates the running score and prompts for a new round; repeated matches correctly accumulate and display totals.
