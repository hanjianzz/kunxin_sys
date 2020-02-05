# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    return render_template('front/index.html')