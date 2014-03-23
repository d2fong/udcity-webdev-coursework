import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app
