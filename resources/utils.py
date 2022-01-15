import re
from database.models import Tag
import requests
from flask import url_for

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
ALLOWED_CONTENT_TYPE = set(["image/jpeg", "image/png", "image/gif"])


def get_filters(objects):
    object_string = objects.strip('"')
    filters = object_string.split(",")
    filters = [s.lstrip().rstrip() for s in filters]
    return filters


def get_tags(filters):
    tags = []
    for filter in filters:
        tag = Tag.objects(name=filter).first()
        tags.append(tag)
    return tags


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_content_type(headers):
    return headers.get("content-type").lower() in ALLOWED_CONTENT_TYPE


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get("content-type")
    if "text" in content_type.lower():
        return False
    if "html" in content_type.lower():
        return False
    return True


def prettify_data(data):
    all_images = []
    for image in data:
        all_images.append(
            {
                "id": str(image.id),
                "name": image.name,
                "tags": [tag.name for tag in image.tags],
                "url": url_for("file", image_id=image.id, _external=True),
            }
        )
    return all_images
