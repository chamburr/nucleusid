from server.app import create_app
from server.utils import config

app = create_app()


if __name__ == "__main__":
    app.run(config.SERVER_HOST, config.SERVER_PORT, debug=True)
