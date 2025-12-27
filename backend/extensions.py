from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
