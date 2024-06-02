from flask import render_template, request, jsonify
from . import app
import app.letters_round as lr
import app.numbers_round as nr

@app.route('/')
def index():
    return render_template('index.html')  # Render the game's starting page

@app.route('/play/letters', methods=['GET', 'POST'])
def play_letters():
    if request.method == 'POST':
        # Process submitted answers and return results
        # For simplicity, assuming the answer is sent via form data
        answer = request.form['answer']
        score = lr.evaluate_letters(answer)  # Hypothetical function in your letters_round module
        return jsonify(score=score)
    else:
        # GET request - serve the letters round game page
        # You would likely generate and send the letters for the round here
        letters = lr.generate_letters()  # Hypothetical function to generate letters
        return render_template('letters_round.html', letters=letters)

@app.route('/play/numbers', methods=['GET', 'POST'])
def play_numbers():
    if request.method == 'POST':
        # Similar to play_letters, but for numbers
        answer = request.form['answer']
        score = nr.evaluate_numbers(answer)  # Hypothetical function in your numbers_round module
        return jsonify(score=score)
    else:
        # Serve the numbers round game page
        numbers, target = nr.generate_numbers()  # Hypothetical function to generate numbers and target
        return render_template('numbers_round.html', numbers=numbers, target=target)
    
if __name__== 'main':
    app.run(debug=True)