# coding:utf-8

import os
from flask import request, Blueprint, jsonify
from werkzeug.utils import secure_filename
import time

from ..settings import UPLOAD_FOLDER, UPLOAD_URL

bp = Blueprint('uploads', __name__)


@bp.route("/upload", methods=['POST'])
def upload():
    upload_file = request.files['file']
    if upload_file:
        filename = secure_filename(upload_file.filename)
        basename, extension = filename.rsplit('.', 1)
        filename = "{basename}({timestamp}).{extension}".format(basename=basename, timestamp=int(time.time()),
                                                                extension=extension)
        upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
        upload_file_url = '/'.join([UPLOAD_URL, filename])
        return jsonify(data=dict(success=True, file_url=upload_file_url))
    else:
        return jsonify(data=dict(success=False, error_code='NO_FILE'))





