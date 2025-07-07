# 🧠 DevLab – Vývojová vrstva nad Jarvikem / DevLab – Development layer for Jarvik

## English

**DevLab** is a standalone development sub‑application within the **Jarvik** ecosystem. It focuses on intelligent code generation, validation and management with help of cooperating AI models. While the project is in an early stage, it aims to simplify Python development, API design and working with GitHub repositories.

### Features
- AI assisted generation of code snippets
- Simple validation stubs ready for future extension
- `DevLabManager` orchestrating generation and validation steps
- Designed to integrate with the Jarvik platform

### Installation
1. Clone this repository
```bash
git clone https://github.com/your-org/devlab.git
cd devlab
```
2. Create and activate a Python virtual environment. This is required on systems
   that implement [PEP 668](https://peps.python.org/pep-0668/) with an
   externally managed Python installation. Keep the environment active when
   running `install.sh` or `upgrade.sh`.
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Alternatively, run `./create_venv.sh` to perform these steps automatically.
**Note:** Systems lacking the `python3-venv` or `pip` packages may produce errors like "No module named pip". Install the relevant OS packages (e.g. `python3-venv` and `python3-pip` on Debian/Ubuntu) or run `python3 -m ensurepip`.
3. Install Python dependencies
```bash
pip install -r requirements.txt
```
4. With the virtual environment still active, run `./install.sh` to install the
   package locally

5. With the virtual environment active, run `./upgrade.sh` to update to the newest release

You can optionally start DevLab using the helper script `./devlab_venv.sh`. The
script creates (or reuses) a local `.venv`, installs the dependencies and runs
`install.sh` by default before launching `devlab-cli`. Pass `upgrade` as the
first argument to have the helper run `upgrade.sh` instead of `install.sh`.

Running `devlab-cli` or `devlab-server` directly on systems with an externally
managed Python installation will fail with an error. Use the `devlab_venv.sh`
helper or create and activate a virtual environment before launching the tools.

### Basic usage
```python
from devlab.manager import DevLabManager

manager = DevLabManager()
code = manager.run("Create a simple Hello World application")
print(code)
```

### Command line interface
You can also interact with DevLab directly from a terminal. After installing the
package, run:

```bash
devlab-cli "Create a simple Hello World application"
```

Omitting the prompt starts an interactive mode where you can enter multiple
prompts one by one.

### Exporting data
You can save DevLab context for later review:

* **Export memory** – compresses the `dev_memory/` directory into a `memory_export.zip` archive by calling `DevEngine.export_memory()`.
* **Export knowledge** – collects all entries from `knowledge_db/` into `knowledge_export.json` using `DevEngine.export_knowledge()`.

Open `devlab/ui/devlab_ui.html` and use the provided links, or call the methods directly in your Python code.

### Web server and UI
Start the bundled FastAPI server with:

```bash
devlab-server
```
This command launches `uvicorn` with the ``devlab.app:app`` application.

The server listens on `http://127.0.0.1:8000`. Open
`http://127.0.0.1:8000/devlab_ui.html` in your browser to use the UI.

### Running tests
Create and activate a Python virtual environment before running the test suite.
You can use the helper script `./devlab_venv.sh` to set up the environment.
Then install `pytest` and execute the tests:

```bash
pip install pytest
pytest -q
```

### Contributing
Contributions are welcome! Fork the repository, create a feature branch and open a pull request.

### Reporting issues
If you encounter problems or have suggestions, please open an issue on GitHub.

### License
This project is released under the [MIT License](LICENSE).

---

## Čeština

**DevLab** je samostatná vývojová podaplikace v rámci systému **Jarvik**. Jejím cílem je generovat, validovat a spravovat kód pomocí spolupracujících AI modelů. Projekt je v rané fázi, ale má ulehčit vývoj v Pythonu, návrhy API i práci s GitHub repozitáři.

### Funkce
- Generování úryvků kódu za pomoci AI
- Základní validace připravené k dalšímu rozšiřování
- `DevLabManager` koordinuje kroky generování a validace
- Navrženo pro integraci do platformy Jarvik

### Instalace
1. Naklonujte tento repozitář
```bash
git clone https://github.com/your-org/devlab.git
cd devlab
```
2. Vytvořte a aktivujte virtuální prostředí. Na systémech s
   [PEP 668](https://peps.python.org/pep-0668/) je to nutné. Prostředí
   ponechte aktivní při spouštění `install.sh` nebo `upgrade.sh`.
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Případně můžete spustit `./create_venv.sh`, který kroky provede automaticky.
**Poznámka:** Na systémech bez balíčků `python3-venv` nebo `pip` se může objevit chyba "No module named pip". Nainstalujte potřebné balíčky systému (např. `python3-venv` a `python3-pip` na Debianu/Ubuntu) nebo spusťte `python3 -m ensurepip`.
3. Nainstalujte Python závislosti
```bash
pip install -r requirements.txt
```
4. Se stále aktivním virtuálním prostředím spusťte `./install.sh` pro lokální
   instalaci balíčku
5. Pro aktualizaci na nejnovější verzi aktivujte virtuální prostředí a
   spusťte `./upgrade.sh`

Pro rychlý start můžete použít pomocný skript `./devlab_venv.sh`. Ten
vytvoří (nebo znovu použije) lokální adresář `.venv`, nainstaluje závislosti a
standardně spustí `install.sh` před spuštěním `devlab-cli`. Pokud jako první
argument předáte `upgrade`, skript místo toho spustí `upgrade.sh`.

Přímé spuštění `devlab-cli` nebo `devlab-server` na systémech s externě
spravovanou instalací Pythonu skončí chybou. Pro úspěšný start použijte
skript `devlab_venv.sh` nebo si ručně vytvořte a aktivujte virtuální
prostředí.

### Základní použití
```python
from devlab.manager import DevLabManager

manager = DevLabManager()
code = manager.run("Vytvoř jednoduchou aplikaci Hello World")
print(code)
```

### Příkazová řádka
DevLab můžete ovládat i z terminálu. Po instalaci spusťte:

```bash
devlab-cli "Vytvoř jednoduchou aplikaci Hello World"
```

Bez zadaného promptu se spustí interaktivní režim pro více dotazů.

### Webový server
Server spustíte příkazem:

```bash
devlab-server
```
Příkaz spustí `uvicorn` s aplikací ``devlab.app:app``.

Poté otevřete `http://127.0.0.1:8000/devlab_ui.html` ve webovém prohlížeči.

### Spouštění testů
Před spuštěním testů vytvořte a aktivujte virtuální prostředí. Můžete využít
pomocný skript `./devlab_venv.sh`. Pak nainstalujte `pytest` a spusťte testy:

```bash
pip install pytest
pytest -q
```

### Jak přispět
Budeme rádi za pull requesty. Forkněte repozitář, vytvořte větev a odešlete návrh ke schválení.

### Hlášení chyb
Pro nahlášení chyby nebo návrh nového vylepšení založte issue na GitHubu.

### Licence
Tento projekt je publikován pod licencí [MIT License](LICENSE).

