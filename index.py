from app import flask_app

if __name__ == '__main__':
    flask_app.run(host=flask_app.config.get('HOST'),
                  port=flask_app.config.get('PORT'))
