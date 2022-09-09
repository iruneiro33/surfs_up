# To import the Flask dependency
from flask import Flask

# Create a New Flask App Instance
# "Instance" is a general term in programming to refer to a singular version of something. 
# magic methods: Variables with underscores before and after
# This __name__ variable denotes the name of the current function.

app = Flask(__name__)

# Create Flask Routes
# First, we need to define the starting point, also known as the root. 

@app.route('/')
def hello_world():
    return 'Hello world'

#Run a Flask App
# To run the app, we're first going to need to use the command line to navigate to the folder 
# where we've saved our code.    
# we want to modify the path that will run our app.py file so that we can run our file.

if __name__ == "__main__" :
    app.run(debug=True)



