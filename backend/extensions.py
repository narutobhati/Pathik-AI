from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate

migrate = Migrate()


db = SQLAlchemy()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
