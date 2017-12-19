from copy import deepcopy
import time
import random
# importing Board.py file (has to be in the same folder) 
import Board

# object for a player to play the connect four game
# asks the player to input a number to make moves in the game
# can be used to play against bot(for debugging) or another player(for fun) 
class Connect_Four_Player :

	# === Parameter ===
	# board = Board object from Board.py
	# color = character
	def __init__(self, board, color) :
		self.board = board
		self.color = color

	# asks user to input a number, which will be column number where the user wants to 
	# insert his/her piece, if piece cannot be inserted at that column number then asks the user for 
	# column number again and again until valid number is provided 
	# Also returns the column number (for server client application, not used here)
	# === Returns ===
	# col = int
	def make_a_move(self) :
		print "Player", self.color ,"Move"
		col = input("Enter column Number : ")
		while not self.board.put_piece_at(col, self.color) :
			col = input("Enter column Number : ")
		return col
		

# object which can make a decision of which move to make in connect four game
# uses minimax algorithm to make decisions
# time taken to arrive at a decision varies on the "max_depth"
class Connect_Four_Bot :

	# === Parameters ===
	# board = Board object from Board.py
	# color = character
	# max_depth = int
	# alpha_beta = Boolean
	def __init__(self, board, color, max_depth, alpha_beta) :
		self.board = board
		self.color = color
		self.max_depth = max_depth
		self.alpha_beta = alpha_beta
		self.node_explored = 0
		if self.board.color1 == self.color :
			self.opponent_color = self.board.color2
		else :
			self.opponent_color = self.board.color1
		# print self.opponent_color

	# decides which column to put it's piece according to minimax algorithm
	# or minimax with alpha beta pruning (depends on self.alpha_beta)
	# Also returns the column number (for server client application, not used here)
	# === Returns ===
	# col = int
	def make_a_move(self) :
		# print "inside make_a_move"
		start = time.time()

		self.node_explored = 0
		if self.alpha_beta :
			col = self.minimax_with_alpha_beta(self.board, self.color, -1000, 1000, True, 0)
		else :
			col = self.minimax(self.board, self.color, True, 0)
		
		
		end = time.time()
		print "Time taken by Bot to think =", end - start
		print "Nodes Explored =", self.node_explored
		
		self.board.put_piece_at(col, self.color)
		return col

	# Recursive function which implements minimax algorithm with alpha beta pruning
	# if index_needed is given True, then returns the number of column that is best,
	# otherwise returns the utility value of state itself
	# The depth of the recursion is dependent on the self.max_depth
	# at maximum depth, it returns a heuristic value
	# === Parameter ===
	# state = Board object from Board.py
	# color = character
	# alpha = int
	# beta = int
	# index_needed = Boolean
	# depth = int
	# === Returns ===
	# int
	def minimax_with_alpha_beta(self, state, color, alpha, beta, index_needed, depth) :
		self.node_explored += 1

		# return if terminal state
		if state.is_game_complete() :
			if state.winner == self.color :
				return 1000*(self.max_depth - depth)
			elif state.winner is None :
				return 0
			else :
				return -1000*(self.max_depth - depth)
		
		# return if depth exceeded
		if depth > self.max_depth :
			return self.heuristic(state)

		# initialise values
		children_values = []
		children_index = None
		v = 0
		if color == self.color :
			v = -10000
		else :
			v = 10000

		# determine next players color
		next_color = self.color
		if color == self.color :
			next_color = self.opponent_color

		# iterate through all possible actions
		for i in range(state.max_col) :
			child = deepcopy(state)
			
			# if column is full, don't call recursive function
			if not child.put_piece_at(i, color) :
				continue
			
			# call recursive function with newly created board state and increased depth
			answer_from_child = self.minimax_with_alpha_beta(child, next_color, alpha, beta, False, depth+1)

			# append the answer from child only if index is needed
			if index_needed :
				children_values.append(answer_from_child)

			# determine if its max's move or min's move
			# update v, alpha, beta and chilren_index accordingly 
			# if better solution already exists in the tree,
			# return value according to "index_needed"
			if color == self.color :
				if v < answer_from_child :
					v = answer_from_child
					children_index = i
				if v >= beta :
					if index_needed :
						print "Bot's utility", children_values
						return children_index
					else :
						return v
				alpha = max(alpha, v)
			else :
				if v > answer_from_child :
					v = answer_from_child
					children_index = i	
				if v <= alpha :
					if index_needed :
						print "Bot's utility", children_values
						return children_index
					else :
						return v
				beta = min(beta, v)
		
		
		# determine if the index of the action is needed or not and return values accordingly
		if index_needed :
			print "Bot's utility", children_values
			return children_index
		else :
			return v



	# Recursive function which implements minimax algorithm
	# if index_needed is given True, then returns the number of column that that is best,
	# otherwise returns the value itself
	# The depth of the recursion is dependent on the self.max_depth
	# at maximum depth, it returns a heuristic value
	# === Parameter ===
	# state = Board object from Board.py
	# color = character
	# index_needed = Boolean
	# depth = int
	# === Returns ===
	# int
	def minimax(self, state, color, index_needed, depth) :
		self.node_explored += 1

		# return if terminal state
		if state.is_game_complete() :
			if state.winner == self.color :
				return 1000*(self.max_depth - depth)
			elif state.winner is None :
				return 0
			else :
				return -1000*(self.max_depth - depth)
		
		# return if depth exceeded
		if depth > self.max_depth :
			return self.heuristic(state)

		# initialise values
		children_values = []
		children_index = []

		# determine next players color
		next_color = self.color
		if color == self.color :
			next_color = self.opponent_color

		# iterate through all possible actions
		for i in range(state.max_col) :
			child = deepcopy(state)
			
			# if column is full, don't call recursive function
			if not child.put_piece_at(i, color) :
				continue
			
			# call recursive function with newly created board state and increased depth
			answer_from_child = self.minimax(child, next_color, False, depth+1)
			
			# save the value from child
			children_values.append(answer_from_child)
			children_index.append(i)
		
		# determine if its max's move or min's move and initialise "desired_value" accordingly
		if color == self.color :
			desired_value = max(children_values)
		else :
			desired_value =  min(children_values)
		
		# determine if the index of the action is needed or not and return value accordingly
		if index_needed :
			print "Bot's utility", children_values
			return children_index[children_values.index(desired_value)]
		else :
			return desired_value

	# Returns a heuristic value depending on the "state" of the game
	# gets all possible list of size 4 from state using a function in Board class
	# assigns points to both players for certain lists (1 or 2 or 3 in a row)
	# substracts the points of opponent from our point and returns the value
	# === Parameter === 
	# state = Board object from Board.py
	# === Returns ===
	# int
	def heuristic(self, state) :
		all_4_array = state.get_all_possible_list_of_size(4)
		opponent_point = 0
		our_point = 0
		for i in all_4_array :
			# print i
			if i.count(self.opponent_color) == 3 and i.count("N") == 1 :
				opponent_point += 200
			elif i.count(self.color) == 3 and i.count("N") == 1 :
				our_point += 100
			elif i.count(self.opponent_color) == 2 and i.count("N") == 2 :
				opponent_point += 20
			elif i.count(self.color) == 2 and i.count("N") == 2 :
				our_point += 10
			elif i.count(self.opponent_color) == 1 and i.count("N") == 3 :
				opponent_point += 2
			elif i.count(self.color) == 1 and i.count("N") == 3 :
				our_point += 1
			

		# print our_point, opponent_point
		return our_point - opponent_point
		



