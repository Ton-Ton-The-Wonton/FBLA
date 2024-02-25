"""main module: entry point of the application"""

import sys
import os

from app.__init__ import app, Base, engine
from controller.index_controller import index_bp
from controller.partner_controller import partner_bp

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

# register blueprints for the app to route requests
app.register_blueprint(partner_bp)
app.register_blueprint(index_bp)

# initialize database schema
Base.metadata.create_all(bind=engine)

# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, threaded=True, debug=True)
