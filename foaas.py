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
    return 'text/plain'

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

@foaas_app.route('/off/<name>/<from>')
@content_type_adjuster
def off(**ka):
    return "Fuck off, {name}. - {from}".format(**ka)

@foaas_app.route('/you/<name>/<from>')
@content_type_adjuster
def you(**ka):
    return "Fuck you, {name}. - {from}".format(**ka)

@foaas_app.route('/this/<from>')
@content_type_adjuster
def this(**ka):
    return "Fuck this - {from}".format(**ka)

@foaas_app.route('/that/<from>')
@content_type_adjuster
def that(**ka):
    return "Fuck that. - {from}".format(**ka)

@foaas_app.route('/everything/<from>')
@content_type_adjuster
def everything(**ka):
    return "Fuck everything. - {from}".format(**ka)

@foaas_app.route('/everyone/<from>')
@content_type_adjuster
def everyone(**ka):
    return "Everyone can go and fuck off. - {name}".format(**ka)

@foaas_app.route('/donut/<name>/<from>')
@content_type_adjuster
def donut(**ka):
    return "{name}, go and take a flying fuck at a rolling donut. - {from}".format(**ka)

@foaas_app.route('/linus/<name>/<from>')
@content_type_adjuster
def linus(**ka):
    return "{name}, there aren't enough swear-words in the English language, so now I'll have to call you perkeleen vittup\xc3\xa4 just to express my disgust and frustration with this crap. - {from}".format(**ka)

@foaas_app.route('/king/<name>/<from>')
@content_type_adjuster
def king(**ka):
    return "Oh fuck off, just really fuck off you total dickface. Christ {name}, you are fucking thick. - {from}".format(**ka)

@foaas_app.route('/pink/<from>')
@content_type_adjuster
def pink(**ka):
    return "Well, Fuck me pink. - {from}".format(**ka)

if __name__ == "__main__":
    bottle.run(app=foaas_app, host='0.0.0.0', port=8088, debug=True)
