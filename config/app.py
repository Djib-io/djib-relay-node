"""
application global configuration
"""

try:
    from os import path, environ
    from dotenv import load_dotenv

    BASEDIR = path.abspath(path.dirname(__file__) + "/..")
    load_dotenv(dotenv_path=BASEDIR + "/.env")

    TITLE = "Djib RELAY NODE"
    HOST = environ.get("FLASK_HOST")
    PORT = int(environ.get("FLASK_PORT"))
    SECRET = environ.get("FLASK_SECRET")

    PROPAGATE_EXCEPTIONS = False
    DEBUG = True

    if environ.get("FLASK_MODE") == "PRODUCTION":
        TESTING = False
        ENV = 'production'
    else:
        TESTING = True
        ENV = 'development'

    LEADER_NODE = environ.get("LEADER_NODE")
    RELAY_ID = environ.get("RELAY_PUBLIC_KEY")
    RELAY_DN = environ.get("RELAY_DN")

except Exception as e:
    print(f"Error on reading global config: {str(e)}")
    exit(1)
