import argparse
import time

################################################################################
# ARGUMENTS #

description = """
--------------------------------------------------------------------------------
TicTacToe: Board game implemented in Python2.7
AI is implemented with Minimax algorithm and optimised with alpha-beta pruning.

Available game modes (-m, --mode):
	0: Human vs Human
	1: Human vs AI (Default)
	2: AI vs AI

Level of complexity (-l, --level):
	0: Easy
	1. Hard (Default)
--------------------------------------------------------------------------------
"""
parser = argparse.ArgumentParser(description)

# Optional Arguments

# Mode
parser.add_argument("-m", "--mode", help="Game mode",  type=int, default=1)

# Level
parser.add_argument("-l", "--level", help="Level of complexity", type=int, default=1)

################################################################################

##############################################################################
#
# Player
# Could be a human or an AI
#
##############################################################################

class Player(object):
	def __init__(self, symbol=None, ai=False):
		super(Player, self).__init__()
		self.__symbol = symbol
		self.__ai = ai

	@property
	def symbol(self):
		return self.__symbol

	def is_ai(self):
		return self.__ai

	def enable_ai(self):
		self.__ai = True

	def disable_ai(self):
		self.__ai = False

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "{0} Player: '{1}'".format("AI" if self.__ai else "Human",
			self.__symbol)

##############################################################################
#
# Tic Tac Toe
#
##############################################################################

