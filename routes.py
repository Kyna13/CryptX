from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import email_validator
from wtforms.validators import Length, EqualTo, Email, Required
from passlib.handlers.sha2_crypt import sha256_crypt
import database_script
import time
import math

class RegisterationForm(FlaskForm):
    fullname = StringField('Full Name: ', validators = [Required(), Length(min=2, max=150)])
    username = StringField('User Name: ', validators = [Required(), Length(min=2, max=50)])
    discordid = StringField('Discord ID: ', validators = [Required(), Length(min=2, max=50)])
    email = StringField('Email Address: ', validators = [Required(), Email()])
    schoolname = StringField('School Name: ', validators = [Required(), Length(min=2, max=75)])
    confirm_password = PasswordField('Confirm Password: ', validators=[Required()])
    password = PasswordField('Password: ', validators = [Required(), Length(min=6), EqualTo('confirm_password')])
    submit = SubmitField("Sign Up")

class SigninForm(FlaskForm):
    signin_username = StringField('Username: ', validators = [Required(), Length(min=2, max=50)])
    signin_password = PasswordField('Password: ', validators = [Required(), Length(min=6)])
    submit = SubmitField("Sign In")

class AnswerForm(FlaskForm):
    answer = StringField('Answer: ', validators = [Required(), Length(max=20)])
    submit = SubmitField("Submit")

app = Flask(__name__)
app.config["SECRET_KEY"] = 'b273ea4c91d118774f716248'
global username
username = ""
user_level = 0
leaderboard_table = []

questions_dict = {0: ("This is the 0th question", "klafdiuswenfmdksmaflifndksafnleasdkfcgjkdfmoehjds", "", []), 1: ("This is the 1th question", "answer1", "", []),
                2: ("This is the 2th question", "answer2", "", []), 3: ("This is the 3th question", "answer3", "", []),
                4: ("This is the 4th question", "answer4", "", []), 5: ("This is the 5th question", "answer5", "", []),
                6: ("This is the 6th question", "answer6", "", []), 7: ("This is the 7th question", "answer7", "", []),
                8: ("This is the 8th question", "answer8", "", []), 9: ("This is the 9th question", "answer9", "", []),
                10: ("This is the 10th question", "answer10", "", []), 11: ("This is the 11th question", "answer11", "", []),
                12: ("This is the 12th question", "answer12", "", []), 13: ("This is the 13th question", "answer13", "", []),
                14: ("This is the 14th question", "answer14", "", []), 15: ("This is the 15th question", "answer15", "", [])}

questions_dict = {0: ("https://pastebin.com/efLJTvGW, akshay kumar is a great athlete", "vikramarkudu", "", []), 1: ("Hatxcxryuzxklccszoe", "saippuakivikauppias", "", [""]),
                2: ("R zn mlg z, Xwzc2TYH", "discodancer", "", []), 3: ("QW5jaWVudCB0aW1lcyB3ZXJlIGRpZmZlcmVudCwgbG92ZSBsZWFkcyB0byB3YXIg", "gahadavala", "", ["jayachandra.com"]),
                4: ("LzuyMJgbVUEinPOgLJ5aVT1uqPjtn3IwnPOwnTSbnKyyVUEinPOgMJuhLKDtn2SlVTS1pvOwnTIyovOfMD", "cryptx", "", ["bit.ly/kotafactory"]), 5: ("DN BYQ IM IKIPRUNR TB LKYIKFNMI, DN'Q Y HLHDDN, DN'Q Y OQUGP RN'T QMG NUN QKM PHPIGM ZKG GTTN", "vasilievich", "", []),
                6: ("ls blf'ev yllpvw blfi hklg! yvrmt kirnfh rh oryvizgrmt. yfg dzrg, dszg'h gsv wzgv?", "5K4W6rqBFWDnAN6FQUkS6x", "Vigenere JlMFCDFy", ["042018"]), 7: ("V - IX VIII IV IV IX - II", "teslawarszawa2020", "", []),
                8: ("Ger is such a hard man! Especially when it's worth a billion dollars! Es begann Anfang der 1990er Jahre in Berlin. Eine Sache, in der ich gut war, war Computer programmierung.", "rolandemmerich", "a R F d 7 J 7 q", ["terravision"]), 9: ("drive.google.com/file/d/1jytevgwrI0LqWU8k2b1qcdSwQaTfN24V/view?usp=sharing + bit.ly/SeCoNd", "stiftung", "", []),
                10: ("file d 17MMau1yTj2te6Y_IV5b4d1hXWBzH-r09 view", "messier87", "", ["lee"]), 11: ("- .... . / .-. .. ...- .- .-.. .-. -.-- / -.-. --- -- -- . -. -.-. . --..-- / .- .-.. .-.. / .-- .- ... / - . -. ... . --..-- / .--. ..- ...- .--. / .--. .-. --. / -- ..- . --- .... --- --..-- / -..- -..- .--. / -.- .- ... .--- .-.. / .--- --.- / -.-. - .... / --.- ..- --.. .--. .-.-.-", "eukleides", "57d5dFo7oN2yUyGfSKPrRv", []),
                12: ("53 74 6f 70 20 49 6d 69 74 61 74 69 6e 67 20 6d 65 21 0a 49 74 27 73 20 6e 6f 74 20 61 20 67 61 6d 65 2e 0a 43 72 61 63 6b 20 74 68 65 20 63 6f 64 65 21 21", "entscheidungsproblem", "AFBMSDU9 6193", ["1MayNCgSRcxJIWULwwTats"]), 13: ("Jh bsz gym aonqchxlv sgx cqjzke, ncwljshbrmd ivza bvsw sjq yw shf 0g2grut5lOrJxQcoymc8dG.Uhvnubaui? Sq uos jf kauma tgsh Tekvtjpvpoc? Fuchu dwg qznb mme ph wlj hlac lcmvbh ye zbmokow! Vhbv'v xmk ymukeubb?!", "georgesimonohm", "Imagine a place where your tag is '461429133168082945'", ["writteninreverse"]),
                14: ("३२० *२५०* २८३ -४- *१८८* *३४९* -०- *१९४* This seems obscure but you know what day say, 'Koshish karne walo ki hamesha jeet hoti hai.'", "wednesday", "paste 4PTG3Z6ehGkBFwjybzWkR8", ["apple"]), 15: ("Dps okhieeovls pwhhsje wll dps doks, nced pwbs di vslosbs od uwj", "rickastley", "key=3", [])}



