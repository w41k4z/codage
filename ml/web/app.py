from flask import Flask, render_template, request
from ai_model import AI

app = Flask(__name__)
ai = AI()

@app.route('/', methods=['GET', 'POST'])
def index():
    last_input = ''
    if request.method == 'POST':
        last_input = request.form.get('language')
        language = last_input.split()
        processed_data = [last_input, ai.predict(language)]
        return render_template('index.html', processed_data=processed_data)
    return render_template('index.html', processed_data=[last_input, None])

if __name__ == '__main__':
    app.run(debug=True)
