import copy

class Game:
    def __init__(self):
        # 7x7 grid where only 24 positions are available
        self.board = [['.' for i in range(7)] for i in range(7)]
        
        # Available positions (x, y) coordinates based on the image
        self.tiles = {
            # Outer Square (8 nodes)
            (0, 0), (0, 3), (0, 6),  # Top row
            (3, 6), (6, 6), (6, 3), (6, 0), (3, 0),  # Right, bottom, left sides
            
            # Middle Square (8 nodes)
            (1, 1), (1, 3), (1, 5),  # Top row
            (3, 5), (5, 5), (5, 3), (5, 1), (3, 1),  # Right, bottom, left sides
            
            # Inner Square (8 nodes)
            (2, 2), (2, 3), (2, 4),  # Top row
            (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)   # Right, bottom, left sides
        }
        
        # Game state
        self.placed = 0  # Total pieces placed
        self.white = 0   # White pieces on board
        self.black = 0   # Black pieces on board
        self.white_removed = 0  # White pieces removed
        self.black_removed = 0  # Black pieces removed
        self.player = 'W'  # Current player
        self.history = []
        self.game_started = False  # Track if a game has been started
        
        # Define adjacency for each position based on the image
        # Only positions connected by lines are adjacent
        self.adjacency = {
            # Outer Square (8 points) - corners and midpoints
            (0, 0): [(0, 3), (3, 0)],  # Top-left corner
            (0, 3): [(0, 0), (0, 6), (1, 3)],  # Top middle
            (0, 6): [(0, 3), (3, 6)],  # Top-right corner
            (3, 0): [(0, 0), (6, 0)],  # Left middle
            (3, 6): [(0, 6), (6, 6)],  # Right middle
            (6, 0): [(3, 0), (6, 3)],  # Bottom-left corner
            (6, 3): [(6, 0), (6, 6), (5, 3)],  # Bottom middle
            (6, 6): [(3, 6), (6, 3)],  # Bottom-right corner
            
            # Middle Square (8 points) - corners and midpoints
            (1, 1): [(1, 3), (3, 1)],  # Inner top-left
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],  # Inner top middle
            (1, 5): [(1, 3), (3, 5)],  # Inner top-right
            (3, 1): [(1, 1), (3, 0), (3, 2), (5, 1)],  # Inner left middle
            (3, 5): [(1, 5), (3, 6), (5, 5)],  # Inner right middle
            (5, 1): [(3, 1), (5, 3)],  # Inner bottom-left
            (5, 3): [(6, 3), (5, 1), (5, 5), (4, 3)],  # Inner bottom middle
            (5, 5): [(3, 5), (5, 3)],  # Inner bottom-right
            
            # Inner Square (8 points) - corners and midpoints
            (2, 2): [(2, 3), (3, 2)],  # Center top-left
            (2, 3): [(1, 3), (2, 2), (2, 4)],  # Center top middle
            (2, 4): [(2, 3), (3, 4)],  # Center top-right
            (3, 2): [(2, 2), (3, 1), (4, 2)],  # Center left middle
            (3, 4): [(2, 4), (3, 5), (4, 4)],  # Center right middle
            (4, 2): [(3, 2), (4, 3)],  # Center bottom-left
            (4, 3): [(2, 3), (4, 2), (4, 4), (5, 3)],  # Center bottom middle
            (4, 4): [(3, 4), (4, 3)]   # Center bottom-right
        }
        
        # Define all possible mills (three-in-a-row)
        self.mills = [
            # Horizontal mills
            [(0, 0), (0, 3), (0, 6)],
            [(1, 1), (1, 3), (1, 5)],
            [(2, 2), (2, 3), (2, 4)],
            [(3, 0), (3, 1), (3, 2)],
            [(3, 4), (3, 5), (3, 6)],
            [(4, 2), (4, 3), (4, 4)],
            [(5, 1), (5, 3), (5, 5)],
            [(6, 0), (6, 3), (6, 6)],
            # Vertical mills
            [(0, 0), (3, 0), (6, 0)],
            [(1, 1), (3, 1), (5, 1)],
            [(2, 2), (3, 2), (4, 2)],
            [(0, 3), (1, 3), (2, 3)],
            [(4, 3), (5, 3), (6, 3)],
            [(2, 4), (3, 4), (4, 4)],
            [(1, 5), (3, 5), (5, 5)],
            [(0, 6), (3, 6), (6, 6)]
        ]

    def start(self):
        """Reset the game to initial state"""
        self.board = [['.' for i in range(7)] for i in range(7)]
        self.placed = 0
        self.white = 0
        self.black = 0
        self.white_removed = 0
        self.black_removed = 0
        self.player = 'W'
        self.history = []
        self.game_started = True

    def switch_player(self):
        """Switch to the other player"""
        self.player = 'B' if self.player == 'W' else 'W'

    def is_placement_phase(self):
        """Check if we're still in the placement phase"""
        return self.placed < 18

    def place(self, x, y):
        """Place a piece at the given coordinates"""
        if self.placed >= 18:
            return False, "All pieces have been placed"
        
        if (x, y) not in self.tiles:
            return False, "Invalid position"
        
        if self.board[y][x] != '.':
            return False, "Position already occupied"
        
        # Place the piece
        self.board[y][x] = self.player
        self.placed += 1
        if self.player == 'W':
            self.white += 1
        else:
            self.black += 1
        
        # Check for mill formation
        mill_formed = self.check_mill(x, y)
        
        # Record the move
        self.history.append(('place', x, y, None, mill_formed))
        
        # Switch player (unless a mill was formed, then same player gets another turn)
        if not mill_formed:
            self.switch_player()
        
        return True, "Piece placed successfully" + (" - Mill formed!" if mill_formed else "")

    def move(self, x, y, nx, ny):
        """Move a piece from (x,y) to (nx,ny)"""
        if self.placed < 18:
            return False, "Still in placement phase"
        
        if (x, y) not in self.tiles or (nx, ny) not in self.tiles:
            return False, "Invalid position"
        
        if self.board[y][x] != self.player:
            return False, "No piece of current player at source position"
        
        if self.board[ny][nx] != '.':
            return False, "Destination position is occupied"
        
        # Check if move is valid (adjacent or flying)
        if not self.is_valid_move(x, y, nx, ny):
            return False, "Invalid move - positions not adjacent"
        
        # Move the piece
        self.board[y][x] = '.'
        self.board[ny][nx] = self.player
        
        # Check for mill formation
        mill_formed = self.check_mill(nx, ny)
        
        # Record the move
        self.history.append(('move', x, y, nx, ny, mill_formed))
        
        # Switch player (unless a mill was formed, then same player gets another turn)
        if not mill_formed:
            self.switch_player()
        
        return True, "Piece moved successfully" + (" - Mill formed!" if mill_formed else "")

    def is_valid_move(self, x, y, nx, ny):
        """Check if a move is valid"""
        # If player has only 3 pieces left, they can fly (move anywhere)
        pieces_on_board = self.white if self.player == 'W' else self.black
        if pieces_on_board <= 3:
            return True
        
        # Otherwise, must move to adjacent position
        return (nx, ny) in self.adjacency[(x, y)]

    def check_mill(self, x, y):
        """Check if placing/moving a piece at (x,y) forms a mill"""
        player = self.board[y][x]
        for mill in self.mills:
            if (x, y) in mill:
                if all(self.board[pos[1]][pos[0]] == player for pos in mill):
                    return True
        return False

    def remove_piece(self, x, y):
        """Remove an opponent's piece (after forming a mill)"""
        if (x, y) not in self.tiles:
            return False, "Invalid position"
        
        opponent = 'B' if self.player == 'W' else 'W'
        if self.board[y][x] != opponent:
            return False, "No opponent piece at that position"
        
        # Check if piece is in a mill (can only remove if no other pieces available)
        if self.is_in_mill(x, y, opponent):
            # Check if all opponent pieces are in mills
            opponent_positions = [(x, y) for x in range(7) for y in range(7) 
                                if self.board[y][x] == opponent]
            if all(self.is_in_mill(pos[0], pos[1], opponent) for pos in opponent_positions):
                pass  # Can remove from mill
            else:
                return False, "Cannot remove piece from mill unless all pieces are in mills"
        
        # Remove the piece
        self.board[y][x] = '.'
        if opponent == 'W':
            self.white -= 1
            self.white_removed += 1
        else:
            self.black -= 1
            self.black_removed += 1
        
        self.history.append(('remove', x, y, None, None))
        self.switch_player()
        return True, "Piece removed successfully"

    def is_in_mill(self, x, y, player):
        """Check if a piece is part of a mill"""
        for mill in self.mills:
            if (x, y) in mill:
                if all(self.board[pos[1]][pos[0]] == player for pos in mill):
                    return True
        return False

    def undo(self):
        """Undo the last move"""
        if not self.history:
            return False, "No moves to undo"
        
        action, x, y, nx, ny, mill_formed = self.history.pop()
        
        if action == 'place':
            self.board[y][x] = '.'
            self.placed -= 1
            if self.player == 'B':  # Undoing white's move
                self.white -= 1
            else:  # Undoing black's move
                self.black -= 1
        elif action == 'move':
            self.board[ny][nx] = '.'
            self.board[y][x] = self.player
        elif action == 'remove':
            opponent = 'B' if self.player == 'W' else 'W'
            self.board[y][x] = opponent
            if opponent == 'W':
                self.white += 1
                self.white_removed -= 1
            else:
                self.black += 1
                self.black_removed -= 1
        
        # Switch player back
        self.switch_player()
        return True, "Move undone"

    def get_valid_moves(self):
        """Get all valid moves for the current player"""
        moves = []
        
        if self.is_placement_phase():
            # Placement phase
            for x in range(7):
                for y in range(7):
                    if (x, y) in self.tiles and self.board[y][x] == '.':
                        moves.append(('place', x, y))
        else:
            # Movement phase
            player_positions = [(x, y) for x in range(7) for y in range(7) 
                              if self.board[y][x] == self.player]
            pieces_on_board = len(player_positions)
            
            for from_x, from_y in player_positions:
                if pieces_on_board <= 3:
                    # Flying - can move anywhere
                    for to_x in range(7):
                        for to_y in range(7):
                            if (to_x, to_y) in self.tiles and self.board[to_y][to_x] == '.':
                                moves.append(('move', from_x, from_y, to_x, to_y))
                else:
                    # Normal movement - adjacent only
                    for to_x, to_y in self.adjacency[(from_x, from_y)]:
                        if self.board[to_y][to_x] == '.':
                            moves.append(('move', from_x, from_y, to_x, to_y))
        
        return moves

    def is_game_over(self):
        """Check if the game is over"""
        # Only check for game over if we're not in the initial state
        if self.placed == 0:
            return False, None
        
        # Don't check for game over during placement phase
        if self.is_placement_phase():
            return False, None
        
        # Check if a player has less than 3 pieces on board
        if self.white < 3:
            return True, 'B'  # Black wins
        if self.black < 3:
            return True, 'W'  # White wins
        
        # Check for no valid moves in movement phase
        if not self.get_valid_moves():
            return True, 'B' if self.player == 'W' else 'W'
        
        return False, None

    def evaluate_position(self):
        """Evaluate position using exact priority system"""
        # 1. Immediately winning
        game_over, winner = self.is_game_over()
        if game_over:
            if winner == 'W':
                return 1000000  # White wins
            else:
                return -1000000  # Black wins
        
        score = 0
        
        # 2. Preventing opponent from immediately winning
        white_prevents_loss = self.can_prevent_immediate_loss('W')
        black_prevents_loss = self.can_prevent_immediate_loss('B')
        if white_prevents_loss:
            score += 900000
        if black_prevents_loss:
            score -= 900000
        
        # 3. Creating a mill
        white_creates_mill = self.can_create_mill('W')
        black_creates_mill = self.can_create_mill('B')
        if white_creates_mill:
            score += 800000
        if black_creates_mill:
            score -= 800000
        
        # 4. Blocking opponent's 2-in-a-row
        white_blocks_mill = self.can_block_opponent_mill('W')
        black_blocks_mill = self.can_block_opponent_mill('B')
        if white_blocks_mill:
            score += 700000
        if black_blocks_mill:
            score -= 700000
        
        # 5. Maintaining a mill
        white_mills = self.count_mills('W')
        black_mills = self.count_mills('B')
        score += white_mills * 600000 - black_mills * 600000
        
        # 6. Having an unblocked 2-in-a-row
        white_twos = self.count_two_in_row('W')
        black_twos = self.count_two_in_row('B')
        score += white_twos * 500000 - black_twos * 500000
        
        return score

    def count_immediate_mill_opportunities(self, player):
        """Count immediate mill formation opportunities (can form mill in next move)"""
        count = 0
        for mill in self.mills:
            player_pieces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == player)
            empty_spaces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == '.')
            if player_pieces == 2 and empty_spaces == 1:
                # Check if we can place/move to the empty space
                empty_pos = None
                for pos in mill:
                    if self.board[pos[1]][pos[0]] == '.':
                        empty_pos = pos
                        break
                
                if empty_pos:
                    # Check if this position is reachable in the next move
                    if self.is_placement_phase():
                        count += 1  # Can place anywhere
                    else:
                        # Check if any of our pieces can move to this position
                        player_positions = [(x, y) for x in range(7) for y in range(7) 
                                          if self.board[y][x] == player]
                        for px, py in player_positions:
                            if self.can_move_to(px, py, empty_pos[0], empty_pos[1]):
                                count += 1
                                break
        return count

    def count_mills(self, player):
        """Count how many mills a player has"""
        count = 0
        for mill in self.mills:
            if all(self.board[pos[1]][pos[0]] == player for pos in mill):
                count += 1
        return count

    def count_two_in_row(self, player):
        """Count two-in-a-row pieces for a player"""
        count = 0
        for mill in self.mills:
            player_pieces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == player)
            empty_spaces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == '.')
            if player_pieces == 2 and empty_spaces == 1:
                count += 1
        return count

    def can_move_to(self, from_x, from_y, to_x, to_y):
        """Check if a piece can move from one position to another"""
        if not self.is_valid_move(from_x, from_y, to_x, to_y):
            return False
        return self.board[to_y][to_x] == '.'

    def get_opponent_mill_threats(self, player):
        """Get opponent pieces that can form mills next turn"""
        opponent = 'B' if player == 'W' else 'W'
        threats = []
        
        for mill in self.mills:
            opponent_pieces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == opponent)
            empty_spaces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == '.')
            if opponent_pieces == 2 and empty_spaces == 1:
                # Find the empty position
                for pos in mill:
                    if self.board[pos[1]][pos[0]] == '.':
                        # Find opponent pieces that can move to this position
                        opponent_positions = [(x, y) for x in range(7) for y in range(7) 
                                            if self.board[y][x] == opponent]
                        for ox, oy in opponent_positions:
                            if self.can_move_to(ox, oy, pos[0], pos[1]):
                                threats.append((ox, oy))
        return threats

    def can_prevent_immediate_loss(self, player):
        """Check if player can prevent immediate loss"""
        opponent = 'B' if player == 'W' else 'W'
        
        # Check if opponent can win by reducing pieces to less than 3
        opponent_pieces = self.black if opponent == 'B' else self.white
        my_pieces = self.white if player == 'W' else self.black
        
        if opponent_pieces <= 3 and my_pieces <= 3:
            # Check if opponent can remove enough pieces to win
            return True
        
        # Check if opponent can block all our moves
        if not self.is_placement_phase():
            my_valid_moves = 0
            my_positions = [(x, y) for x in range(7) for y in range(7) 
                           if self.board[y][x] == player]
            for px, py in my_positions:
                for to_x in range(7):
                    for to_y in range(7):
                        if (to_x, to_y) in self.tiles and self.board[to_y][to_x] == '.':
                            if self.can_move_to(px, py, to_x, to_y):
                                my_valid_moves += 1
                                break
                    if my_valid_moves > 0:
                        break
                if my_valid_moves > 0:
                    break
            
            if my_valid_moves == 0:
                return True
        
        return False

    def can_create_mill(self, player):
        """Check if player can create a mill in next move"""
        for mill in self.mills:
            player_pieces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == player)
            empty_spaces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == '.')
            if player_pieces == 2 and empty_spaces == 1:
                # Check if we can place/move to the empty space
                for pos in mill:
                    if self.board[pos[1]][pos[0]] == '.':
                        if self.is_placement_phase():
                            return True
                        else:
                            # Check if any of our pieces can move to this position
                            player_positions = [(x, y) for x in range(7) for y in range(7) 
                                              if self.board[y][x] == player]
                            for px, py in player_positions:
                                if self.can_move_to(px, py, pos[0], pos[1]):
                                    return True
                        break
        return False

    def can_block_opponent_mill(self, player):
        """Check if player can block opponent's 2-in-a-row"""
        opponent = 'B' if player == 'W' else 'W'
        
        for mill in self.mills:
            opponent_pieces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == opponent)
            empty_spaces = sum(1 for pos in mill if self.board[pos[1]][pos[0]] == '.')
            if opponent_pieces == 2 and empty_spaces == 1:
                # Find the empty position that would complete opponent's mill
                for pos in mill:
                    if self.board[pos[1]][pos[0]] == '.':
                        # Check if we can place/move to this position
                        if self.is_placement_phase():
                            return True
                        else:
                            # Check if any of our pieces can move to this position
                            player_positions = [(x, y) for x in range(7) for y in range(7) 
                                              if self.board[y][x] == player]
                            for px, py in player_positions:
                                if self.can_move_to(px, py, pos[0], pos[1]):
                                    return True
                        break
        return False



    def will_move_form_mill(self, move):
        """Check if a specific move will form a mill"""
        if move[0] == 'place':
            x, y = move[1], move[2]
        else:
            x, y = move[3], move[4]  # Destination coordinates
        
        # Temporarily place the piece
        original_piece = self.board[y][x]
        self.board[y][x] = self.player
        
        # Check if this forms a mill
        mill_formed = self.check_mill(x, y)
        
        # Restore the board
        self.board[y][x] = original_piece
        
        return mill_formed

    def display_board(self):
        """Display the current board state"""
        print("\n" + "="*50)
        print("MILL GAME SOLVER")
        print("="*50)
        
        # Create visual representation with proper lines and nodes
        # Based on the exact layout from the image
        visual = [
            "*─────*─────*",
            "│     │     │",
            "│ *———*———* │",
            "│ │   │   │ │",
            "│ │ *─*─* │ │",
            "│ │ │   │ │ │",
            "*─*─*   *─*─*",
            "│ │ │   │ │ │",
            "│ │ *—*—* │ │",
            "│ │   │   │ │",
            "│ *———*———* │",
            "│     │     │",
            "*─────*─────*"
        ]
        
        # Create a mapping from board coordinates to visual positions
        # Simple approach: double the coordinates for display
        coord_to_visual = {}
        for x in range(7):
            for y in range(7):
                if (x, y) in self.tiles:
                    coord_to_visual[(x, y)] = (y * 2, x * 2)
        
        # Replace nodes with pieces
        for (x, y), (vx, vy) in coord_to_visual.items():
            piece = self.board[y][x]
            if piece == '.':
                symbol = '*'  # Empty node
            elif piece == 'W':
                symbol = 'W'  # White piece
            elif piece == 'B':
                symbol = 'B'  # Black piece
            
            # Replace the node in the visual representation
            line = visual[vx]
            visual[vx] = line[:vy] + symbol + line[vy+1:]
        
        for line in visual:
            print(line)
        
        print(f"\nWhite pieces: {self.white} on board, {9 - self.white - self.white_removed} remaining, {self.white_removed} removed")
        print(f"Black pieces: {self.black} on board, {9 - self.black - self.black_removed} remaining, {self.black_removed} removed")
        print(f"Current player: {'White' if self.player == 'W' else 'Black'}")
        
        if self.is_placement_phase():
            print("Phase: Placement")
        else:
            print("Phase: Movement")
        
        print("="*50)


