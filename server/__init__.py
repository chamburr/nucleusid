import os

import dotenv

os.environ["PROMETHEUS_MULTIPROC_DIR"] = "/tmp"

dotenv.load_dotenv(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env")),
    override=True,
)
