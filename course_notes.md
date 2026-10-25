# Professional Python for Data Engineering (pp4de) — Complete Course Notes

---

## 1. Project Architecture & Standards
* **The `src/` Layout Pattern:** Code lives inside `src/<package_name>/` rather than directly in the root directory. This prevents accidental imports of local working-directory scripts and guarantees that tests run against the installed package.
* **Modern Package Metadata (`pyproject.toml`):** Replaces legacy `setup.py` and `requirements.txt`. It standardizes build backend specifications (`setuptools`, `hatchling`), core dependencies, optional dependency groups (`[project.optional-dependencies] dev = [...]`), script CLI entrypoints (`[project.scripts]`), and tool configurations (`ruff`, `mypy`, `pytest`).
* **Packaging and Editable Mode:** Using `pip install -e ".[dev]"` installs the local package in editable mode alongside developer tooling. In `zsh`, square brackets must be quoted (`".[dev]"`) to prevent the shell from interpreting them as glob patterns.
* **Environment Isolation:** Every standalone service or pipeline module maintains its own virtual environment (`python3 -m venv .venv`), keeping package dependencies strictly decoupled.

---

## 2. CLI Design & Operational Interfaces
* **Interface Decoupling:** Pipeline orchestration belongs in CLI commands (`click` / `argparse`), separating argument parsing from pure business logic functions.
* **Exit Codes as Operational Signals:** Standard command-line tools emit status codes. Code `0` indicates success; any non-zero exit code indicates an error or failure, allowing upstream schedulers (Airflow, Cron, GitHub Actions) to act predictably.
* **Idempotent CLI Invocations:** Pipeline commands should accept execution dates or run IDs as parameters rather than assuming "today," ensuring backfills run safely without altering core ingestion logic.

---

## 3. Data Boundary Validation & Typing
* **Pydantic Validation at Ingestion:** All raw external data (JSON, CSV, REST API payloads) must pass through strongly-typed Pydantic schemas before reaching downstream transformations or data warehouse tables.
* **Schema Evolution & Coercion:** Explicit models catch missing keys, schema drift, invalid nulls, and wrong types at the extraction boundary, avoiding silent data corruption deep inside pipelines.
* **Strict Static Typing (`mypy --strict`):** Enforce strict type annotations across functions. Type checking prevents common runtime errors (e.g., `NoneType` attribute access, implicit numeric conversions, mismatched dictionary structures) before code executes.

---

## 4. Resilience, Retries & External APIs
* **Transient vs. Permanent Errors:**
  * *Transient (Retryable):* Network drops, HTTP 429 (Rate Limit), HTTP 503 (Service Unavailable), read timeouts.
  * *Permanent (Non-retryable):* HTTP 400 (Bad Request), HTTP 401/403 (Unauthorized/Forbidden), boundary validation failures.
* **Exponential Backoff with Jitter:** When retrying external calls, calculate delays using $t = \min(\text{max\_delay}, \text{base\_delay} \times 2^{\text{attempt}}) \pm \text{jitter}$ to prevent the "thundering herd" problem from overwhelming upstream APIs.
* **Exception Handling Cleanliness:** In Python exception handlers, use a bare `raise` to re-raise active exceptions rather than `raise exc`, preserving the original traceback.

---

## 5. Database Writing & Idempotency
* **Idempotent Pipelines:** A pipeline must produce the exact same final state whether executed once or multiple times for the same logical batch.
* **Upsert Strategies (`ON CONFLICT`):** In SQL databases (PostgreSQL), use `INSERT INTO ... ON CONFLICT (id) DO UPDATE SET ...` to guarantee that rerunning pipeline batches updates records in place rather than creating duplicate rows.
* **Atomic Transactions:** Wrap batch inserts and state updates inside single database transactions (`with connection.transaction():`). If an error occurs midway through a 10,000-row batch, the transaction rolls back cleanly, leaving no orphaned or partial records.

---

## 6. Testing Strategies for Data Engineering
* **Unit Testing:** Validates isolated transformation functions (such as revenue/discount formulas, currency conversions, schema parsers) without requiring database or network connections.
* **Property-Based Testing (`hypothesis`):** Tests business logic across hundreds of randomized edge cases (e.g., negative amounts, zero quantities, massive floats, unicode strings) to discover bugs missed by manual test cases.
* **Integration Testing:** Tests real database interactions against isolated instances (e.g., test databases or SQLite fixtures) to ensure transactions, constraints, and rollbacks function properly.
* **Test Discovery Configuration:** Setting `pythonpath = ["src"]` in `[tool.pytest.ini_options]` allows `pytest` to resolve internal packages during test discovery. Setting `norecursedirs` prevents test collectors from traversing nested subprojects or virtual environments.

---

## 7. Concurrency & Asynchronous Pipelines
* **Async I/O (`asyncio`):** Efficient for high-latency, network-bound workloads (such as hitting hundreds of REST endpoints or fetching multiple object keys from S3).
* **Concurrency Throttling (`asyncio.Semaphore`):** Unbounded concurrency (`asyncio.gather(*tasks)`) can exhaust socket file descriptors or trigger HTTP 429 rate limits. Wrapping calls in `async with asyncio.Semaphore(N):` constrains concurrent executions to a safe limit.
* **Memory Management via Generators (`yield`):** Avoid loading massive API responses or multi-gigabyte query outputs into a single in-memory list. Process data using streaming chunks or generator functions to maintain constant $O(1)$ memory overhead and avoid out-of-memory (OOM) process termination.

---

## 8. Configuration, Secrets & Environment Safety
* **Centralized Settings (`pydantic-settings`):** Configuration belongs in a dedicated schema class inheriting from `BaseSettings`. Avoid scattering raw `os.environ.get()` calls across disparate files.
* **Environment Prefix Mapping:** Using `SettingsConfigDict(env_prefix="REPORT_DB_", extra="ignore")` automatically binds variables like `REPORT_DB_PASSWORD` to the model's `password` attribute.
* **Failing Fast on Secrets:**
  * Provide defaults *only* for safe, local-friendly properties (e.g., `host: str = "localhost"`).
  * Never set default fallback values for credentials or database passwords (`password: str`).
  * If a mandatory secret is missing from the environment, `BaseSettings` immediately raises a `ValidationError` at startup, preventing the application from silently routing traffic to fallback or mock environments.

---

## 9. Automated CI/CD Quality Gates
* **The Role of CI in Data Engineering:** Undetected bugs in data pipelines do not merely break user interfaces—they can silently write corrupted records into analytical data warehouses. Automated gates catch schema, type, and transformation errors before merge.
* **The "Green Pipeline" Illusion:** Suppressing non-zero exit codes using commands like `|| true` or `|| echo "skipped"` masks real pipeline failures, creating false-positive green checks while shipping broken code.
* **The Standard Data Engineering CI Pipeline (GitHub Actions):**
  1. **Checkout Code:** `actions/checkout@v4`
  2. **Set up Environment:** `actions/setup-python@v5` with explicit Python versions.
  3. **Install Dependencies:** `pip install -e ".[dev]"`
  4. **Lint & Style Check:** `ruff check .`
  5. **Strict Static Type Gate:** `mypy --strict src/ tests/`
  6. **Unit & Integration Suite:** `pytest`