# Importing the Flask app from market module.
from market import app

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    # Running the Flask app in debug mode.
    app.run(debug=True)
