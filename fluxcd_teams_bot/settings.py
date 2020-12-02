import logging
from os import getenv as __getenv
from os import path as __path

LOG_LEVEL = logging.getLevelName(__getenv("LOG_LEVEL", "INFO").upper())

LISTEN_ADDR = __getenv("LISTEN_ADDR", "0.0.0.0")
LISTEN_PORT = int(__getenv("LISTEN_PORT", "8080"))

GIT_REPO_URL_PREFIX = __getenv("GIT_REPO_PREFIX", "https://github.com/fluxcd/flux-get-started/blob/master/")
FLUX_TOKEN = __getenv("FLUX_TOKEN", None)

TEAMS_WEBHOOK = __getenv("TEAMS_WEBHOOK_URL", "")

CARD_TEMPLATE_DIR = __path.join(__path.dirname(__file__), "card_templates")
