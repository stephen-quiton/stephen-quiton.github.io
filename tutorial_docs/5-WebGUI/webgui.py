from fireworks import LaunchPad
from fireworks.flask_site.app import app

app.lp = LaunchPad(
    host = 'localhost',
    port = XXXXX,
    authsource = 'admin',
    name = 'fireworks',
    password = None,
    ssl = False,
    username = None)  # change the LaunchPad info if needed

app.run(port=YYYY,debug=True)