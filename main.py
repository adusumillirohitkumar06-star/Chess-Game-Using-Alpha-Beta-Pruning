import chess
def print_board(board, user_color):
    """Displays the chessboard in a readable format."""
    print("\n    a b c d e f g h")
    print("  +-----------------+")
    rows = str(board).split("\n")

    if user_color == chess.WHITE:
        for i, row in enumerate(rows, start=1):
            rank = 9 - i
            print(f"{rank} | {row} | {rank}")
    else:
        for i, row in enumerate(rows[::-1], start=1):
            rank = i
            row_cells = row.split(" ")
            flipped_row = " ".join(row_cells[::-1])
            print(f"{rank} | {flipped_row} | {rank}")

    print("  +-----------------+")
    print("    a b c d e f g h\n")


def evaluate_board(board):
    """Evaluates the board based on material advantage."""
    if board.is_checkmate():
        return float('inf') if not board.turn else -float('inf')
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    score = 0
    for piece, val in values.items():
        score += len(board.pieces(piece, chess.WHITE)) * val
        score -= len(board.pieces(piece, chess.BLACK)) * val
    return score


def alpha_beta(board, depth, alpha, beta, maximizing):
    """Alpha-Beta Pruning algorithm implementation."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
        value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = max(value, alpha_beta(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = min(value, alpha_beta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def select_move(board, depth):
    """Selects the best move for the AI using alpha-beta pruning."""
    best_move = None
    best_val = -float('inf') if board.turn else float('inf')

    for move in board.legal_moves:
        board.push(move)
        val = alpha_beta(board, depth - 1, -float('inf'), float('inf'), not board.turn)
        board.pop()

        if board.turn and val > best_val:
            best_val, best_move = val, move
        elif not board.turn and val < best_val:
            best_val, best_move = val, move

    return best_move


def play_game():
    """Main function to play the chess game."""
    board = chess.Board()
    move_history = []

    color = input("Choose your side (white/black): ").strip().lower()
    if color not in ["white", "black"]:
        print("Invalid choice! Defaulting to white.")
        color = "white"

    user_color = chess.WHITE if color == "white" else chess.BLACK
    print(f"\nYou are playing as {color.capitalize()}.\n")
    print("Capital letters represent White pieces, lowercase represent Black pieces.\n")

    # If user plays black, AI starts
    if user_color == chess.BLACK:
        ai_move = select_move(board, depth=3)
        board.push(ai_move)
        move_history.append(str(ai_move))
        print(f"AI move: {ai_move}\n")

    while not board.is_game_over():
        print_board(board, user_color)
        print("Moves so far:", " ".join(move_history) if move_history else "None")

        if board.turn == user_color:
            move = input("Your move (e.g., e2e4): ").strip()
            try:
                board.push_uci(move)
                move_history.append(move)
            except ValueError:
                print("Invalid move! Try again.\n")
                continue
        else:
            print("\nAI is thinking...\n")
            ai_move = select_move(board, depth=3)
            board.push(ai_move)
            move_history.append(str(ai_move))
            print(f"AI move: {ai_move}\n")

    print_board(board, user_color)
    print("Game Over")
    print("Result:", board.result())
    print("Move history:", " ".join(move_history))


if __name__ == "__main__":
    play_game()


