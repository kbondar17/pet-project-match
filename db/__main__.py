import logging


from typer import Typer

from db.session import create_db, db_session, reset_db

app = Typer()
logger = logging.getLogger(__name__)


@app.command()
def reset():
    reset_db()
    logger.debug('Удалили базу!')


@app.command()
def create():
    create_db()
    print('Создали базку')
    logger.debug('Создали базку!')


if __name__ == '__main__':
    app()
