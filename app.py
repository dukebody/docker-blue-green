from bottle import route, run, default_app

@route('/')
def index():
    return '<b>Hello world!</b>!'

app = default_app()
