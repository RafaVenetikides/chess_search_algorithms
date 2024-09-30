import chess
import math

def pretty_print_board(board):
    piece_symbols = {
        chess.PAWN: '♙', chess.KNIGHT: '♘', chess.BISHOP: '♗',
        chess.ROOK: '♖', chess.QUEEN: '♕', chess.KING: '♔',
        chess.PAWN + 8: '♟', chess.KNIGHT + 8: '♞', chess.BISHOP + 8: '♝',
        chess.ROOK + 8: '♜', chess.QUEEN + 8: '♛', chess.KING + 8: '♚'
    }
    
    board_str = ""
    
    for rank in range(7, -1, -1):
        board_str += f"{rank + 1} "  
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            if piece:
                board_str += piece_symbols[piece.piece_type + (8 if piece.color == chess.BLACK else 0)] + " "
            else:
                board_str += ". "  
        board_str += "\n"
    
    board_str += "  a b c d e f g h"  
    print(board_str)

def alphabeta(board, max_depth, color):
    best_move = None

    if color == chess.WHITE:
        best_value = -math.inf
    else:
        best_value = math.inf

    for move in board.legal_moves:
        board.push(move)
        if color == chess.WHITE:
            value = min_value(board, -math.inf, math.inf, max_depth, color)
            if value > best_value:
                best_value = value
                best_move = move
        else:
            value = max_value(board, -math.inf, math.inf, max_depth, color)
            if value < best_value:
                best_value = value
                best_move = move
        board.pop()

    print(f"Best move: {best_move}, value: {best_value}")
    return best_move

def board_utility(board, color):
    
    player_score = 0
    opponent_score = 0
    
    for square, piece in board.piece_map().items():
        if piece.color == color:
            player_score += 1
        else:
            opponent_score += 1
    
    return player_score - opponent_score

def max_value(board, alpha, beta, max_depth, color):
    if board.is_checkmate():
        return -math.inf 
    if board.is_stalemate() or board.is_insufficient_material() or max_depth == 0:
        return board_utility(board, color)
    
    max_depth -= 1
    v = -math.inf

    for a in board.legal_moves:
        move = chess.Move.from_uci(str(a))
        board.push(move)
        v = max(v, min_value(board, alpha, beta, max_depth, color))
        board.pop()

        if v >= beta: return v
        alpha = max(alpha, v)
    return v

def min_value(board, alpha, beta, max_depth, color):
    if board.is_checkmate():
        return math.inf  
    if board.is_stalemate() or board.is_insufficient_material() or max_depth == 0:
        return board_utility(board, color)
    
    max_depth -= 1
    v = math.inf

    for a in board.legal_moves:
        move = chess.Move.from_uci(str(a))
        board.push(move)
        v = min(v, max_value(board, alpha, beta, max_depth, color))
        board.pop()

        if v <= alpha: return v
        beta = min(beta, v)
    return v


board = chess.Board()

print(f"[1] AI vs AI\n[2] Player vs AI")
mode = input("Select mode: ")

if mode == "2":
    print(f"[1] White\n[2] Black")
    color = input("Select color: ")

    if color == "2":
        move = alphabeta(board, 3, chess.BLACK)
        board.push(move)
        pretty_print_board(board)

if mode == "1":
    while not board.is_game_over():
        move = alphabeta(board, 3, board.turn)
        board.push(move)
        pretty_print_board(board)
        print(board.legal_moves)
else:
    while not board.is_game_over():
        pretty_print_board(board)
        print(board.legal_moves)
        move = input("Enter move: ")
        try:
            board.push_san(move)
        except:
            print("Invalid move")
            continue
        
        pretty_print_board(board)
        move = alphabeta(board, 3, board.turn)
        board.push(move)

print(board.result())