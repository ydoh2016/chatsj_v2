# -*- coding: utf-8 -*-

from datetime import timedelta

from app import create_app, socketio

app = create_app(debug=True)
app.secret_key = 'my_fuckin_key'  # secret_key는 서버상에 동작하는 어플리케이션 구분하기 위해 사용하고 복잡하게 만들어야 합니다.
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1) # 로그인 지속시간을 정합니다. 현재 1분
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)