@app.errorhandler(404)
def error_404(e):
    return render_template('404.html', password = "false")

@app.route('/')
def home_first():
    password = "false"
    return redirect(url_for("home", password = password))

@app.route('/home/<password>')
def home(password):
    if password != "":
        password = password
    else:
        password = "false"
    return render_template("home.html", password = password)

@app.route('/format/<password>')
def format(password):
    if password != "":
        password = password
    else:
        password = "false"
    return render_template('format.html', password=password)

@app.route('/register', methods=["POST", "GET"])
def register():
    database_script.dosomething("CREATE TABLE IF NOT EXISTS userinfo (username Text, email TEXT, schoolname TEXT, password TEXT, user_level FLOAT, time INTEGER, egg_count INTEGER, fullname TEXT, discord_id TEXT)")
    register_form = RegisterationForm()
    errors_lst = []
    password = "false"
    user_to_create = {"Username": "", "Email": "", "Schoolname": "", "Password": "", "Fullname": "", "Discord ID": ""}
    registration_complete_html = ["", ""]
    rows = database_script.view_userinfo()

    if register_form.validate_on_submit():

        user_to_create = {"Username": register_form.username.data, "Email": register_form.email.data, "Schoolname": register_form.schoolname.data, "Password": sha256_crypt.encrypt(register_form.password.data), "Fullname": register_form.fullname.data, "DiscordID": register_form.discordid.data}

        if rows != [] and rows != None:
            for row in rows:
                if user_to_create["Username"] == row[0]:
                    errors_lst.append("Username: This username is already taken. Please write a different one.")

        if len(errors_lst) == 0:
            user_to_create_command_str = "INSERT INTO userinfo VALUES('%s', '%s', '%s', '%s', %s, %s, %s, '%s', '%s')" % (user_to_create["Username"], user_to_create["Email"], user_to_create["Schoolname"], user_to_create["Password"], 0, 0, 0, user_to_create["Fullname"], user_to_create["DiscordID"])
            database_script.dosomething(user_to_create_command_str)
            print(user_to_create)
            password = user_to_create["Password"]
            password = str(password).replace('.', 'stp')
            password = str(password).replace('/', 'slsh')
            registration_complete_html = ["Congratulations! You have registered successfully. Now all you have to do is wait for competition day.Best of luck!", "Go Back Home"]

    if register_form.errors != {}:
        for error_msg, field_name in zip(register_form.errors.values(), register_form.errors.keys()):
            errors_lst.append(field_name[0].upper() + field_name[1:] + ": " + error_msg[0])

    return render_template("register.html", password = password, register_form = register_form, errors_lst = errors_lst, registration_complete_text = registration_complete_html[0], registration_complete_button = registration_complete_html[1])

@app.route('/login', methods=["POST", "GET"])
def signin():
    print('Login start')
    questions_text = ""
    leaderboard_text = ""
    error_text = ""
    rows = database_script.view_userinfo()
    signin_form = SigninForm()

    if signin_form.validate_on_submit():
        signin_input = [signin_form.signin_username.data, signin_form.signin_password.data]
        for row in rows:
            if row[0] == signin_input[0]:
                if sha256_crypt.verify(signin_input[1], row[3]):
                    questions_text = "Questions"
                    leaderboard_text = "Leaderboard"
                    username = row[0]
                    password = row[3]
                    password = str(password).replace('.', 'stp')
                    password = str(password).replace('/', 'slsh')
                    return redirect(url_for('questions', password = password))

        error_text = "Wrong username or password entered. Please try again."

    return render_template("login.html", signin_form=signin_form, questions_text = questions_text, leaderboard_text = leaderboard_text, password = "", error_text = error_text)

