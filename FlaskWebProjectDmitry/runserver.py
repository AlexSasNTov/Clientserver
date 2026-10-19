"""
This script runs the FlaskWebProjectDmitry application using a development server.
"""

import sys
import collections
import markupsafe
import jinja2

try:
    from collections import UserDict
except ImportError:
    import collections.abc
    UserDict = collections.UserDict
sys.modules['UserDict'] = UserDict

jinja2.Markup = markupsafe.Markup
jinja2.escape = markupsafe.escape

import os
from FlaskWebProjectDmitry import app

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
        
    print(f"Сервер запускается на http://{HOST}:{PORT}")
    app.run(HOST, PORT)