from flask import jsonify

from app.libs.redprint import Redprint
from app.models.config import get_value

api = Redprint('system')


@api.route('/get_default_info', methods=['POST'])
def get_default_info_api():
    return jsonify({
        'xn': get_value('default_xn'),
        'xq': get_value('default_xq')
    })
    pass
