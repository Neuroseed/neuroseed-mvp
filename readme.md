# Neuroseed Platform Alpha - WEB API

Release Version 0.1.0

## Dependencies

* pyramid

## Development

```bash
pserve development.ini --reload
```

### Tests

Install dependencies:

```bash
pip3 install -e ".[testing]"
```

Run tests:

```bash
pytest -q
```

## Production

```bash
pserve production.ini --reload
```

