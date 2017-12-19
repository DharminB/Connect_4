# connect four board
# common for both players
class Board :

	# === Parameters ===
	# max_col = int
	# max_row = int
	# color1 = character
	# color2 = character
	def __init__(self, max_col, max_row, color1, color2) :
		self.board = []
		self.max_row = max_row
		self.max_col = max_col
		self.color1 = color1
		self.color2 = color2
		self.winner = None
		for i in range(self.max_col) :
			self.board.append([])
			for j in xrange(self.max_row) :
				self.board[i].append("N")


	# called by player object to put their color piece at their desired column
	# returns True if successfully inserted piece at the desired column else False
	# === Parameters ===
	# col_num = int (typically between 0 and max_col)
	# color = string (typically either color1 or color2)
	# === Returns ===
	# Boolean
	def put_piece_at(self, col_num, color) :
		if color == self.color1 :
			color = self.color1
		else :
			color = self.color2

		if col_num in range(self.max_col) :
			if self.board[col_num].count("N") > 0 :
				self.board[col_num][self.board[col_num].index("N")] = color
			else :
				# print "Column", col_num, "Full"
				return False

		else :
			print "Invalid Column"
			return False
		return True

	# printing the state of the board on stdout
	def print_board(self) :
		for row_num in reversed(range(self.max_row)) :
			temp = []
			for col_num in xrange(self.max_col) :
				temp.append(self.board[col_num][row_num])
			s = "|"
			for i in temp :
				if i == "N" :
					s += " |"
				else :
					s += i+"|"
			print s
		print self.max_col*2*"=" + "="
		print "",
		for i in xrange(self.max_col) :
			print i,
		print ""

	# sets the board from an external array
	# === Parameters === 
	# array = 2D array of characters
	def set_board_array(self, array) :
		self.board = array

	# returns the board as a 2D array
	# === Returns ===
	# 2D array of characters
	def get_board_array(self) :
		return self.board

	# get a list of size n starting from "row" and "col" in direction of column
	# if cannot do this then returns empty list
	# === Parameters ===
	# n = int (typically smaller than max_col and max_row)
	# row = int (typically smaller than max_col and max_row)
	# col = int (typically smaller than max_col and max_row)
	# === Returns ===
	# temp = list of characters (size of list = n or 0)
	def get_n_in_col(self, row, col, n) :
		# print "inside get_4_in_col"
		temp = []
		if row > self.max_row - n :
			return temp
		for i in xrange(n) :
			temp.append(self.board[col][row+i])
		return temp

	# get a list of size n starting from "row" and "col" in direction of row
	# if cannot do this then returns empty list
	# === Parameters ===
	# n = int (typically smaller than max_col and max_row)
	# row = int (typically smaller than max_col and max_row)
	# col = int (typically smaller than max_col and max_row)
	# === Returns ===
	# temp = list of characters (size of list = n or 0)
	def get_n_in_row(self, row, col, n) :
		# print "inside get_4_in_row"
		temp = []
		if col > self.max_col - n :
			return temp
		for i in xrange(n) :
			temp.append(self.board[col+i][row])
		return temp			

	# get a list of size n starting from "row" and "col" in direction of other diagonal
	# if cannot do this then returns empty list
	# === Parameters ===
	# n = int (typically smaller than max_col and max_row)
	# row = int (typically smaller than max_col and max_row)
	# col = int (typically smaller than max_col and max_row)
	# === Returns ===
	# temp = list of characters (size of list = n or 0)
	def get_n_in_other_diagonal(self, row, col, n) :
		temp = []
		if col > self.max_col - n or row > self.max_row - n :
			return temp
		for i in xrange(n) :
			temp.append(self.board[col+i][row+i])
		return temp

	# get a list of size n starting from "row" and "col" in direction of main diagonal
	# if cannot do this then returns empty list
	# === Parameters ===
	# n = int (typically smaller than max_col and max_row)
	# row = int (typically smaller than max_col and max_row)
	# col = int (typically smaller than max_col and max_row)
	# === Returns ===
	# temp = list of characters (size of list = n or 0)
	def get_n_in_main_diagonal(self, row, col, n) :
		temp = []
		if col > self.max_col - n or row < n - 1 :
			return temp
		for i in xrange(n) :
			temp.append(self.board[col+i][row-i])
		return temp

	# get a list of arrays (of size n) in every direction starting from everywhere
	# basically returns every possible list of size n that can be taken from self.board
	# === Parameters ===
	# n = int (typically smaller than max_col and max_row)
	# === Returns ===
	# all_n_array = list of (list of characters) (size of list of characters = n or 0)
	def get_all_possible_list_of_size(self, n) :
		all_n_array = []
		for i in xrange(self.max_col) :
			for j in xrange(self.max_row) :
				temp = self.get_n_in_row(j, i, n)
				if temp != [] :
					all_n_array.append(temp)
				temp = self.get_n_in_col(j, i, n)
				if temp != [] :
					all_n_array.append(temp)
				temp = self.get_n_in_other_diagonal(j, i, n)
				if temp != [] :
					all_n_array.append(temp)
				temp = self.get_n_in_main_diagonal(j, i, n)
				if temp != [] :
					all_n_array.append(temp)
		return all_n_array

	# return True if the game is complete and updates winner otherwise returns False
	# === Returns ===
	# Boolean
	def is_game_complete(self) :
		all_4_array = self.get_all_possible_list_of_size(4)
		all_valid_4_array = []
		for i in all_4_array :
			if "N" not in i :
				all_valid_4_array.append(i)
		for i in all_valid_4_array :
			# print i
			if i.count(self.color1) == 4 :
				self.winner = self.color1
				return True
			if i.count(self.color2) == 4 :
				self.winner = self.color2
				return True

		# outcome for draw
		full = True
		for i in self.board :
			if "N" in i :
				full = False
				break
		if full :
			return True

		return False


if __name__ == '__main__':
	print "This file is only for Board class. Make an object of it in your own file."