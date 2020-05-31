from os import getenv as __getenv, path as __path

LISTEN_ADDR = __getenv('LISTEN_ADDR', '0.0.0.0')
LISTEN_PORT = int(__getenv('LISTEN_PORT', '8080'))

GIT_REPO_URL_PREFIX = __getenv('GIT_REPO_PREFIX', 'https://github.com/fluxcd/flux-get-started/blob/master/')

TEAMS_WEBHOOK = __getenv('TEAMS_WEBHOOK_URL', '')

CARD_TEMPLATE_DIR = __path.join(__path.dirname(__file__), 'card_templates')
