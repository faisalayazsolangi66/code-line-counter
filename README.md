# code-line-counter

Count lines of code by language in a project directory, split into code, blank, and comment lines.

## Requirements

- Python 3 (standard library only — no third-party packages)

## How to run

```bash
cd 054-code-line-counter
python3 main.py /path/to/project
```

Run `python3 main.py --help` to see all options.

## Example

```bash
python3 main.py /path/to/project
```

Sample output:

```
Language       Files   Total    Code   Blank  Comment
------------------------------------------------------
Python             2      42      30       5        7
JavaScript         1      18      15       2        1
------------------------------------------------------
TOTAL              3      60      45       7        8
```

## Notes

Skips `.git`, `node_modules`, `venv`, `__pycache__`, `dist`, `build`, and similar directories. Use `--ignore` for extra directories, `--extensions '.vue:Vue'` for extra mappings, and `--sort files|name` to change the order.

## License

MIT — see [LICENSE](LICENSE).
