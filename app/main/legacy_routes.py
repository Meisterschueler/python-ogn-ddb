from io import StringIO
import csv
from flask import request, make_response
from app import db
from app.models import Device
from app.main import bp


@bp.route("/download")
def download():
    t = request.args.get("t")
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

    output = StringIO()

    header_writer = csv.writer(output)
    csv_header = ["#DEVICE_TYPE", "DEVICE_ID", "AIRCRAFT_MODEL", "REGISTRATION", "CN", "TRACKED", "IDENTIFIED", "AIRCRAFT_TYPE" "AIRCRAFT_TYPE"]
    header_writer.writerow(csv_header if t else csv_header[:-1])

    row_writer = csv.writer(output, quotechar="'", quoting=csv.QUOTE_ALL)
    for device in db.session.query(Device).filter(*filter_args):
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


@bp.route("/download-fln.php")
def download_fln():
    # devices = Device.query.filter_by(show_track=True).filter_by(show_identity=True).all()
    # return render_template("index.html")
    pass
