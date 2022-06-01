from flask import Blueprint

from CTFd.models import (
    db,
)
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.user import get_ip

def load(app):
    app.db.create_all()
    register_plugin_assets_directory(app, base_path="/plugins/timed_hints/assets/")
