from distutils.command.build_scripts import first_line_re
from flask import session, redirect, url_for, render_template, request, Blueprint

from key.kakao_client import CLIENT_ID, REDIRECT_URI, SIGNOUT_REDIRECT_URI
from app.kakao_controller import Oauth

import requests

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        # session['room'] = request.form['room']
        return redirect(url_for('main.chat'))
    return render_template('index.html')


@main.route('/chat')
def chat():
    name = session.get('name', '')
    # room = session.get('room', '')
    room = "엘공팔"
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)

@main.route('/assemble')
def assemble():
    requests.get("https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code")
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=friends"
    return redirect(kakao_oauth_url)

@main.route('/callback')
def callback():
    code = request.args["code"]

    # 전달받은 authorization code를 통해서 access_token을 발급
    oauth = Oauth()
    auth_info = oauth.auth(code)
    friends = oauth.send("Bearer " + auth_info['access_token'], "message")['elements']
    uuids = list()
    for friend in friends:
        uuids.append(friend['uuid'])
    uuids = '["'+'","'.join(uuids)+'"]'
    url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    header = {"Authorization": 'Bearer ' + auth_info["access_token"]}
    import json
    data={
        'receiver_uuids': uuids,
        "template_object": json.dumps({
            "object_type":"text",
            "text":"엘공팔 어셈블!",
            "link":{
                "web_url" : "https://localhost:5001",
                "mobile_web_url" : "https://localhost:5001"
            },
            "button_title": "참여하기"
        })
    }

    response = requests.post(url, headers=header, data=data)
    response.status_code

    # # error 발생 시 로그인 페이지로 redirect
    # if "error" in auth_info:
    #     print("에러가 발생했습니다.")
    #     return {'message': '인증 실패'}, 404
    return redirect(url_for('main.chat'))

@main.route('/signout')
def kakao_sign_out():
    # 카카오톡으로 로그아웃 버튼을 눌렀을 때
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={SIGNOUT_REDIRECT_URI}"

    if session.get('email'):
        session.clear()
        value = {"status": 200, "result": "success"}
    else:
        value = {"status": 404, "result": "fail"}

    return redirect(kakao_oauth_url)