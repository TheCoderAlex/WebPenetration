from flask import Flask, render_template
from app.views import views


@views.route('/')
def index():
    return render_template('index.html')