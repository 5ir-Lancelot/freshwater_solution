import sys
import os

# Add the directory containing your Flask application to the Python path
sys.path.insert(0, '/var/www/carbonate-system-modelling/freshwater_solution')


from my_app import server as application