from flask import Flask
import os

# Get the absolute path to the Duck_PA directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))

from Duck_PA.homepage import *
from Duck_PA.routes.generate_test import *
from Duck_PA.routes.submit_test import *