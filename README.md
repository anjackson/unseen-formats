Unseen Formats
==============

Applying 'unseen species' methods to file format registries.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```


## pydistinct

Might be good to experiment with `pydistinct`, like [this](https://github.com/chanedwin/pydistinct/blob/master/demo/tutorial%20notebook.ipynb).

But note that it includes an extremely heavyweight (>300MB) dependency via `xgboost` that it doesn't seem to actually use?  A reduced version can be installed using:

```
pip install -e git+https://github.com/anjackson/pydistinct#egg=pydistinct
```

But `hatchling` doesn't like it... 

> ValueError: Dependency #6 of field `project.dependencies` cannot be a direct reference unless field `tool.hatch.metadata.allow-direct-references` is set to `true`