from app import app


@app.route('/')
@app.route('/Home')
def Home():
    return "main.html"