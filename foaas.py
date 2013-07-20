# coding: utf-8

import functools

import bottle

bootstrap_page = """
<!DOCTYPE html>
<html>
  <head>
    <title>FOAAS</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">
  </head>
  <body>
    <div class="hero-unit">  
      <h1>{}</h1>
      <p>{}</p>
    </div>
  </body>
</html>
"""

foaas_app = bottle.Bottle()

def return_content_type():
    return_type = (bottle.request.query.get('f', None) or 
                   bottle.request.headers.get('Accept',
                                              'text/plain'))
    if return_type in ('text/plain', 'application/json', 'text/html'):
        return return_type
    for ret in return_type.split(','):
        if ret in ('text/plain', 'application/json', 'text/html'):
            return ret
    return 'text/plain

def content_type_adjuster(fn):
    @functools.wraps(fn)
    def _fn(*a, **k):
        return_type = return_content_type()
        return_value = fn(*a, **k)
        bottle.response.set_header('Content-Type', return_type)
        if return_type == "text/plain":
            return return_value
        elif return_type == "application/json":
            items = return_value.rsplit(" - ", 1) + [""]
            return { 'message': items[0], 'subtitle': items[1] }
        elif return_type == "text/html":
            items = return_value.rsplit(" - ", 1) + [""]
            return bootstrap_page.format(items[0], items[1])
    return _fn

class TextRoute(object):
    def __init__(self, app, route, text):
        app.route(route)(self)
        self._text = text
    @content_type_adjuster
    def __call__(self, **keyword_args):
        return self._text.format(**keyword_args)

routes = (
    ("/off/:name/:from", "Fuck off, :name. - :from"),
    ("/you/:name/:from", "Fuck you, :name. - :from"),
    ("/this/:from", "Fuck this - :from"),
    ("/that/:from", "Fuck that. - :from"),
    ("/everything/:from", "Fuck everything. - :from"),
    ("/everyone/:from", "Everyone can go and fuck off. - :name"),
    ("/donut/:name/:from", ":name, go and take a flying fuck at a rolling "
                           "donut. - :from"),
    ("/shakespeare/:name/:from", ":name, Thou clay-brained guts, thou "
                                 "knotty-pated fool, thou whoreson obscene "
                                 "greasy tallow-catch! - :from"),
    ("/linus/:name/:from", ":name, there aren't enough swear-words in the "
                           "English language, so now I'll have to call you "
                           "perkeleen vittup‰‰ just to express my disgust and "
                           "frustration with this crap. - :from"),
    ("/king/:name/:from", "Oh fuck off, just really fuck off you total "
                          "dickface. Christ :name, you are fucking thick. - "
                          ":from"),
    ("/pink/:from", "Well, Fuck me pink. - :from"),
    ("/life/:from", "Fuck my life. - :from"),
    ("/chainsaw/:name/:from", "Fuck me gently with a chainsaw, :name. Do I "
                              "look like Mother Teresa? - :from"),
    ("/:thing/:from", "Fuck :thing. - :from"),
    ("/thanks/:from", "Fuck you very much. - :from"),
)

if __name__ == "__main__":
    bottle.run(app=foaas_app, host='0.0.0.0', port=8088, debug=True)
