from flask import session, redirect, url_for, render_template, request, Blueprint

from key.kakao_client import CLIENT_ID, REDIRECT_URI
import oauth

main = Blueprint('main', __name__)

