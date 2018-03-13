from tripmatch import create_app

if __name__ == '__main__':
    app = create_app('development_config.py')
    app.run(host='127.0.0.1', port=5000)