class TicTacToe(object):

	# Board setup
	BOARD_SIZE = 9
	DEFAULT = " "

	# Game states
	WON = 2
	TIE = 1

	GAME_OVER = 0
	INVALID_MOVE = -1

	# Level of complexity
	EASY_MODE = "Easy"
	HARD_MODE = "Hard"
	MODES = (EASY_MODE, HARD_MODE)

	# AI
	WIN_SCORE = 10
	TIE_SCORE = 0
	LOST_SCORE = -10
	MAX = 1000
	MIN = -1000

	def __init__(self, player1, player2, level=None):
		super(TicTacToe, self).__init__()
		self.__players = (player1, player2)
		self.__level = level or TicTacToe.EASY_MODE

		self.__board = None
		self.__current_index = None
		self.__game_over = False

		# AI related
		self.__maximizing_player = None
		self.__minimizing_player = None
		self.__ai_method_to_call = None

		self.initialize()

	##########################################################################
	# Properties
	##########################################################################
	@property
	def players(self):
		return self.__players

	@property
	def current_player(self):
		return self.__players[self.__current_index]	

	##########################################################################
	# Utils
	##########################################################################
	def initialize(self):
		""" Initialize the board and the game
		"""
		self.__populate_board()
		self.__current_index = 0
		self.__game_over = False

		self.__maximizing_player = None
		self.__minimizing_player = None

		self.__ai_method_to_call = self.__get_next_available_slot
		if self.__level == TicTacToe.HARD_MODE:
			self.__ai_method_to_call = self.__use_minimax

	def play(self, index):
		""" Mark the index with the current player's symbol

		Args:
			index int : Index in the board to play.

		Returns:
			int : State of the game.
		"""
		if self.__game_over:
			print "Game over. Please reset the board."
			return TicTacToe.INVALID_MOVE

		if index < 0 or index > 8:
			print "Invalid slot. PLease pick a value between 0-8"
			return TicTacToe.INVALID_MOVE

		if not self.__is_valid_slot(index):
			print "Slot:{0} has already been played.".format(index)
			return TicTacToe.INVALID_MOVE

		self.__board[index] = self.current_player.symbol
		self.pprint()

		# Check if the game is over
		result = self.is_game_over()

		if not result:
			self.__toggle_current_player()
			return 1

		# Game over
		self.__game_over = True
		print "#"*60
		if result == TicTacToe.TIE:
			print "# Game Tied!!"
		else:
			print "# {0} won the game".format(self.current_player)
		print "#"*60

		return TicTacToe.GAME_OVER

	def get_best_move(self):
		""" Get the next best move in the game.

		The alogrithm to use to get this best move is based
		on the mode of this game. If it is set to easy, call
		the simple_ai method, else call the minimax method
		"""
		return self.__ai_method_to_call()

	def is_game_over(self, board=None):
		""" Check if the game has been won or tied

		Args:
			board list: Current state of the board.
						Using AI, it passes different combination
						of boards to this method to compute the
						output. So, if a board isn't passed in,
						assume the instance board.

		Returns:
			int or None
		"""
		if board is None:
			board = self.__board

		def _won(cells):
			if len(set(cells)) == 1 and cells[0] != TicTacToe.DEFAULT:
				return cells[0]
			return None

		# check rows
		for i in range(0,TicTacToe.BOARD_SIZE,3):
			if _won(board[i:i+3]) is not None:
				return TicTacToe.WON

		# check col
		for i in range(3):
			if _won((board[i],
					 board[i+3],
					 board[i+6])) is not None:
				return TicTacToe.WON

		# check diagonals
		if _won((board[0],
				 board[4],
				 board[8])) is not None:
			return TicTacToe.WON
		elif _won((board[2],
				   board[4], 
				   board[6])) is not None:
			return TicTacToe.WON

		# Check if this is a tie
		if not self.__get_available_slots(board):
			return TicTacToe.TIE

		return 0

	def reset(self):
		""" Reset the board
		"""
		self.initialize()

	##########################################################################
	# Utils
	##########################################################################
	def pprint(self, board=None, depth=0):
		if board == None:
			board = self.__board

		for i in range(0, TicTacToe.BOARD_SIZE, 3):
			print "\t"*depth + "|{0},{1},{2}|".format(*board[i:i+3])
		print '\n'

	##########################################################################
	# Privates
	##########################################################################
	def __populate_board(self):
		self.__board = [TicTacToe.DEFAULT for i in range(TicTacToe.BOARD_SIZE)]

	def __toggle_current_player(self):
		self.__current_index = self.__get_next_player_index()

	def __get_next_player_index(self):
		return (self.__current_index + 1) % len(self.__players)

	def __get_available_slots(self, board=None):
		""" Get the available slots that could be played
		"""
		if board is None:
			board = self.__board
		return [i for i in range(TicTacToe.BOARD_SIZE) if board[i] == TicTacToe.DEFAULT]

	def __is_valid_slot(self, index):
		return self.__board[index] == TicTacToe.DEFAULT

	##########################################################################
	# Ai
	##########################################################################
	def __get_copy(self):
		return [i for i in self.__board]

	def __get_next_available_slot(self):
		""" Simple AI. Plays the first available slot
		"""
		return self.__get_available_slots()[0]

	def __use_minimax(self):
		""" Use minimax algo to compute the next best move.
		"""		
		self.__maximizing_player = self.current_player
		self.__minimizing_player = self.__players[self.__get_next_player_index()]

		# Take a snapshot of the board
		board = self.__get_copy()

		# Call minimax
		st = time.time()

		result = self.__minimax(board, self.__maximizing_player,
			TicTacToe.MIN, TicTacToe.MAX)

		index = result["index"]
		print "Best move is {0}. Found in: {1}s".format(index, time.time()-st)
		return index

	def __minimax(self, board, player, alpha, beta):
		""" AI uses minimax algorithm with alpha-beta pruning to work out the
		best possible move.

		Its a recursive method.
		"""
		# Get all the available slots in the board.
		avail_slots = self.__get_available_slots(board)

		# check if the game is over
		game_result = self.is_game_over(board)

		# The result is checked before the player has played his game. So the
		# result belongs to the pervious player. If the current player is the
		# maximizing one, the game has been won by the minimizing player. So
		# send a negative score to let the maximizing player to know he has
		# last the game.
		if game_result == TicTacToe.WON:
			score = TicTacToe.LOST_SCORE if player == self.__maximizing_player \
				else TicTacToe.WIN_SCORE
			return {"score" : score}
		elif game_result == TicTacToe.TIE:
			return {"score" : TicTacToe.TIE_SCORE}

		best_move = None
		best_score = TicTacToe.MIN if player == self.__maximizing_player \
				else TicTacToe.MAX

		# Lopp through the slots
		for i in avail_slots:
			board[i] = player.symbol

			if player == self.__maximizing_player:
				result = self.__minimax(board, self.__minimizing_player,
					alpha, beta)

				if result["score"] > best_score:
					best_score = result["score"]
					best_move = {"index" : i, "score" : best_score}

				alpha = max(alpha, best_score)
				board[i] = TicTacToe.DEFAULT

				# Alpha beta pruning
				if beta <= alpha:
					break
			else:
				result = self.__minimax(board, self.__maximizing_player,
					alpha, beta)

				if result["score"] < best_score:
					best_score = result["score"]
					best_move = {"index" : i, "score" : best_score}

				beta = min(beta, best_score)
				board[i] = TicTacToe.DEFAULT

				# Alpha beta pruning
				if beta <= alpha:
					break

		return best_move

def main():
	args = parser.parse_args()

	mode_txt = "Human vs AI"
	player_ai = (False, True) # Human vs AI
	if args.mode == 0:
		mode_txt = "Human vs Human"
		player_ai = (False, False) # Human vs Human
	elif args.mode == 2:
		mode_txt = "AI vs AI"
		player_ai = (True, True) # AI vs AI

	# Initialize players
	player1 = Player("O", ai=player_ai[0])
	player2 = Player("X", ai=player_ai[1])

	# Set the level
	level = TicTacToe.HARD_MODE if args.level == 1 else TicTacToe.EASY_MODE

	print "-"*60
	print "Tic Tac Toe"
	print "Game mode: {0}".format(mode_txt)
	print "Level of complexity: {0}".format(level)
	print "-"*60

	a = TicTacToe(player1, player2, level)
	a.pprint()

	##########################################################################
	# GamePlay
	##########################################################################
	print "#"*60
	print "# GamePlay"
	print "#"*60

	while True:
		if not a.current_player.is_ai():
			index = raw_input("{0}, pick your cell: ".format(a.current_player))
		else:
			print "{0}s turn".format(a.current_player)
			index = a.get_best_move()

		result = a.play(int(index))

		if result == a.GAME_OVER:
			break

	print "Thanks for playing."

if __name__ == '__main__':
	main()