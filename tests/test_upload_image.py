from tests.BaseCase import BaseCase
import io


class TestImageUpload(BaseCase):
    def test_successful_image_upload(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_image", response.json[0]["name"])

    def test_downloadable(self):
        data = {
            # "name": "test_image",
            "name": "",
            "image-url": "https://www.youtube.com/watch?v=zMhmZ_ePGiM",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        response = self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual("URL is not downloadable", response.data.decode("utf-8"))

    def test_allowed_file(self):
        data = {
            # "name": "test_image",
            "name": "",
            "image-url": "https://s2.q4cdn.com/498544986/files/doc_downloads/test.pdf",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        response = self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual("File type not allowed", response.data.decode("utf-8"))

    def test_invalid_URL(self):
        data = {
            # "name": "test_image",
            "name": "",
            "image-url": "data:image/jpeg;base64,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",
        }
        data = {key: str(value) for key, value in data.items()}
        data["image-file"] = (io.BytesIO(b"abcdef"), "")
        response = self.app.post(
            "/images",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual("URL is not valid", response.data.decode("utf-8"))
