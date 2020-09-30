from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from functools import wraps

from ..controller import *
member = Blueprint('member',
                __name__,
                template_folder="member_templates",
                static_folder="member_templates",
                url_prefix='/member')

# @admin.route('/index')
# def index():
#     testing()
#     return "render_template('index.html')"
@member.route('/')
@member.route('/index')
def index():
    return render_template('user_index.html')

@member.route('/test')
def test():
    data = mysql_query("select * from user_type_master;")
    print(data)
    return "test Data"

