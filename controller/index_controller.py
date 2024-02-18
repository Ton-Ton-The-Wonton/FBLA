"""index controller"""

from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__, url_prefix='/')


@index_bp.route('/list', methods=["GET"])
def list_page():
    """list"""
    
    return render_template("list.html")


@index_bp.route('/collect', methods=["GET"])
def collect_page():
    """collect"""

    return render_template("collect.html")


@index_bp.route('/report', methods=["GET"])
def report_page():
    """report"""

    return render_template("report.html")


@index_bp.route('/navbar', methods=["GET"])
def navbar():
    """navbar"""

    return render_template("navbar.html")


@index_bp.route('/instruction', methods=["GET"])
def instruction():
    """instruction"""

    return render_template("instruction.html")
