lint:
	pipenv run mypy fluxcd_teams_bot
	pipenv run black -l 120 -t py38 .
	pipenv run isort .
	pipenv run flake8 --max-line-length 120
	pipenv run safety check
	pipenv run bandit -r fluxcd_teams_bot
