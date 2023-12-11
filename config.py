import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'good-luck-guessing'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'collegeThrift.db')

    from dotenv import load_dotenv
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))



