from app import create_app
from app.libs.weixin import Weixin

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        Weixin.init_menu()
