from flask import render_template, request, redirect, url_for, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

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
            flash('Post został dodany pomyślnie!')
        else:
            form.populate_obj(entry)
            db.session.commit()
            flash('Post został zmieniony pomyślnie!')
    else:
        return form.errors

@app.route("/new-post/", methods=["GET", "POST"])
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
