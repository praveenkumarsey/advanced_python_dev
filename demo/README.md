# Python Advanced Training — Demo Repository

Teaching demos for a 40-hour Python training program delivered in 4-hour daily sessions.
This repository is for **instructor-led demos**, not assignments.

---

## Audience

Working professionals from data engineering backgrounds who are:
- comfortable with basic Python and simple PySpark-style coding
- newer to structured OOP design and advanced Python modeling
- looking for concept clarity over academic theory

---

## Topics by Day

| Day | Module | Topics |
|-----|--------|--------|
| Day 1 | Foundations + OOP | References, mutability, functions, exceptions, modules, class vs instance, encapsulation, properties, inheritance, composition, ABCs, OOP anti-patterns |
| Day 2 | Advanced Object Modeling | `__repr__`, `__eq__`, dataclasses, properties, context managers, decorators, plugin registration |

---

## Prerequisites

- Python 3.10 or higher
- No third-party libraries required — all demos use the **standard library only**

---

## Environment Setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt` contains no third-party packages. All demos use the standard library.

---

## Running Demos

From the repository root, with `.venv` activated:

```bash
# Day 1
python day-01/01_references_and_mutability.py
python day-01/02_functions_and_exceptions.py
python day-01/03_modules_demo/main.py
python day-01/04_class_vs_instance.py
python day-01/05_encapsulation_and_properties.py
python day-01/06_inheritance_vs_composition.py
python day-01/07_method_overriding_and_abc.py
python day-01/08_oop_antipatterns.py
```

---

## Folder Structure

```
demo/
├── README.md
├── .gitignore
├── requirements.txt
├── day-01/
│   ├── README.md
│   ├── 01_references_and_mutability.py
│   ├── 02_functions_and_exceptions.py
│   ├── 03_modules_demo/
│   │   ├── helpers.py
│   │   └── main.py
│   ├── 04_class_vs_instance.py
│   ├── 05_encapsulation_and_properties.py
│   ├── 06_inheritance_vs_composition.py
│   ├── 07_method_overriding_and_abc.py
│   └── 08_oop_antipatterns.py
└── day-02/
    └── (Day 2 demos — coming soon)
```

---

## Trainer Notes

- Run demos sequentially within each day — concepts build progressively.
- Each file is self-contained and prints its own output.
- You can live-edit and re-run any file to show variations.
- For `03_modules_demo`, always run from the repository root using `python day-01/03_modules_demo/main.py`.
- The anti-patterns file (`08_oop_antipatterns.py`) shows bad code and its fix side-by-side — emphasise the contrast.

---

## Troubleshooting

**`ModuleNotFoundError` on 03_modules_demo:**
Run from the repository root, not from inside the `day-01/03_modules_demo/` directory.

**Wrong Python version:**
Check with `python --version`. Demos require Python 3.10+.

**`.venv` not activating:**
Make sure you created it with `python -m venv .venv` and are in the repository root.
