# LogNexus

**LogNexus** is a foundational sentence extraction tool designed specifically for noisy, unstructured drone flight logs. It utilizes a specialized Named Entity Recognition (NER) model to robustly segment log messages into semantically whole sentences, enabling high-precision downstream forensic analysis.

## Features

* **Robust Segmentation:** Handles inconsistent punctuation and casing common in drone flight log messages.
* **Batch Processing:** Automatically processes all Excel log files in a specified input directory.
* **Flexible Output:** Exports to Excel (exploded rows for easy filtering) or JSON (nested structure for programmatic use).
* **GPU Support:** Optional CUDA acceleration for faster inference on large datasets.

---

## Folder Structure

```
└── 📁LogNexus
    └── 📁evidence
        ├── DJIFlightRecord_2024-11-10_[03-09-29].csv
        ├── DJIFlightRecord_2025-05-12_[08-01-12].csv
        ├── DJIFlightRecord_2025-05-12_[08-20-56].csv
        ├── DJIFlightRecord_2025-06-27_[03-23-15].csv
        ├── DJIFlightRecord_2025-06-27_[03-27-42].csv
        ├── DJIFlightRecord_2025-06-27_[03-31-40].csv
        ├── DJIFlightRecord_2025-06-27_[03-34-35].csv
    └── 📁lognexus
        ├── __init__.py
        ├── cli.py
        ├── core.py
        ├── model.py
        ├── utils.py
    └── 📁model
        ├── .gitattributes
        ├── config.json
        ├── model_args.json
        ├── model.safetensors
        ├── special_tokens_map.json
        ├── tokenizer_config.json
        ├── training_args.bin
        ├── vocab.txt
    └── 📁output
        ├── DJIFlightRecord_2024-11-10_[03-09-29].json
        ├── DJIFlightRecord_2025-05-12_[08-01-12].json
        ├── DJIFlightRecord_2025-05-12_[08-20-56].json
        ├── DJIFlightRecord_2025-06-27_[03-23-15].json
        ├── DJIFlightRecord_2025-06-27_[03-27-42].json
        ├── DJIFlightRecord_2025-06-27_[03-31-40].json
        ├── DJIFlightRecord_2025-06-27_[03-34-35].json
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

---


## Installation

### Prerequisites
* Python 3.8+
* PyTorch (install the version appropriate for your hardware from [pytorch.org](https://pytorch.org/))

### Install from Source
```bash
git clone https://github.com/swardiantara/LogNexus.git
cd LogNexus
pip install .
```

### Quick Start
* **Prepare Model:** Download the pre-trained simpletransformers model files into a folder (default: `./model`).

```bash
# use the below command
lognexus-download

# or, clone the model's Hugging Face repo, and copy all the files to the ./model folder
git lfs install
git clone https://huggingface.co/swardiantara/LogNexus-distilbert-base-uncased
```

* **Prepare Data:** Place your raw `.csv` flight logs in a folder (default: `./evidence`). Logs must have a `APP.tip` and `APP.warning` columns.
* **Run LogNexus:**
```bash
# Basic usage (uses defaults: ./evidence -> ./output using ./model)
lognexus
# or, if the local installation fail, use below command
python -m lognexus.cli

# Custom paths and JSON output
lognexus --input_dir /path/to/logs --output_dir /path/to/results --model_dir /path/to/NER_model --format json
# or
python -m lognexus.cli --input_dir /path/to/logs --output_dir /path/to/results --model_dir /path/to/NER_model --format json

# Enable GPU acceleration
lognexus --cuda
```

### Output Formats
#### Excel (`--format xlsx`) - Default

Duplicate rows are created for messages containing multiple sentences to allow for flat-file filtering.

| date       | time     | message                 | sentence (New Column) |
|------------|----------|-------------------------|-----------------------|
| 2024-01-01 | 12:00:01 | Battery Error. Landing. | Battery Error.        |
| 2024-01-01 | 12:00:01 | Battery Error. Landing. | Landing.              |

#### JSON (`--format json`)

```json
[
  {
    "date": "5/12/2025",
    "time": "8:27:36.34 AM",
    "message": "Failsafe RTH.; Press Brake button to cancel RTH.; RC signal lost. Returning to home.; RC signal weak. Avoid blocking antennas and adjust antenna orientation.; Downlink Restored (after 0m 5.8s).; Flight mode changed to Go Home.",
    "sentence": [
      "Failsafe RTH",
      "Press Brake button to cancel RTH",
      "RC signal lost",
      "Returning to home",
      "RC signal weak",
      "Avoid blocking antennas and adjust antenna orientation",
      "Downlink Restored (after 0m 5.8s)",
      "Flight mode changed to Go Home"
    ]
  },
]
```

---

### Citation
If you use LogNexus in your research, please cite:
```bib
@article{Silalahi2025LogNexus,
title = {LogNexus: A Foundational Segmentation Tool for Noisy Drone Logs},
publisher = {Code Ocean},
volume = {},
pages = {},
year = {2025},
note = {[Source Code]}
author = {Swardiantara Silalahi and Tohari Ahmad and Hudan Studiawan},
}
```