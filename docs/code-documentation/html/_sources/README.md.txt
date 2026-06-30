# Sphinx Code Documentation

API and developer documentation for **fhir-query-validator-factory**, built with [Sphinx](https://www.sphinx-doc.org/).

## Build

From the repository root:

```bash
pip install -e ".[dev]"
make docs
```

Or from this directory:

```bash
pip install -e "..[dev]"
make html
```

Open `doc/_build/html/index.html` in a browser.

## Contents

| Section | Description |
|---------|-------------|
| Introduction | Project goals and Software Factory methodology |
| Installation | Environment setup and dependencies |
| Quick Start | Demos, tests, and workflow entry points |
| Architecture | Agents, loops, and ADK integration |
| API Reference | Autodoc-generated module and class reference |
| Security | OWASP hardening and production flags |
| Demos | CLI and ADK demonstration scripts |

User-facing specs and guides remain in the top-level [`docs/`](../docs/) folder. This `doc/` tree is the **code/API documentation** site.