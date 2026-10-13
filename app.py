from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)
HUMAN, AI = "O", "X"
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None

def minimax(board, depth, maximizing):
    result = winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if " " not in board or depth == 9:
        return 0
    scores = []
    for i in range(9):
        if board[i] == " ":
            board[i] = AI if maximizing else HUMAN
            scores.append(minimax(board, depth + 1, not maximizing))
            board[i] = " "
    return max(scores) if maximizing else min(scores)

def best_move(board):
    best_score, move = -999, -1
    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            score = minimax(board, 1, False)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move

def game_status(board):
    result = winner(board)
    if result == AI:
        return {"over": True, "result": "ai", "message": "AI wins!"}
    if result == HUMAN:
        return {"over": True, "result": "human", "message": "You win!"}
    if " " not in board:
        return {"over": True, "result": "draw", "message": "It's a draw!"}
    return {"over": False, "result": None, "message": ""}

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/move")
def move():
    data = request.get_json(force=True)
    board = data.get("board", [])
    index = data.get("index")
    mode = data.get("mode", "ai")
    if not isinstance(board, list) or len(board) != 9 or any(x not in (" ", "X", "O") for x in board):
        return jsonify({"error": "Invalid board"}), 400
    if not isinstance(index, int) or not 0 <= index < 9 or board[index] != " ":
        return jsonify({"error": "That cell is not available"}), 400
    if game_status(board)["over"]:
        return jsonify({"error": "Game is already over"}), 400
    board[index] = HUMAN if mode == "ai" else ("X" if data.get("turn") == "X" else "O")
    status = game_status(board)
    if mode == "ai" and not status["over"]:
        ai_index = best_move(board)
        if ai_index != -1:
            board[ai_index] = AI
        status = game_status(board)
    return jsonify({"board": board, "status": status, "nextTurn": "O" if board.count("X") > board.count("O") else "X"})

@app.post("/api/tournament")
def tournament():
    wins = draws = losses = 0
    for _ in range(10):
        board = [" "] * 9
        turn = random.choice([AI, HUMAN])
        while not game_status(board)["over"]:
            if turn == AI:
                index = best_move(board)
                if index == -1: break
                board[index] = AI
            else:
                empty = [i for i, cell in enumerate(board) if cell == " "]
                if not empty: break
                board[random.choice(empty)] = HUMAN
            turn = HUMAN if turn == AI else AI
        result = winner(board)
        if result == AI: wins += 1
        elif result == HUMAN: losses += 1
        else: draws += 1
    return jsonify({"wins": wins, "draws": draws, "losses": losses})

if __name__ == "__main__":
    app.run(debug=True)
