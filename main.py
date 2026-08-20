from dotenv import load_dotenv
from core.application import Application

load_dotenv()

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()