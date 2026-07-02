import uvicorn
from src.api.app import app
import config


def main():
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)


if __name__ == "__main__":
    main()
