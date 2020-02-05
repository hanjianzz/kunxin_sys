# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

bp = Blueprint('data_center', __name__)

@bp.route('/center')
def index():
    return render_template('index.html')
