from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app import app


@app.route('/create-week/<program_id>', methods=['POST'])
def create_week(program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Retrieve data from form
    week_data = dict(request.form)
    # Add user_id into retrieved data
    week_data['program_id'] = program_id

    program = program_module.Program.get_by_id(program_id)

    # Get week ID when creating a new week
    week_id = week_module.Week.create_week(week_data)
    # Create week object by using week id
    week = week_module.Week.get_week_by_id(week_id)

    program.weeks.append(week)
    print(f"These are the weeks in the program {program.weeks}")

    return redirect(url_for('view_program_page', program_id=program_id))