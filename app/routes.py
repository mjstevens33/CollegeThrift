from app import app


@app.route('/')
@app.route('/Home')
def Home():
    return render_template('main.html', title='Home')