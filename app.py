from flask import Flask, jsonify, request

app = Flask(__name__)
# A simple in-memory structure to hold game sessions. In production, you might use a database.
games = {}
@app.route('/play', methods=['GET'])
def play_game():
    # Here you would initialize a new game session.
    # For simplicity, we'll just create a game ID and store it.
    game_id = len(games) + 1
    games[game_id] = {"status": "new game", "score": 0}
    # Return game
    data = {
        "message": "New game started", 
        "game_id": game_id, 
        "details": games[game_id]
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)