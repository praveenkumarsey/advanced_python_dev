You are helping me create a **training demo repository** for a 40-hour Python program delivered in **4-hour daily sessions**.

Your task is to generate **day-wise demo code** aligned to the slide content already prepared for:
- Day 1: Python Foundations Bridge + Module 1 (OOP Refresher & Code Design)
- Day 2: Module 2 (Advanced Object Modeling)

Important:
- This is **not** for capstone tasks.
- The demos must be **teaching demos**, not assignments.
- The code must be **fully executable**.
- The examples must be **neutral and concept-first**, with only a small optional secondary example that connects to validation if genuinely helpful.
- Keep the code professional, readable, and instructional.
- Use **only standard library** unless a dependency is absolutely necessary.
- Use **`.venv` everywhere** for setup instructions, commands, and documentation.
- Create a proper `README.md` with exact execution steps.

## Goal

Create a small training repository with **day-wise demo folders**, where each demo:
- maps clearly to the slide topics,
- can be run independently,
- includes short code-level explanations,
- prints meaningful output,
- demonstrates the concept in a simple and engineering-friendly way.

The repository should help an instructor teach by running examples live.

## Audience

- Working professionals from data engineering backgrounds
- Comfortable with basic Python and simple PySpark-style coding
- Newer to structured OOP design and advanced Python modeling
- Need concept clarity more than academic theory

## Content alignment

Use the following content alignment.

### Day 1 — Python Foundations Bridge + Module 1
Cover demo code for:
- Python mental model
- Names and references
- Mutability vs immutability
- Core containers: list, dict, tuple, set
- Functions: parameters, returns, scope
- Exceptions: try/except/else/finally, raise
- Modules and imports
- Class vs instance
- Encapsulation
- Properties
- Inheritance
- Composition vs inheritance
- Method overriding
- Abstract Base Classes
- Interface design
- Designing for extension
- Common OOP anti-patterns

### Day 2 — Module 2
Cover demo code for:
- Python data model basics
- `__repr__`
- `__eq__`
- `dataclasses`
- dataclass field defaults and `default_factory`
- Properties for computed values and validation
- Context managers
- Function decorators
- `functools.wraps`
- Class decorators
- Plugin registration using `__init_subclass__`
- Combining multiple modeling techniques in one example
- Common mistakes and corrected versions where useful

## Output expected from you

Generate the full repository content, including all files.

### Required repository structure

Create a structure like this:

training-demos/
├── README.md
├── .gitignore
├── requirements.txt
├── day-01/
│   ├── README.md
│   ├── 01_references_and_mutability.py
│   ├── 02_functions_and_exceptions.py
│   ├── 03_modules_demo/
│   │   ├── main.py
│   │   └── helpers.py
│   ├── 04_class_vs_instance.py
│   ├── 05_encapsulation_and_properties.py
│   ├── 06_inheritance_vs_composition.py
│   ├── 07_method_overriding_and_abc.py
│   └── 08_oop_antipatterns.py
├── day-02/
│   ├── README.md
│   ├── 01_repr_and_eq.py
│   ├── 02_dataclasses_basics.py
│   ├── 03_dataclasses_field_defaults.py
│   ├── 04_properties_advanced.py
│   ├── 05_context_managers.py
│   ├── 06_function_decorators.py
│   ├── 07_class_decorators.py
│   ├── 08_init_subclass_registry.py
│   └── 09_combined_modeling_demo.py

You may adjust file names slightly if needed, but preserve the day-wise structure and logical flow.

## File-level expectations

For every `.py` file:
- Make it executable with:
  - `python <filename>.py`
- Include:
  - module docstring at the top,
  - clear example setup,
  - printed output that demonstrates the concept,
  - short inline comments only where they improve learning,
  - a `main()` function where appropriate,
  - `if __name__ == "__main__": main()`
- Keep each file focused on **one main concept** or one tightly related pair of concepts.
- Avoid overly long files.
- Prefer multiple small demos over one giant script.

## Teaching style for code

The code should feel like an instructor demo:
- clean and readable,
- progressive,
- simple enough to explain live,
- realistic enough to be respected by engineers,
- not toyish unless a toy example is the clearest way to explain the concept.

Use analogies only in comments or README when they genuinely help, for example:
- class vs instance,
- composition vs inheritance,
- mutable vs immutable state.

Do not overdo analogies.

## README requirements

Create:
- one top-level `README.md`
- one `README.md` inside `day-01/`
- one `README.md` inside `day-02/`

### Top-level README.md must include

1. Project purpose
2. Audience
3. Topics covered by day
4. Prerequisites
5. Exact environment setup using `.venv`
6. Exact run commands
7. Folder structure
8. Notes for trainers
9. Troubleshooting section
10. Clear statement that examples use standard library only unless noted

### Environment setup section must use `.venv`

Use commands like these in the README, with Windows and macOS/Linux variants where needed:

#### Create virtual environment
- `python -m venv .venv`

#### Activate on Windows
- `.venv\\Scripts\\activate`

#### Activate on macOS/Linux
- `source .venv/bin/activate`

