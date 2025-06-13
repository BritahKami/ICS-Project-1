from utils import errhandler

try:

    from website import create_app

    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    errhandler(e, 'server/main')