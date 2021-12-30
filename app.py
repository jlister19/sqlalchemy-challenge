# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__) # do this every time

# 3. Define what to do when a user hits the index route. a route is more or less a uri endpoint. we are creating an endpoint. # like openweather api endpoing
#we in flask design the logic to tell the server what to return for a get requests for example.
# we use a app route decorator
# the forward slash below designates the home or index page of our application
@app.route("/")
# then we create a function to tell the application what to do when a cli makes a requsat to our route. we can call it home or whatever we want
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

# the return will eventaully call an html file. whate you call in return within the function is what will show up on the page. the print will show up in the terminal below

# 4. Define what to do when a user hits the /about route
# then create another route for an about description
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# then 
if __name__ == "__main__":
    app.run(debug=True)