#### Upgrade pip
- `python -m pip install --upgrade pip`

#### Install dependencies
- `pip install -r requirements.txt`

If no third-party dependencies are used, still include:
- `requirements.txt`
- a comment or note indicating standard-library-first demos

### Day README files must include
- learning goals,
- demo file order,
- how to run each demo,
- what to observe in output,
- suggested trainer flow,
- optional extension ideas.

## Specific content guidance

### Day 1 guidance

#### 01_references_and_mutability.py
Demonstrate:
- names pointing to objects,
- aliasing,
- mutating a list through one reference affects another,
- immutable reassignment creates a new object,
- small examples with `id()` only if helpful.

#### 02_functions_and_exceptions.py
Demonstrate:
- parameters,
- default parameters,
- return values,
- local scope,
- raising exceptions,
- handling exceptions with `try/except/else/finally`.

#### 03_modules_demo
Create:
- `helpers.py` with a few reusable functions/classes,
- `main.py` that imports them cleanly.
Demonstrate:
- `import module`,
- `from module import name`,
- `__name__ == "__main__"`.

#### 04_class_vs_instance.py
Demonstrate:
- class attributes vs instance attributes,
- constructor usage,
- independent instance state,
- a clean real-world example like `BankAccount`, `Book`, or `Sensor`.

#### 05_encapsulation_and_properties.py
Demonstrate:
- internal attribute naming conventions,
- controlled access,
- validation through a property setter,
- why direct mutation is risky.

#### 06_inheritance_vs_composition.py
Demonstrate both:
- an inheritance example,
- a composition example,
- a short comparison in comments or output explaining why composition is often more flexible.

#### 07_method_overriding_and_abc.py
Demonstrate:
- overriding behavior in a subclass,
- use of `super()`,
- `ABC` and `@abstractmethod`,
- a simple contract like `Shape`, `Notifier`, or `Exporter`.

#### 08_oop_antipatterns.py
Demonstrate small, safe examples of:
- God object,
- tight coupling,
- misuse of inheritance.
Then provide improved versions in the same file or as paired examples.

### Day 2 guidance

#### 01_repr_and_eq.py
Demonstrate:
- poor default representation,
- improved `__repr__`,
- default identity-based equality,
- custom equality based on state.

#### 02_dataclasses_basics.py
Demonstrate:
- regular class vs dataclass,
- reduced boilerplate,
- generated `__init__`, `__repr__`, `__eq__`.

#### 03_dataclasses_field_defaults.py
Demonstrate:
- default values,
- why mutable defaults are dangerous,
- `field(default_factory=list)` or `dict`,
- optionally `frozen=True`.

#### 04_properties_advanced.py
Demonstrate:
- computed property,
- validation setter,
- separating stored value from presented value.

#### 05_context_managers.py
Demonstrate both:
- class-based context manager with `__enter__` and `__exit__`,
- function-based context manager with `contextlib.contextmanager`,
- resource cleanup behavior.

#### 06_function_decorators.py
Demonstrate:
- wrapping a function,
- timing or logging,
- `functools.wraps`,
- stacking decorators if it remains clear.

#### 07_class_decorators.py
Demonstrate:
- simple class decorator that adds behavior or metadata,
- explain when this is useful and when it is unnecessary.

#### 08_init_subclass_registry.py
Demonstrate:
- plugin registration using `__init_subclass__`,
- base class registry,
- automatic subclass discovery,
- lookup by name or type key.

#### 09_combined_modeling_demo.py
Create a cohesive but still compact demo combining:
- dataclass,
- property,
- context manager,
- decorator,
- plugin registration.
Keep it focused and runnable.
Do not turn this into a capstone.

## Documentation quality bar

Every file and README should be self-explanatory:
- Use short docstrings
- Add a “How to run” section where useful
- Add “Expected learning” or “What this demo shows”
- Keep explanations concise and professional
- Avoid long theory paragraphs

## Execution requirements

Make sure everything runs from the terminal after setting up `.venv`.

### Commands that must work

From repository root:
- `python day-01/01_references_and_mutability.py`
- `python day-01/02_functions_and_exceptions.py`
- `python day-01/03_modules_demo/main.py`
- `python day-02/01_repr_and_eq.py`
- `python day-02/09_combined_modeling_demo.py`

Ensure imports work correctly when run as documented.

## Constraints

- No notebooks
- No capstone code
- No web frameworks
- No database setup
- No external services
- No hidden dependencies
- No unnecessary packaging complexity
- Keep the repository trainer-friendly
- Prefer standard library examples
- Keep examples concept-aligned with the slides

## Nice-to-have additions

If appropriate, also include:
- a simple `Makefile` or cross-platform command notes,
- a `run_all.py` per day,
- a short trainer checklist in the top-level README,
- optional “try this next” exercises at the end of each day README.

## Final instruction

Generate:
1. all file contents,
2. all code,
3. all README files,
4. `.gitignore`,
5. `requirements.txt`,
6. any small helper files needed.

Return the content in a way that is easy to copy into a repository.
Do not skip code.
Do not give only summaries.
Produce concrete, executable files.