class MinimaxAI:
    def __init__(self, game):
        self.game = game

    def get_best_move(self, depth):
        pass

    def minimax(self, game, depth, alpha, beta, is_maximizing):
        pass


def main():
    def get_user_input(prompt, valid_options):
        """Get user input with validation"""
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input in valid_options:
                    return user_input
                else:
                    print(f"Invalid input. Please choose from: {', '.join(valid_options)}")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
            except EOFError:
                print("\nGoodbye!")
                exit()

    game = Game()
    ai = MinimaxAI(game)
    
    print("Welcome to the Mill Game Solver!")
    print("This is a strategic board game where players try to form mills (three-in-a-row)")
    print("and remove opponent pieces. The game has two phases: placement and movement.")
    
    while True:
        # Check if no game is in progress
        if not game.game_started:
            choice = get_user_input("\nWould you like to (1) start a new game or (2) quit? ", ['1', '2'])
            if choice == '1':
                game.start()
                continue
            else:
                print("Thanks for playing!")
                break
        
        # Check if game is over
        game_over, winner = game.is_game_over()
        if game_over:
            game.display_board()
            print(f"\nGame Over! {'White' if winner == 'W' else 'Black'} wins!")
            choice = get_user_input("\nWould you like to (1) start a new game or (2) quit? ", ['1', '2'])
            if choice == '1':
                game.start()
                continue
            else:
                print("Thanks for playing!")
                break
        
        # Display current board
        game.display_board()
        
        # Game in progress - get user choice
        choice = get_user_input("\nChoose an action:\n(1) Take action\n(2) Let computer decide\n(3) Undo last move\n(4) Restart game\n(5) Quit\nYour choice: ", ['1', '2', '3', '4', '5'])
        
        if choice == '1':  # User takes action
            if game.is_placement_phase():
                print(f"\nPlacement phase - {game.player} to place a piece")
                try:
                    x = int(input("Enter x-coordinate (0-6): "))
                    y = int(input("Enter y-coordinate (0-6): "))
                    success, message = game.place(x, y)
                    if not success:
                        print(f"Error: {message}")
                    else:
                        print(message)
                        # If mill was formed, require piece removal
                        if "Mill formed" in message:
                            piece_removed = False
                            while not piece_removed:
                                try:
                                    rx = int(input("Enter x-coordinate to remove opponent piece (0-6): "))
                                    ry = int(input("Enter y-coordinate to remove opponent piece (0-6): "))
                                    success, message = game.remove_piece(rx, ry)
                                    if not success:
                                        print(f"Error: {message}")
                                        print("Please try again.")
                                    else:
                                        print(message)
                                        piece_removed = True
                                except ValueError:
                                    print("Invalid input. Please enter numbers between 0 and 6.")
                except ValueError:
                    print("Invalid input. Please enter numbers between 0 and 6.")
            else:
                print(f"\nMovement phase - {game.player} to move a piece")
                try:
                    from_x = int(input("Enter source x-coordinate (0-6): "))
                    from_y = int(input("Enter source y-coordinate (0-6): "))
                    to_x = int(input("Enter destination x-coordinate (0-6): "))
                    to_y = int(input("Enter destination y-coordinate (0-6): "))
                    success, message = game.move(from_x, from_y, to_x, to_y)
                    if not success:
                        print(f"Error: {message}")
                    else:
                        print(message)
                        # If mill was formed, require piece removal
                        if "Mill formed" in message:
                            piece_removed = False
                            while not piece_removed:
                                try:
                                    rx = int(input("Enter x-coordinate to remove opponent piece (0-6): "))
                                    ry = int(input("Enter y-coordinate to remove opponent piece (0-6): "))
                                    success, message = game.remove_piece(rx, ry)
                                    if not success:
                                        print(f"Error: {message}")
                                        print("Please try again.")
                                    else:
                                        print(message)
                                        piece_removed = True
                                except ValueError:
                                    print("Invalid input. Please enter numbers between 0 and 6.")
                except ValueError:
                    print("Invalid input. Please enter numbers between 0 and 6.")
        
        elif choice == '2':  # Computer decides
            depth = int(input("Enter search depth (1-5 recommended): "))
            print(f"\nComputer ({game.player}) is thinking...")
            best_move = ai.get_best_move(depth)
            
            if best_move:
                if best_move[0] == 'place':
                    success, message = game.place(best_move[1], best_move[2])
                    print(f"Computer places piece at ({best_move[1]}, {best_move[2]})")
                else:
                    success, message = game.move(best_move[1], best_move[2], best_move[3], best_move[4])
                    print(f"Computer moves piece from ({best_move[1]}, {best_move[2]}) to ({best_move[3]}, {best_move[4]})")
                
                if success:
                    print(message)
                    # If mill was formed, computer removes a piece
                    if "Mill formed" in message:
                        print("Mill detected - attempting piece removal...")
                        # Aggressive AI for piece removal - prioritize opponent mill threats
                        opponent = 'B' if game.player == 'W' else 'W'
                        piece_removed = False
                        
                        # First, try to remove opponent pieces that can form mills next turn
                        mill_threats = game.get_opponent_mill_threats(game.player)
                        for x, y in mill_threats:
                            if game.board[y][x] == opponent:
                                success, message = game.remove_piece(x, y)
                                if success:
                                    print(f"Computer removes threatening piece at ({x}, {y})")
                                    piece_removed = True
                                    break
                        
                        # If no mill threats removed, remove any available piece
                        if not piece_removed:
                            for x in range(7):
                                for y in range(7):
                                    if game.board[y][x] == opponent:
                                        success, message = game.remove_piece(x, y)
                                        if success:
                                            print(f"Computer removes piece at ({x}, {y})")
                                            piece_removed = True
                                            break
                                if piece_removed:
                                    break
                        
                        if not piece_removed:
                            print("Computer could not remove any opponent pieces")
            else:
                print("No valid moves found!")
        
        elif choice == '3':  # Undo
            success, message = game.undo()
            if not success:
                print(f"Error: {message}")
            else:
                print("Last move undone.")
        
        elif choice == '4':  # Restart
            game.start()
            print("Game restarted.")
        
        elif choice == '5':  # Quit
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
