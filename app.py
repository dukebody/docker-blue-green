from bottle import route, run, default_app

@route('/')
def index():
    return '<b>Hello broken!</b>!'

app = default_app()
