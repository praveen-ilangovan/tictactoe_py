# TicTacToe

Board game implemented in Python2.7. AI is implemented with Minimax algorithm and optimised with alpha-beta pruning.

## Available game modes (-m, --mode):
	0: Human vs Human
	1: Human vs AI (Default)
	2: AI vs AI
## Level of complexity (-l, --level):
	0: Easy
	1. Hard (Default)

### Depth
Minimax algorithm has been updated to use depth as a factor to pick the best possible outcome.  
Consider the following test case  
|O,O,X|  
|_,X,_|  
|_,O,_|  
Although playing the slot 6 gives the AI an immediate victory, since it picks the first best outcome, it ignores that option and
instead goes for the slot 3. This extends the game to one additional move. By letting the function to take the depth into consideration,
this scenario could be avoided. The winning or the losing score is divided by the depth before returning it to the caller. Slot 6 would
return a score of 10 while slot 3 would return 3.33 and so AI would pick the slot 6 and wins the game straight-away.
