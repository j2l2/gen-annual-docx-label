# Lunar Calendar Utilities

Small Python utilities for generating I-Kuan Tao (一貫道) lunar-calendar documents and label sheets.

## Requirements

- Python 3
- Dependencies:
  - `docx-mailmerge` - used by `gen_lunar_cal.py`
  - `lunarcalendar` - used by `gen_lunar_cal.py`
  - `lxml` - used by `gen_label.py`

On macOS/Homebrew Python, install dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install docx-mailmerge lunarcalendar lxml
```

## `gen_lunar_cal.py`

Generates a yearly lunar/solar anniversary document from `special_days.py`.

### Usage

```bash
.venv/bin/python gen_lunar_cal.py <year>
```

### Arguments

- `year` - Western year, integer between `1900` and `2100`.

### Template and Output

- Template: `仙佛紀念日.docx`
- Output: `{year} {干支}年（{生肖}年）.docx`  
  Example: `2026 丙午年（馬年）.docx`

### Example

```bash
.venv/bin/python gen_lunar_cal.py 2026
```

## `gen_label.py`

Generates one label per entry in `special_days.py` using the label template.

### Usage

```bash
.venv/bin/python gen_label.py <year> [--start N] [--preview]
```

### Arguments

- `year` - Year used in the output filename.
- `--start N` - 1-based label position to start printing from. Default: `1`.  
  Use this to skip used labels on a partial sheet.
- `--preview` - Open the generated `.docx` after creation (macOS `open`).

### Template and Output

- Template: `標籤-5167.docx`
- Output: `仙佛紀念日標籤-{year}.docx`

### Examples

Generate labels for 2027:

```bash
.venv/bin/python gen_label.py 2027
```

Start at the 5th label position and open for preview/printing:

```bash
.venv/bin/python gen_label.py 2027 --start 5 --preview
```

## Data Source

`special_days.py` defines the shared `SpecialDay` entries used by both generators, including name, etiquette, lunar date, and note.
