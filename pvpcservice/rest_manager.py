import connexion
import logging

log = logging.getLogger(__name__)


def create_app():
    """Create and config main API based on swagger yaml file."""
    app = connexion.App(
        __name__,
        specification_dir='./swagger/',
        server='flask',
        )
    app.add_api(
        'pvpc_swagger.yaml',
        strict_validation=True,
        validate_responses=True,
        )

    return app


if __name__ == '__main__':
    logging.info("Initializing PVPC REST service")
    create_app().run(port=8080)
