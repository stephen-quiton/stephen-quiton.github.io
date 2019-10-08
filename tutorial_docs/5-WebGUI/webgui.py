from fireworks import LaunchPad
from fireworks.flask_site.app import app

app.lp = LaunchPad(
    host = 'replace.with.MongoDB.hostname.address',
    authsource = 'admin',
    name = 'whatever you want',
    password = 'password set up in mongodb',
    ssl = True,
    username = 'username set up in mongodb')  # change the LaunchPad info if needed

app.run(port=4040,debug=True)