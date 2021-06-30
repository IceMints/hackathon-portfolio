
import sys, os
from dotenv import load_dotenv

project_home = '.'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

project_folder = os.path.expanduser(project_home)
load_dotenv(os.path.join(project_folder, '.env'))


from app import app

if __name__ == "__main__":
    app.run()
