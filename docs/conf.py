import sys
import os

sys.path.append(os.path.abspath('..'))
project = 'HW14_JWT'
copyright = '2024, Serhii'
author = 'Serhii'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
