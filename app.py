from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, RegisterForm, FeedbackForm, DeleteFeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "stealthissecretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    # return redirect('/login')
    # return render_template('index.html')
    if "username" not in session:
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        return render_template('display.html', user=user)
    

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if "username" not in session:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_user = User.register(username, password, email, first_name, last_name)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('There is already an account with that username. Choose another user name or log in if you already have an account.')
                return render_template('register.html', form=form)
            session['username'] = new_user.username
            flash('Successfully Created Your Account!', "success")
            return redirect(f"/users/{new_user.username}")
        return render_template('register.html', form=form)
    else:
        return redirect(f"/users/{session['username']}")

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if "username" not in session:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.authenticate(username, password)
            if user:
                flash(f"Welcome Back, {user.username}!", "primary")
                session['username'] = user.username
                return redirect(f"/users/{user.username}")
            else:
                form.username.errors = ['Invalid username or password.']
        return render_template('login.html', form=form)
    else:
        return redirect(f"/users/{session['username']}")

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>')
def display_page(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        flash("Here's your information.", "success")
        user = User.query.get(username)
        return render_template('display.html', user=user)

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_page(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        form = FeedbackForm()
        user = User.query.get(username)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{username}")
        else:
            return render_template('feedback.html', user=user, form=form)

@app.route('/feedback/<int:feedback_id>/feedback/update', methods=['GET', 'POST'])
def update_feedback_page(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(session['username'])
        feedback = Feedback.query.get(feedback_id)
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f"/users/{feedback.username}")
        else:
            return render_template('edit_feedback.html', user=user, form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/feedback/delete', methods=['POST'])
def delete_feedback_page(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        feedback = Feedback.query.get(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
        

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete this user and any feedback """
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
    return redirect("/login")