@app.route('/leaderboard/<password>')
def leaderboard(password):
    leaderboard_list = []
    rows = database_script.view_userinfo()
    for row in rows:
        if row[0] != "AzTechClub":
            leaderboard_list.append([row[0], row[4], row[5]])
        # if int(str(row[4])[0]) > 10:
            # leaderboard_list.append([row[0], 10, row[5]])
        # else:
            # leaderboard_list.append([row[0], row[4], row[5]])

    leaderboard_list.sort(key=lambda value: value[1], reverse=True)
    leaderboard_list2 = []
    leaderboard_list3 = []

    for x in range(1, 17):
        lst1 = []
        lst2 = []
        lst3 = []
        for value in leaderboard_list:
            if math.floor(value[1]) == 16 - x:
                if value[1] > 16.1 - x:
                    lst1.append(value)
                elif value[1] > 16 - x:
                    lst2.append(value)
                else:
                    lst3.append(value)
        leaderboard_list2.append(lst1)
        leaderboard_list2.append(lst2)
        leaderboard_list2.append(lst3)

    for lst in leaderboard_list2:
        lst.sort(key=lambda value: value[2], reverse=False)

    for lst in leaderboard_list2:
        for value in lst:
            leaderboard_list3.append(value)

    leaderboard_list3 = [[item[0], round(int(item[1]*10))*10, item[2]] for item in leaderboard_list3]

    print(leaderboard_list3)

    password = str(password).replace('.', 'stp')
    password = str(password).replace('/', 'slsh')
    return render_template("leaderboard.html", password=password, leaderboard_list=leaderboard_list3)

@app.route('/play/<password>', methods=['GET', 'POST'])
def questions(password):
    user_level = None
    end_text=""
    error = ""
    password = str(password).replace('stp', '.')
    password = str(password).replace("slsh", "/")
    rows = database_script.view_userinfo()
    for row in rows:
        if password == row[3]:
            username = row[0]
            user_level = row[4]
            egg_count = row[6]

    if user_level != None:

        if math.floor(user_level) < 15:
            user_problem = questions_dict[int(math.floor(user_level))][0]
            user_answer = questions_dict[math.floor(user_level)][1]
            hidden = questions_dict[math.floor(user_level)][2]
            user_eggs = questions_dict[math.floor(user_level)][3]
            answer_form = AnswerForm()
            verify = ""

        elif math.floor(user_level) >= 15:
            user_problem = ""
            user_answer = ""
            hidden = ""
            answer_form = AnswerForm()
            verify = ""
            error = ""
            end_text = "All Done!"

        if answer_form.validate_on_submit:
            if answer_form.answer.data != None:
                print(username + ": " + answer_form.answer.data + " ----- Level: " + str(user_level))
                if answer_form.answer.data == user_answer:
                    user_level = user_level + 1
                    add_command = "UPDATE userinfo SET user_level=%s, time=%s WHERE username='%s'" % (user_level, time.time(), username)
                    database_script.dosomething(add_command)
                    if user_level > 10:
                        database_script.dosomething(add_command)
                        password = str(password).replace('.', 'stp')
                        password = str(password).replace('/', 'slsh')
                        add_command = "UPDATE userinfo SET egg_count=%s WHERE username='%s'" % (0, username)
                        database_script.dosomething(add_command)
                        return redirect(url_for('questions', password = password, end_text = end_text))
                    else:
                        password = str(password).replace('/', 'slsh')
                        password = str(password).replace('.', 'stp')
                        add_command = "UPDATE userinfo SET egg_count=%s WHERE username='%s'" % (0, username)
                        database_script.dosomething(add_command)
                        return redirect(url_for('questions', password = password))

                elif answer_form.answer.data in user_eggs:
                    if egg_count != 1:
                        user_level = user_level + 0.1
                        egg_count += 1
                        add_command = "UPDATE userinfo SET user_level=%s, time=%s, egg_count=%s WHERE username='%s'" % (user_level, time.time(), egg_count, username)
                        database_script.dosomething(add_command)
                        error = "Ho Ho Ho! You got one of Santa's Bells! But incorrect answer. Please try again."
                    else:
                        error = "You already got that bell. Incorrect answer. Please try again."
                else:
                    error = "Incorrect answer. Please try again."
            else:
                error = ""
        password = str(password).replace('/', 'slsh')
        password = str(password).replace('.', 'stp')
        verify = "Sometimes the best hiding place is one right in plain sight."
        return render_template("questions.html", answer_form = answer_form, password=password, error = error, user_level = str(math.floor(user_level)), user_problem = user_problem, hidden = hidden, verify = verify, end_text = end_text)

    else:
        return redirect(url_for("home", password="false"))

if __name__ == "__main__":
    app.run(debug=False)