import abc
import sys

class Piece(abc.ABC):
    def __init__(self, color, board, position):
        """
        Represents a piece on the board.

        Parameters
        ----------
        color: str
            Either 'w' or 'b' for white or black pieces, respectively.
        board: Board
            The board the piece is on.
        position: tuple
            The position of the piece on the board.
        """
        assert color in ('w', 'b')
        self.color = color
        self.board = board
        self.position = position

    @abc.abstractmethod
    def next(self):
        """
        Returns a list of boards that result from the piece moving to a new possible position.

        Returns
        -------
        boards: list of Board
            The new boards resulting from the piece moving.
        """
        return []

class Bishop(Piece):
    def next(self):
        boards = []
        x, y = self.position
        moves = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in moves:
            for i in range(1, 8):
                new_x, new_y = x + i * dx, y + i * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    pos = (new_x, new_y)
                    piece_at_pos = self.board.board.get(pos)
                    if piece_at_pos is None:
                        board_new = self.board.copy()
                        board_new.board[pos] = Bishop(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                    elif piece_at_pos.color != self.color:
                        board_new = self.board.copy()
                        board_new.board[pos] = Bishop(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                        break
                    else:
                        break
                else:
                    break
        return boards

class Flinger(Piece):
    def next(self):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        boards = []
        x, y = self.position

        # Regular moves (like a king, to empty squares only)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board.board.get((nx, ny)) is None:
                board_new = self.board.copy()
                board_new.board[(nx, ny)] = Flinger(self.color, board_new, (nx, ny))
                del board_new.board[self.position]
                boards.append(board_new)

        # Flinging moves (limit to 1 square for pawns)
        for dx, dy in moves:
            x_adj, y_adj = x + dx, y + dy
            if 0 <= x_adj < 8 and 0 <= y_adj < 8:
                adjacent_piece = self.board.board.get((x_adj, y_adj))
                if adjacent_piece and adjacent_piece.color == self.color:
                    x_sling, y_sling = x_adj + dx, y_adj + dy
                    if 0 <= x_sling < 8 and 0 <= y_sling < 8:
                        target = self.board.board.get((x_sling, y_sling))
                        if target is None:
                            # Land on an empty square (limit pawn flinging to 1 square)
                            board_new = self.board.copy()
                            if isinstance(adjacent_piece, Peon) and abs(x_sling - x_adj) + abs(y_sling - y_adj) > 1:
                                continue  # Skip if pawn flinged more than 1 square
                            board_new.board[(x_sling, y_sling)] = type(adjacent_piece)(adjacent_piece.color, board_new, (x_sling, y_sling))
                            del board_new.board[(x_adj, y_adj)]
                            boards.append(board_new)
                        elif target.color != self.color and target.__class__.__name__ != "King":
                            # Capture an opposing piece (not a King) and destroy the flung piece
                            board_new = self.board.copy()
                            del board_new.board[(x_sling, y_sling)]
                            del board_new.board[(x_adj, y_adj)]
                            boards.append(board_new)
        return boards


class Cannon(Piece):
    def next(self):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        boards = []
        x, y = self.position

        # Regular moves
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board.board.get((nx, ny)) is None:
                board_new = self.board.copy()
                board_new.board[(nx, ny)] = Cannon(self.color, board_new, (nx, ny))
                del board_new.board[self.position]
                boards.append(board_new)

        # Diagonal attack
        moves_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in moves_diag:
            pieces_hit = []
            nx, ny = x, y
            while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                nx, ny = nx + dx, ny + dy
                target = self.board.board.get((nx, ny))
                if target:
                    pieces_hit.append((nx, ny))
            if pieces_hit:
                board_new = self.board.copy()
                for px, py in pieces_hit:
                    del board_new.board[(px, py)]
                boards.append(board_new)
        return boards

class King(Piece):
    def next(self):
        boards = []
        x, y = self.position
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in possible_moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                pos = (new_x, new_y)
                piece_at_pos = self.board.board.get(pos)
                if piece_at_pos is None or piece_at_pos.color != self.color:
                    board_new = self.board.copy()
                    board_new.board[pos] = King(self.color, board_new, pos)
                    del board_new.board[self.position]
                    boards.append(board_new)
        return boards

class Knight(Piece):
    def next(self):
        boards = []
        x, y = self.position
        possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in possible_moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                pos = (new_x, new_y)
                piece_at_pos = self.board.board.get(pos)
                if piece_at_pos is None or piece_at_pos.color != self.color:
                    board_new = self.board.copy()
                    board_new.board[pos] = Knight(self.color, board_new, pos)
                    del board_new.board[self.position]
                    boards.append(board_new)
        return boards

class Peon(Piece):
    def next(self):
        boards = []
        x, y = self.position
        move = 1 if self.color == 'w' else -1

        # Forward one square
        new_y = y + move
        if 0 <= new_y < 8 and self.board.board.get((x, new_y)) is None:
            board_new = self.board.copy()
            if new_y == (7 if self.color == 'w' else 0):
                board_new.board[(x, new_y)] = Zombie(self.color, board_new, (x, new_y))
            else:
                board_new.board[(x, new_y)] = Peon(self.color, board_new, (x, new_y))
            del board_new.board[self.position]
            boards.append(board_new)

        # Diagonal captures
        for dx in [-1, 1]:
            new_x, new_y = x + dx, y + move
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target = self.board.board.get((new_x, new_y))
                if target and target.color != self.color:
                    board_new = self.board.copy()
                    if new_y == (7 if self.color == 'w' else 0):
                        board_new.board[(new_x, new_y)] = Zombie(self.color, board_new, (new_x, new_y))
                    else:
                        board_new.board[(new_x, new_y)] = Peon(self.color, board_new, (new_x, new_y))
                    del board_new.board[self.position]
                    boards.append(board_new)
        return boards

class Queen(Piece):
    def next(self):
        boards = []
        x, y = self.position
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in moves:
            for i in range(1, 8):
                new_x, new_y = x + i * dx, y + i * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    pos = (new_x, new_y)
                    piece_at_pos = self.board.board.get(pos)
                    if piece_at_pos is None:
                        board_new = self.board.copy()
                        board_new.board[pos] = Queen(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                    elif piece_at_pos.color != self.color:
                        board_new = self.board.copy()
                        board_new.board[pos] = Queen(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                        break
                    else:
                        break
                else:
                    break
        return boards

class Rook(Piece):
    def next(self):
        boards = []
        x, y = self.position
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in moves:
            for i in range(1, 8):
                new_x, new_y = x + i * dx, y + i * dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    pos = (new_x, new_y)
                    piece_at_pos = self.board.board.get(pos)
                    if piece_at_pos is None:
                        board_new = self.board.copy()
                        board_new.board[pos] = Rook(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                    elif piece_at_pos.color != self.color:
                        board_new = self.board.copy()
                        board_new.board[pos] = Rook(self.color, board_new, pos)
                        del board_new.board[self.position]
                        boards.append(board_new)
                        break
                    else:
                        break
                else:
                    break
        return boards

class Zombie(Piece):
    def next(self):
        boards = []
        x, y = self.position
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = self.board.board.get((nx, ny))
                if target is None or target.color != self.color:
                    board_new = self.board.copy()
                    board_new.board[(nx, ny)] = Zombie(self.color, board_new, (nx, ny))
                    del board_new.board[self.position]
                    boards.append(board_new)
        return boards

class Board:
    pieces = {
        'B': Bishop,
        'C': Cannon,
        'F': Flinger,
        'K': King,
        'N': Knight,
        'P': Peon,
        'Q': Queen,
        'R': Rook,
        'Z': Zombie,
    }
    
    piece_symbols = {
        Bishop: 'B',
        Cannon: 'C',
        Flinger: 'F',
        King: 'K',
        Knight: 'N',
        Peon: 'P',
        Queen: 'Q',
        Rook: 'R',
        Zombie: 'Z'
    }

    def __init__(self, board=None, turn=None, diff_values=None):
        """
        Represents a state of the board.

        Parameters
        ----------
        board: dict
            A dictionary mapping positions to pieces.
        turn: str
            Either 'w' or 'b' for white or black turn, respectively.
        diff_values: tuple of int
            The three extra integers from the first line of the input.
        """
        if board is None:
            board = {}
        self.check(board)
        self.board = board
        self.turn = turn
        self.diff_values = diff_values
        for piece in self.board.values():
            if piece is not None:
                piece.board = self

    @classmethod
    def check(cls, board):
        """Ensures board positions are within bounds."""
        for x, y in board.keys():
            assert 0 <= x <= 7 and 0 <= y <= 7

    @classmethod
    def from_string(cls, txt):
        """
        Initializes the board from a string in the given format.
        """
        lines = txt.strip().splitlines()
        first_line_parts = lines[0].split()
        turn = first_line_parts[0]
        diff_values = tuple(map(int, first_line_parts[1:]))

        board = {}
        for line in lines[1:]:
            if line.startswith("{") or line.startswith("}"):
                continue
            if ":" in line:
                position, piece = line.split(":")
                position = position.strip()
                piece = piece.strip().strip("'")
                color, piece_type = piece[0], piece[1]
                x = ord(position[0].lower()) - ord('a')
                y = int(position[1]) - 1

                piece_class = cls.pieces.get(piece_type)
                if piece_class:
                    board[(x, y)] = piece_class(color, None, (x, y))

        instance = cls(board, turn, diff_values)
        for piece in instance.board.values():
            if piece is not None:
                piece.board = instance
        return instance

    def __getitem__(self, pos):
        return self.board.get(pos)

    def capture(self, x, y):
        if (x, y) in self.board:
            del self.board[(x, y)]

    def copy(self):
        board_new = {pos: type(piece)(piece.color, None, pos) 
                    for pos, piece in self.board.items() 
                    if piece is not None}
        instance = Board(board_new, self.turn, self.diff_values)
        for piece in instance.board.values():
            if piece is not None:
                piece.board = instance
        return instance

    def switch_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'

    def apply_contagion(self):
        zombies = [pos for pos, piece in self.board.items() if isinstance(piece, Zombie)]
        conversions = {}
        for x, y in zombies:
            zombie_color = self.board[(x, y)].color
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.board.get((nx, ny))
                    if target and target.color != zombie_color and not isinstance(target, (King, Zombie)) and (nx, ny) not in conversions:
                        conversions[(nx, ny)] = Zombie(zombie_color, self, (nx, ny))
        for pos, zombie in conversions.items():
            self.board[pos] = zombie

    def next(self):
        boards = []
        for pos, piece in list(self.board.items()):
            if piece is not None and piece.color == self.turn:
                for board_new in piece.next():
                    board_new.switch_turn()
                    board_new.apply_contagion()
                    boards.append(board_new)
        return boards

    def to_string(self):
        """Returns a string representation of the board."""
        board_rep = []
        pieces = [(pos, piece) for pos, piece in self.board.items() if piece is not None]
        for idx, ((x, y), piece) in enumerate(pieces):
            col = chr(x + ord('a'))
            row = y + 1
            piece_symbol = self.piece_symbols[piece.__class__]
            piece_rep = f"  {col}{row}: '{piece.color}{piece_symbol}'"
            if idx < len(pieces) - 1:
                piece_rep += ','
            board_rep.append(piece_rep)

        diff_values_str = " ".join(map(str, self.diff_values))
        return f"{self.turn} {diff_values_str}\n{{\n" + "\n".join(board_rep) + "\n}\n0\n0\n0\n"

if __name__ == '__main__':
    board = Board.from_string(sys.stdin.read())
    for i, board_new in enumerate(board.next(), 0):
        with open(f'board.{i:03d}', 'w') as f:
            f.write(board_new.to_string())

