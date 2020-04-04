import unittest
import json
import codecs
from app.filldata import import_fakedata
from .base import TestCaseBase


class TestLegacy(TestCaseBase):
    def test_download(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.charset, 'utf-8')
            self.assertEqual(response.mimetype, 'text/plain')
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y'\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y'\n"
                "'F','DD4711','ASH-25','D-4711','11','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_t(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?t=1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.charset, 'utf-8')
            self.assertEqual(response.mimetype, 'text/plain')
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED,AIRCRAFT_TYPE\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y','1'\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y','1'\n"
                "'F','DD4711','ASH-25','D-4711','11','Y','Y','1'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_j(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?j=1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.charset, 'utf-8')
            self.assertEqual(response.mimetype, 'application/json')
            self.assertTrue(response.is_json)
            data = response.get_data()
            json_data = json.loads(data)

            shouldbe = {
                "devices": [
                    {"aircraft_model": "Rhönlärche Ил-32", "cn": "TO", "device_id": "ABCDEF", "device_type": "O", "identified": "Y", "registration": "D-OTTO", "tracked": "Y"},
                    {"aircraft_model": "ASK-13", "cn": "34", "device_id": "DD1234", "device_type": "F", "identified": "Y", "registration": "D-1234", "tracked": "Y"},
                    {"aircraft_model": "ASH-25", "cn": "11", "device_id": "DD4711", "device_type": "F", "identified": "Y", "registration": "D-4711", "tracked": "Y"},
                ]}

            self.assertEqual(json_data, shouldbe)

    def test_download_j_t(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?j=1&t=1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.charset, 'utf-8')
            self.assertEqual(response.mimetype, 'application/json')
            self.assertTrue(response.is_json)
            data = response.get_data()
            json_data = json.loads(data)

            shouldbe = {
                "devices": [
                    {"aircraft_model": "Rhönlärche Ил-32", "cn": "TO", "device_id": "ABCDEF", "device_type": "O", "identified": "Y", "registration": "D-OTTO", "tracked": "Y", "aircraft_type": "1"},
                    {"aircraft_model": "ASK-13", "cn": "34", "device_id": "DD1234", "device_type": "F", "identified": "Y", "registration": "D-1234", "tracked": "Y", "aircraft_type": "1"},
                    {"aircraft_model": "ASH-25", "cn": "11", "device_id": "DD4711", "device_type": "F", "identified": "Y", "registration": "D-4711", "tracked": "Y", "aircraft_type": "1"},
                ]}

            self.assertEqual(json_data, shouldbe)

    def test_download_device_id(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?device_id=DD1234,ABCDEF', follow_redirects=True)
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y'\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_from_id(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?from_id=DD1234', follow_redirects=True)
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y'\n"
                "'F','DD4711','ASH-25','D-4711','11','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_till_id(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?till_id=DD1234', follow_redirects=True)
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y'\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_registration(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?registration=D-4711,D-OTTO', follow_redirects=True)
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y'\n"
                "'F','DD4711','ASH-25','D-4711','11','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_cn(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download?cn=34,TO', follow_redirects=True)
            data = response.get_data().decode('utf-8')

            shouldbe = (
                "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n"
                "'O','ABCDEF','Rhönlärche Ил-32','D-OTTO','TO','Y','Y'\n"
                "'F','DD1234','ASK-13','D-1234','34','Y','Y'\n"
            )

            self.assertEqual(data, shouldbe)

    def test_download_fln(self):
        import_fakedata()
        with self.app.test_client() as c:
            response = c.get(f'/download/download-fln.php', follow_redirects=True)
            data = response.get_data().decode('utf-8')
            decoded_data = '\n'.join(codecs.decode(line, "hex").decode('utf-8') for line in data.split('\n')[1:])

            shouldbe = (
                "ABCDEF                                          Rh?nl?rche ?-32      D-OTTO TO        \n"
                "DD1234                                          ASK-13               D-1234 34        \n"
                "DD4711                                          ASH-25               D-4711 11        "
            )

            self.assertEqual(decoded_data, shouldbe)


if __name__ == "__main__":
    unittest.main()
