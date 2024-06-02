from . import app
from app import routes

if __name__== 'main':
    app.run(debug=True)