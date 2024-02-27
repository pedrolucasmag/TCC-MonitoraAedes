from app import create_app
from livereload import Server

app = create_app()

if __name__ == '__main__':
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve(debug=False)