import os

from flask import Flask

from apply_helper.config import Config, logger
from apply_helper.routes import init_routes


def init_upload_directory(app):
    absolute_path = os.path.abspath(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(absolute_path):
        logger.debug("New directory created: %s", absolute_path)
        try:
            os.makedirs(absolute_path, exist_ok=True)
        except PermissionError:
            logger.error(
                "Error: No permission to create directory at %s", absolute_path
            )
            raise
        except Exception as e:
            logger.error(
                "Error creating directory %s, %s", absolute_path, str(e)
            )
            raise


def create_app():
    from apply_helper.assistant import create_assistant

    app = Flask(__name__)
    app.config.from_object(Config)

    init_upload_directory(app)

    Config.ASSISTANT_ID = create_assistant()
    if not Config.ASSISTANT_ID:
        logger.error("Error creating assistant id")

    init_routes(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
