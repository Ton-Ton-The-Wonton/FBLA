"""main module"""

import sys
import os
import argparse  # Parse/handle command line arguments

from app.__init__ import app, Base, engine
from controller.index_controller import index_bp
from controller.partner_controller import partner_bp

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

parser = argparse.ArgumentParser(description="Please specify an environment")
parser.add_argument("env", type=str, help="Input env: dev, prod")
args = parser.parse_args()
os.environ["env"] = args.env

app.register_blueprint(partner_bp)  # import bp
app.register_blueprint(index_bp)  # import index_bp

Base.metadata.create_all(bind=engine)

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=9999, threaded=True, debug=True)
