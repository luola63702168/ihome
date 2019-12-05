# coding: utf-8
from flask import Blueprint, current_app, make_response
from flask_wtf import csrf

html = Blueprint("web_html", __name__)


@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    '''提供html文件'''
    if not html_file_name:
        html_file_name = "index.html"
    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name
    csrf_token = csrf.generate_csrf()
    resp = make_response(current_app.send_static_file(html_file_name))
    resp.set_cookie("csrf_token", csrf_token)
    return resp

# todo 其实这里是将我们所有的页面都可以返回，但是很明显，有些页面在用户未登录的情况下是不可以返回的，因此，我们可以在这里添加用户是否登录的逻辑来进行页面的筛选
# todo 当然也可以对每个不可访问的页面进行ajax请求session接口，从而跳转到login.html
