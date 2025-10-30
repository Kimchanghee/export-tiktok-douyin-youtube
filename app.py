"""Cloud Run Buildpacks entry point."""

import os

from web.app import app as application

# Expose the Flask application under the conventional name `app`.
app = application

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    application.run(host="0.0.0.0", port=port)
