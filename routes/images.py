from flask import (
    Blueprint,
    request,
    render_template,
    send_file,
    url_for,
    redirect,
    Response,
)
from database.models import Image, Tag
from werkzeug.utils import send_file
from mongoengine.errors import NotUniqueError, ValidationError
import json
import io
import re
import requests
from resources.utils import (
    allowed_content_type,
    get_filters,
    get_tags,
    allowed_file,
    is_downloadable,
    prettify_data,
)
from resources.imagga_api import ImaggaAPI
from werkzeug.utils import secure_filename

images = Blueprint("images", __name__)


@images.route("/images", methods=["GET", "POST"])
def index():

    if request.method == "POST" and (
        "image-file" in request.files or "image-url" in request.form
    ):
        if request.files["image-file"].filename != "":
            filename = secure_filename(request.files["image-file"].filename)
            if allowed_file(filename):
                image_file = request.files["image-file"]
            else:
                return Response("File type not allowed", status=400)
        else:
            image_url = request.form["image-url"]
            try:
                if not is_downloadable(image_url):
                    return Response("URL is not downloadable", status=400)

                response = requests.get(image_url)
                if (
                    "Content-Type" not in response.headers.keys()
                    or not allowed_content_type(response.headers)
                ):
                    return Response("File type not allowed", status=400)

                image_file = io.BytesIO(response.content)
                if "Content-Disposition" in response.headers.keys():
                    fname = re.findall(
                        "filename=(.+)", response.headers["Content-Disposition"]
                    )[0]
                else:
                    fname = "untitled"
            except Exception as e:
                return Response("URL is not valid", status=400)

        # Check if the object detection is enabled
        # if enabled, then perform object detection on the image_file
        # and return the tags
        tags_list = []
        if request.form.get("object-detection"):
            imagga = ImaggaAPI(
                app.config["IMAGGA_API_KEY"], app.config["IMAGGA_API_SECRET"]
            )
            response = imagga.get_tags(image_file)
            tags = response["result"]["tags"]
            for entry in tags:
                try:
                    tag = Tag(name=entry["tag"]["en"]).save()
                except NotUniqueError:
                    tag = Tag.objects(name=entry["tag"]["en"]).first()
                tags_list.append(tag)

        # Check if a name for the file was provided
        # store the file with the given name if provided
        # use the original filename if not provided
        if request.form["name"]:
            image = Image(file=image_file, name=request.form["name"], tags=tags_list)
        else:
            try:
                filename = image_file.filename
            except AttributeError:
                filename = fname
            image = Image(
                file=image_file,
                name=filename,
                tags=tags_list,
            )
        image.save()

        all_images = prettify_data([image])
        return Response(json.dumps(all_images), mimetype="application/json", status=200)

    # Get images from the database
    if request.args.get("objects"):
        # get images according to the filters provided within the objects string
        filters = []
        tags = []
        filters = get_filters(request.args.get("objects"))
        if filters:
            tags = get_tags(filters)

        images = Image.objects(tags__all=tags)
    else:
        # get all images if no parameters are provided
        images = Image.objects()

    all_images = prettify_data(images)

    return Response(json.dumps(all_images), mimetype="application/json", status=200)

    # return render_template(
    #     "images.html",
    #     images=all_images,
    #     query=request.args.get("objects").strip('"')
    #     if request.args.get("objects")
    #     else "",
    # )


# Get image file from the database to be displayed
@images.route("/file/<image_id>", methods=["GET"])
def file(image_id):

    image = Image.objects(id=image_id).first()

    return send_file(
        io.BytesIO(image.file.read()), mimetype="image/png", environ=request.environ
    )


# Get individual image from the database given image_id
@images.route("/images/<image_id>", methods=["GET"])
def get_image(image_id):
    try:
        images = Image.objects(id=image_id)
        all_images = prettify_data(images)
    except ValidationError:
        return Response("Image not found", status=404)

    try:
        return Response(json.dumps(all_images), mimetype="application/json", status=200)
        # return render_template("image.html", image=all_images[0])
    except AttributeError:
        return Response("Image not found", status=404)
