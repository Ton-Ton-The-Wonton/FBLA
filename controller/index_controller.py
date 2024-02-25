"""rendering html templates for each page"""

from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__, url_prefix='/')


@index_bp.route('/', methods=["GET"])
def list_page():
    
    return render_template("list.html")


@index_bp.route('/add', methods=["GET"])
def add_page():

    return render_template("add.html")


@index_bp.route('/report', methods=["GET"])
def report_page():

    return render_template("report.html")


@index_bp.route('/navbar', methods=["GET"])
def navbar():

    return render_template("navbar.html")


@index_bp.route('/instructions', methods=["GET"])
def instruction():

    return render_template("instructions.html")


@index_bp.route('/chatbot', methods=["GET"])
def chatbot():

    return render_template("chatbot.html")
