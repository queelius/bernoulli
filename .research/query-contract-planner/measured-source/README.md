# Exact source snapshot used for final timings

Both files match the SHA256 values in every data/*/results.json. The current
code later fixed optional capabilities at tiny targets and normalized repeated
candidate parameters. Those paths do not change the measured inputs. Other
source files are unchanged and remain in ../code/. Reproduce this snapshot from
the repository root with:

```bash
PYTHONPATH=.research/query-contract-planner/code bernoulli-py/.venv/bin/python .research/query-contract-planner/measured-source/experiment.py --builds 64 --per-profile 32 --output .research/query-contract-planner/reproduced-measured
```

The current driver is preferred for new inputs. verify_artifacts.py rebuilds
every recorded payload and checks representative queries with the current code.
