from flask import Flask, render_template, request
app = Flask (__name__)

@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/report')
def report():
    user = request.args.get('UserName')
    pw = request.args.get('Password')
    upperFlag = False
    lowerFlag = False
    numFlag = False
    message = ""
    error_list = []
    if pw[-1].isnumeric():
        numFlag = True
       
    for char in pw:
        if char.isupper():
            upperFlag = True
            
        if char.islower():
            lowerFlag = True
            
    if numFlag == False:
        message = "password is missing number at the end"
        error_list.append(message)
    if lowerFlag == False:
        message = "password is missing lowercase character"
        error_list.append(message)
    if upperFlag == False:
        message = "password is missing uppercase character"
        error_list.append(message)

    upperFlagUser = False
    lowerFlagUser = False
    numFlagUser = False
    if user[-1].isnumeric():
        numFlagUser = True
    for char in user:
        if char.isupper():
            upperFlagUser = True
        if char.islower():
            lowerFlagUser = True
        
    if numFlagUser == False:
        message = "user is missing number at the end"
        error_list.append(message)
    if lowerFlagUser == False:
         message = "user is missing lowercase character"
         error_list.append(message)
    if upperFlagUser == False:
        message = "user is missing uppercase character"
        error_list.append(message)
    if message == "":
        message = "Password and User worked!"
    if len(error_list) == 0:
        message = "User and Password work!"
    return render_template("report.html", error_list=error_list, message = message)


if __name__ == '__main__':
    app.run(debug=True)