from tests.BaseCase import BaseCase
import io


class TestImaggaAPI(BaseCase):
    def test_image_tags(self):
        data = {
            "name": "test_image",
            # "name": "",
            "image-url": "https://media.istockphoto.com/photos/sea-otter-on-ice-enhydra-lutris-prince-william-sound-alaska-in-front-picture-id1283550298?b=1&k=20&m=1283550298&s=170667a&w=0&h=ri6Mksaesf8fs4rcAQArPoG_m8YEu78piNHjVMBc3jI=",
            "object-detection": "on",
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
        self.assertGreater(len(response.json[0]["tags"]), 0)
        self.assertIn("otter", response.json[0]["tags"])
