import os
from flask import Flask
from apply_helper.config import Config, logger
from apply_helper.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_routes(app)
    return app

if __name__ == '__main__':
    from assistant import create_assistant

    app = create_app()
    logger.debug(f"app created")
    if not os.path.exists(os.path.abspath(Config.UPLOAD_FOLDER)):
        logger.debug(f"Error: No directory exists {Config.UPLOAD_FOLDER}")
        upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        try:
            os.makedirs(upload_folder, exist_ok=True)
        except PermissionError:
            logger.debug(f"Error: No permission to create directory at {upload_folder}")
            raise
        except Exception as e:
            logger.debug(f"Error creating directory {upload_folder}: {str(e)}")
            raise
    logger.debug(f"file path created")
    Config.ASSISTANT_ID = create_assistant()
    app.run(debug=True)
