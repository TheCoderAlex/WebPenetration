from flask import Flask, render_template
from app.views import views


@views.route('/edit_hosts')
def edit_hosts():
    return render_template('edit_hosts.html')