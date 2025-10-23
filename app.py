from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from DAL import init_db, get_all_projects, add_project, delete_project

app = Flask(__name__)

# Initialize the database on startup
init_db()


@app.route('/')
def index():
    return render_template('home.html', title="Homepage")

@app.route('/about')
def about():
    return render_template('about.html', title="About Me")

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Resume")

@app.route('/projects')
def projects():
    projects = get_all_projects()
    return render_template('projects.html', title="Projects — Queeny Chen", projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission - redirect to thank you page
        return redirect(url_for('thank_you'))
    
    return render_template('contact.html', title="Contact")

@app.route('/add', methods=['GET', 'POST'])
def add_project_route():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_file_name = request.form['image_file_name']
        
        add_project(title, description, image_file_name)
        return redirect(url_for('projects'))
    
    return render_template('add_project.html', title="Add Project")

@app.route('/delete/<int:project_id>')
def delete_project_route(project_id):
    delete_project(project_id)
    return redirect(url_for('projects'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    # Bind to 0.0.0.0 so the app is reachable from outside the container
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', debug=debug)
