from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__, static_folder='Styles', template_folder='Templates')

@app.route('/')
def Home():
    current_time = datetime.now().strftime('%H:%M')
    return render_template('Home.html', current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
