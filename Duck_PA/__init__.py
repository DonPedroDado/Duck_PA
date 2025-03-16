from flask import Flask

app = Flask(__name__)

from Duck_PA.teachers.get_teachers import *
from Duck_PA.teachers.delete_teacher import *
from Duck_PA.teachers.create_teacher import *
from Duck_PA.teachers.add_teacher_page import *
from Duck_PA.homepage import *
from Duck_PA.routes.generate_test import *
from Duck_PA.routes.submit_test import *