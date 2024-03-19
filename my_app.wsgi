import sys
import os

# Add the directory containing your Flask application to the Python path
# here I must give the whole path to the file because the excecution of this file takes place in another directory
sys.path.insert(0, '/var/www/carbonate-system-modelling/freshwater_solution')


from my_app import server as application