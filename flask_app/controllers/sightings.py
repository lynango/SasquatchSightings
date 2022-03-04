from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

#Directs the user to a new page in order to report the new sighting.
@app.route('/new/sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_sighting.html',user=User.get_by_id(data))

#Process the user's request to report a new sighting.
@app.route('/report/sighting',methods=['POST'])
def report_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting_report(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "num_of_sasquatches": request.form["num_of_sasquatches"],
        "reporter": request.form["reporter"],
        "user_id": session["user_id"]
    }
    Sighting.save(data)
    return redirect('/dashboard')

#Directs the user to a new page in order to edit their reported sighting.
@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_sighting.html",edit=Sighting.get_one(data),user=User.get_by_id(user_data))

#Process the user's request to update the reported sighting. 
@app.route('/update/sighting',methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Sighting.validate_sighting_report(request.form):
        return redirect('/edit/sighting/<int:id>')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "num_of_sasquatches": request.form["num_of_sasquatches"],
        "reporter": request.form["reporter"],
        "id": request.form['id']
    }
    Sighting.update(data)
    return redirect('/dashboard')

#Directs the user to a new page in order to view/read the reported sighting.
@app.route('/sighting/<int:id>')
def show_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }

    user_data = {
        "id":session['user_id']
    }
    # one_user = User.get_one(data)
    # sightings = Sighting.get_one(data)
    return render_template("show_sighting.html", sighting = Sighting.get_one(data), user=User.get_by_id(user_data))

    # sighting = Sighting.get_one(data), user=User.get_by_id(user_data)

#Process the user's request to delete one of their reported sightings.
@app.route('/delete/sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Sighting.delete(data)
    return redirect('/dashboard')

