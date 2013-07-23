# coding: utf-8

import re

import bottle

__all__ = ['register_foaas_routes']

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
      <h1>{message}</h1>
      <p>- {subtitle}</p>
    </div>
  </body>
</html>
"""

def return_content_type():
    accepted_types = ('text/plain', 'application/json', 'text/html')
    return_type = (bottle.request.query.get('f', None) or 
                   bottle.request.headers.get('Accept',
                                              'text/plain'))
    for ret in return_type.split(','):
        if ret.strip().lower() in accepted_types:
            return ret
    return 'text/plain'

def content_type_adjuster(fn):
    def _fn(*a, **k):
        return_type = return_content_type()
        return_value = fn(*a, **k)
        bottle.response.set_header('Content-Type', return_type)
        message, subtitle = (return_value.rsplit(" - ", 1) + [""])[:2]

        if return_type == "text/plain":
            return return_value
        elif return_type == "application/json":
            items = return_value.rsplit(" - ", 1) + [""]
            return { 'message': message, 'subtitle': subtitle }
        elif return_type == "text/html":
            items = return_value.rsplit(" - ", 1) + [""]
            return bootstrap_page.format(message=message, subtitle=subtitle)
    return _fn

def register_route(app, route, text):
    @app.route(route)
    @content_type_adjuster
    def routed_text(**keyword_args):
        return text.format(**keyword_args)

def fix_routes(routes):
    variable_re = re.compile("[:]([a-z]+)")
    for route_path, route_text in routes:
        yield (variable_re.sub("<\\1>", route_path),
               variable_re.sub("{\\1}", route_text))

foaas_routes = (
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

def register_foaas_routes(foaas_app):
    """Registers the standard FOAAS routes in on bottle.Application instance"""
    for route_path, route_text in fix_routes(foaas_routes):
        register_route(foaas_app, route_path, route_text)

if __name__ == "__main__":
    foaas_app = bottle.Bottle()
    register_foaas_routes(foaas_app)
    bottle.run(app=foaas_app, host='0.0.0.0', port=8088, debug=True)
