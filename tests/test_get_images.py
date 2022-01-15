from tests.BaseCase import BaseCase
import io


class TestImageGet(BaseCase):
    def test_empty_response(self):
        response = self.app.get("/images")
        self.assertListEqual(response.json, [])
        self.assertEqual(response.status_code, 200)

    def test_image_not_found(self):
        response = self.app.get("/images/asdf")

        self.assertEqual(response.status_code, 404)
        self.assertEqual("Image not found", response.data.decode("utf-8"))

    def test_image_response(self):
        data = {
            "name": "test_image",
            # "name": "",
            "image-url": "https://media.istockphoto.com/photos/sea-otter-on-ice-enhydra-lutris-prince-william-sound-alaska-in-front-picture-id1283550298?b=1&k=20&m=1283550298&s=170667a&w=0&h=ri6Mksaesf8fs4rcAQArPoG_m8YEu78piNHjVMBc3jI=",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        response = self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        image_id = response.json[0]["id"]

        response = self.app.get("/images/{}".format(image_id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_image", response.json[0]["name"])

    def test_image_objects(self):
        data = {
            "name": "test_image",
            # "name": "",
            "image-url": "https://media.istockphoto.com/photos/sea-otter-on-ice-enhydra-lutris-prince-william-sound-alaska-in-front-picture-id1283550298?b=1&k=20&m=1283550298&s=170667a&w=0&h=ri6Mksaesf8fs4rcAQArPoG_m8YEu78piNHjVMBc3jI=",
            "object-detection": "on",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        data = {
            # "name": "test_image",
            "name": "",
            "image-url": "https://media.istockphoto.com/photos/sea-otter-british-columbia-picture-id507171882?b=1&k=20&m=507171882&s=170667a&w=0&h=j6RDmP-Gz0M9xG1JYPy8QMlXjdPCzOjFV_vi0GjvCyU=",
            "object-detection": "on",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        response = self.app.get('/images?objects="otter"')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertGreater(len(response.json[0]["tags"]), 0)
        self.assertIn("otter", response.json[0]["tags"])

    def test_images_response(self):
        data = {
            "name": "test_image",
            # "name": "",
            "image-url": "https://media.istockphoto.com/photos/sea-otter-on-ice-enhydra-lutris-prince-william-sound-alaska-in-front-picture-id1283550298?b=1&k=20&m=1283550298&s=170667a&w=0&h=ri6Mksaesf8fs4rcAQArPoG_m8YEu78piNHjVMBc3jI=",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )

        response = self.app.get("/images")

        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_image", response.json[0]["name"])
