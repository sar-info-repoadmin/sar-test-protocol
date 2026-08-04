# SAR Washing Machine Accessibility Test Protocol

A public test protocol for evaluating the accessibility of washing machines. Each criterion has its own page, generated from [`docs/Washing Machine Accessibility Reporting Template.csv`](docs/Washing%20Machine%20Accessibility%20Reporting%20Template.csv), with a discussion thread (via [giscus](https://giscus.app), backed by GitHub Discussions) where anyone can comment or propose a change.

## Updating criteria

Edit the source CSV in `docs/`, then regenerate the `_criteria/` collection and `_data/categories.yml` (requires `pyyaml`: `python3 -m pip install pyyaml`):

```bash
python3 scripts/build_criteria.py
```

Commit and push to `main` — the site rebuilds and deploys automatically via the `Deploy Jekyll site to Pages` GitHub Actions workflow.

## Local development

```bash
bundle install
bundle exec jekyll serve
```

macOS's built-in system Ruby can fail to compile native gems (`ruby/config.h not found`) needed by Jekyll. If `bundle install` fails with that error, install a proper Ruby first, e.g. via [rbenv](https://github.com/rbenv/rbenv) or Homebrew (`brew install rbenv ruby-build && rbenv install 3.3.0`), then retry.
