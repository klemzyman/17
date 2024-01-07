from flask import Flask, render_template, request, make_response
from random import randint

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        user_name = request.cookies.get("user_name")
        
        return render_template('about.html', name=user_name)
    
    elif request.method == "POST":
        contact_name = request.form.get("contact-name")
        contact_email = request.form.get("contact-email")
        contact_message = request.form.get("contact-message")
        
        print(contact_name)
        print(contact_email)
        print(contact_message)
        
        response = make_response(render_template("success.html"))
        response.set_cookie("user_name", contact_name)
        
        return response

@app.route("/game", methods=["GET", "POST"])
def play_the_game():
    if request.method == "GET":
        game = True
        secret_number = randint(1,20)
        current_try = 1
        message = "Enter a number between 1 and 20."

        response = make_response(render_template('game.html', game=game, current_try=current_try, message=message))
        response.set_cookie("secret_number", str(secret_number))
        response.set_cookie("current_try", str(current_try))

        return response
    
    elif request.method == "POST":
        game = True
        user_guess = int(request.form.get("user_guess"))
        secret_number = int(request.cookies.get("secret_number"))
        current_try = int(request.cookies.get("current_try"))
        expires = 600


        if user_guess == secret_number:
            game = False
            message = "Congratulations! You've done it!"
            expires = 0
        
        elif current_try < 5:
            if user_guess < secret_number:
                message = "Try a higher number"
            else:
                message = "Try a lower number"

            current_try += 1

        else:
            game = False
            message = "Sorry! The secret number was " + str(secret_number)

        response = make_response(render_template('game.html', game=game, current_try=current_try, message=message))
        response.set_cookie("current_try", str(current_try))
                
        return response
        

if __name__ == '__main__':
    app.run(use_reloader=True, port=5001)
