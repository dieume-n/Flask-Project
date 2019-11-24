import os.path
from hdps import create_app, setup_db


app = create_app()

if not os.path.isfile('hdps/hdps.db'):
    setup_db(app)

if __name__ == '__main__':
    app.run(debug=True)