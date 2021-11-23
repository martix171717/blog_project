from flask import render_template, request, redirect, url_for, flash, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm, DeleteForm
import functools
from sqlalchemy import or_

@app.route("/")
def index():
      all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
      return render_template("homepage.html", all_posts=all_posts)

def create_edit_entry(form, entry_id=None, entry=None):
    if form.validate_on_submit():
        if entry_id == None:
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            if form.is_published.data==True:
                flash('Post został dodany pomyślnie!')
            else:
                flash('Szkic został dodany pomyślnie!')  
        else:
            form.populate_obj(entry)
            db.session.commit()
            if form.is_published.data==True:
                flash('Post został zmieniony pomyślnie!')
            else:
                flash('Szkic został zmieniony pomyślnie!')
    else:
        return form.errors

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        create_edit_entry(form)
        return redirect(url_for('index'))
    else:
        errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        create_edit_entry(form, entry_id=entry_id, entry=entry)
        return redirect(url_for('index'))
    else:
        errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('Zostałeś poprawnie zalogowany!', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Zostałeś poprawnie wylogowany!', 'success')
    return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Post został skasowany pomyślnie', 'success')
    return redirect(url_for('index'))

@app.route('/search/', methods=['GET'])
def search():
    errors = None
    form = EntryForm()
    search_query = request.args.get("q", "")
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    if search_query:
        posts = Entry.query.filter(
            or_(
                Entry.title.like('%' + search_query + '%'), 
            Entry.body.like('%' + search_query + '%'))
        )
        return render_template("search.html", posts=posts, search_query=search_query)
    else:
        errors = form.errors
    return render_template("homepage.html", form=form, errors=errors)


@app.route("/post/<int:entry_id>", methods=['GET'])
def entry_details(entry_id):
      entry = Entry.query.filter_by(id=entry_id).first_or_404()
      return render_template("details.html", entry=entry)

