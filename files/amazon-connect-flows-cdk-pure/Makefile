.PHONY: help install install-dev test lint format validate clean deploy destroy synth diff

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests with coverage"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make validate      - Validate configs and flows"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make synth         - Synthesize CloudFormation"
	@echo "  make diff          - Show deployment diff"
	@echo "  make deploy        - Deploy to dev environment"
	@echo "  make deploy-prod   - Deploy to production"
	@echo "  make destroy       - Destroy dev stacks"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest --cov=stacks --cov=utils/connect_flows --cov-report=html --cov-report=term

lint:
	flake8 stacks/ utils/connect_flows/ tests/ --max-line-length=120
	mypy stacks/ utils/connect_flows/

format:
	black stacks/ utils/connect_flows/ tests/ scripts/

validate:
	python scripts/validate_configs.py
	python scripts/validate_flows.py

clean:
	rm -rf cdk.out
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

synth:
	cdk synth -c environment=dev

diff:
	cdk diff --all -c environment=dev

deploy:
	cdk deploy --all -c environment=dev

deploy-prod:
	cdk deploy --all -c environment=prod --require-approval broadening

destroy:
	cdk destroy --all -c environment=dev
