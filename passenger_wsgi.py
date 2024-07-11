import os
import sys
from DjangoDevelopment.wsgi import application
sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")))


# import imp
# import os
# import sys


# sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source('wsgi', 'passenger_wsgi.py')
# application = wsgi.application
