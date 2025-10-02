from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Project, WordCount
from . import db, login_manager
from sqlalchemy.exc import IntegrityError
from datetime import date

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('base.html')
    else:
        return redirect(url_for('main.login'))

@main.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(url_for('main.dashboard'))
        flash('Invalid Credentials')
    return render_template('login.html')

@main.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

#display projects on dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    projects = current_user.projects
    return render_template('dashboard.html', projects = projects)

#creating project path
@main.route('/projects/new', methods = ['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title:
            flash("title is required.", "error")
            return render_template("new_project.html", title=title, description=description), 400

        if len(title)>200:
            flash("Title is too long (max 200 chars).", "error")
            return render_template("new_project.html", title = title, description=description), 400
        

        project = Project(title = title, description = description, user_id = current_user.id)

        try:
            db.session.add(project)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Could not create project(database error).", "error")
            return render_template("new_project.html", title = title, description = description), 500

        flash("Project created!", "success")
        return redirect(url_for("main.dashboard")) #change this to main.view_project later, for now main.dashboard for convinience

    return render_template("new_project.html")

@main.route('/projects/<int:project_id>/save', methods=['POST'])
@login_required
def save_project(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        abort(403)

    project.content = request.form['content']
    db.session.commit()

    flash("Project saved!", "success")
    return redirect(url_for('open_project', project_id=project.id))


@main.route('/projects/<int:project_id>')
@login_required
def view_project(project_id):
    project=Project.query.get_or_404(project_id)

    if project.user_id!=current_user.id:
        flash("You don't have permission to view this project.", "danger")
        return redirect(url_for("main.dashboard"))
    
    return render_template("view_project.html", project = project)

@main.route("/projects/<int:project_id>/update_wordcount", methods = ["POST"])
@login_required
def update_wordcount(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("Not your project!", "danger")
        return redirect(url_for("main.dashboard"))
    
    words_written = request.form.get("words_written", type = int)

    entry = WordCount.query.filter_by(project_id=project_id, date=date.today()).first()

    if entry:
        entry.words_written+=words_written
    else:
        entry = WordCount(project_id=project_id, words_written=words_written)
        db.session.add(entry)

    db.session.commit()
    flash("Word Count Updated", "success")
    return redirect(url_for ("main.view_project", project_id = project_id))


@main.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('main.login'))