# ===================== #
# ======= MAIN ======== #
# ===================== #
if __name__ == '__main__':

	# sign for the color of the two players, can be any character 
	red = "x"
	blue = "o"

	# number of columns and rows in the connect 4 board
	max_col = 5
	max_row = 4

	# Depth till which bot should build tree for searching
	max_depth = 5

	# Should bot use alpha-beta pruning or not
	alpha_beta = True

	print "You can have default settings where"
	print "  Columns = 5 \n  Rows = 4 \n  Depth till which bot should search = 5 \n  and use Alpha-Beta pruning"
	print "or you can choose your own settings\n"

	choice = raw_input("Do you want Default settings ? [y/n] ")
	if choice != "y" :
		max_col = input("Enter number of columns(width) for Connect 4 board : ")
		max_row = input("Enter number of rows(height) for Connect 4 board : ")
		max_depth = input("Enter depth till which bot should search (< 10 please): ")
		a_b_choice = raw_input("Do you want the bot to use Alpha-Beta pruning ? [y/n] ")
		alpha_beta = a_b_choice == "y"
		
	# initialising the board
	board = Board.Board(max_col, max_row, red, blue)
	
	# initialising the players
	player_1 = Connect_Four_Bot(board, blue, max_depth, alpha_beta)
	player_2 = Connect_Four_Player(board, red)
	# player_2 = Connect_Four_Bot(board, red, max_depth, alpha_beta)
	
	# print board
	board.print_board()
	
	# take turns to ask for the player's move untill the game is complete and print winner
	player_1_turn = True
	while not board.is_game_complete() :
		if player_1_turn :
			player_1.make_a_move()
			player_1.heuristic(board)
		else :
			player_2.make_a_move()
		player_1_turn = not player_1_turn
		board.print_board()
		print "="*20
	print "Winner =",board.winner
			