from io import StringIO
import csv
import re
from flask import request, make_response, jsonify
from app import db
from app.models import Device
from app.main import bp


@bp.route("/download")
def download():
    t = request.args.get("t")
    j = request.args.get("j")
    device_id = request.args.get("device_id")
    from_id = request.args.get("from_id")
    till_id = request.args.get("till_id")
    registration = request.args.get("registration")
    cn = request.args.get("cn")

    filter_args = []
    if device_id:
        filter_args = [Device.address.in_(device_id.split(","))]
    elif from_id and till_id:
        filter_args = [Device.address >= from_id, Device.address <= till_id]
    elif from_id:
        filter_args = [Device.address >= from_id]
    elif till_id:
        filter_args = [Device.address <= till_id]
    elif registration:
        filter_args = [Device.registration.in_(registration.split(","))]
    elif cn:
        filter_args = [Device.cn.in_(cn.split(","))]

    devices = db.session.query(Device).filter(*filter_args).order_by(Device.address)
    if j:
        output = []
        for device in devices:
            show = device.show_track and device.show_identity
            data = {"device_type": device.device_type.name[0],
                    "device_id": device.address,
                    "aircraft_model": device.aircraft_type.name if show else "",
                    "registration": device.registration if show else "",
                    "cn": device.cn if show else "",
                    "tracked": "Y" if device.show_track else "N",
                    "identified": "Y" if device.show_identity else "N"
                    }
            if t:
                data["aircraft_type"] = str(device.aircraft_type.category.value)

            output.append(data)

        return jsonify({"devices": output})
    else:
        output = StringIO()

        header_writer = csv.writer(output, lineterminator='\n')
        csv_header = ["#DEVICE_TYPE", "DEVICE_ID", "AIRCRAFT_MODEL", "REGISTRATION", "CN", "TRACKED", "IDENTIFIED", "AIRCRAFT_TYPE"]
        header_writer.writerow(csv_header if t else csv_header[:-1])

        row_writer = csv.writer(output, quotechar="'", quoting=csv.QUOTE_ALL, lineterminator='\n')
        for device in devices:
            if device.show_track and device.show_identity:
                csv_data = [
                    device.device_type.name[0],
                    device.address,
                    device.aircraft_type.name,
                    device.registration,
                    device.cn,
                    "Y" if device.show_track else "N",
                    "Y" if device.show_identity else "N",
                    device.aircraft_type.category.value,
                ]
            else:
                csv_data = [
                    device.device_type.name[0],
                    "", "", "", "",
                    "Y" if device.show_track else "N",
                    "Y" if device.show_identity else "N",
                    device.aircraft_type.category.value,
                ]
            row_writer.writerow(csv_data if t else csv_data[:-1])

        # return file text/csv
        '''
        buffer = BytesIO()
        buffer.write(output.getvalue().encode("utf-8"))
        buffer.seek(0)
        return send_file(buffer, mimetype="text/comma-separated-values", attachment_filename="ddb.csv", as_attachment=True)
        '''

        # return text/plain
        response = make_response(output.getvalue().encode("utf-8"), 200)
        response.mimetype = "text/plain"
        return response


def _encode_string(string, width):
    return ''.join(["{0:02x}".format(ord(c)) for c in re.sub(r'[^\x00-\x7F]+', '?', string[:width]).ljust(width)])


@bp.route("/download/download-fln.php")
def download_fln():
    lines = ["002c38"]                                    # version

    for device in Device.query.filter(Device.show_track and Device.show_identity).order_by(Device.address):
        parts = [
            _encode_string(device.address, 6),               # address
            _encode_string('', 21),                          # owner
            _encode_string('', 21),                          # airport
            _encode_string(device.aircraft_type.name, 21),   # aircraft
            _encode_string(device.registration, 7),          # registration
            _encode_string(device.cn, 3),                    # cn
            _encode_string('', 7)                            # frequency
        ]
        lines.append(''.join(parts))

    # return text/plain
    response = make_response('\n'.join(lines), 200)
    response.mimetype = "text/plain"
    return response
