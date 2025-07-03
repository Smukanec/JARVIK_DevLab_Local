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
git clone https://github.com/your-org/jarvik-devlab.git
cd jarvik-devlab
```
2. (optional) Create a virtual environment and activate it
3. Install Python dependencies
```bash
pip install -r requirements.txt
```
4. Run `./install.sh` to install the package locally
5. Run `./upgrade.sh` anytime to update to the newest release

### Basic usage
```python
from devlab.manager import DevLabManager

manager = DevLabManager()
code = manager.run("Create a simple Hello World application")
print(code)
```

### Exporting data
You can save DevLab context for later review:

* **Export memory** – compresses the `dev_memory/` directory into a `memory_export.zip` archive by calling `DevEngine.export_memory()`.
* **Export knowledge** – collects all entries from `knowledge_db/` into `knowledge_export.json` using `DevEngine.export_knowledge()`.

Open `DevLab/ui/devlab_ui.html` and use the provided links, or call the methods directly in your Python code.

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
git clone https://github.com/your-org/jarvik-devlab.git
cd jarvik-devlab
```
2. (volitelně) Vytvořte a aktivujte virtuální prostředí
3. Nainstalujte Python závislosti
```bash
pip install -r requirements.txt
```
4. Spusťte `./install.sh` pro lokální instalaci balíčku
5. Pro aktualizaci na nejnovější verzi použijte `./upgrade.sh`

### Základní použití
```python
from devlab.manager import DevLabManager

manager = DevLabManager()
code = manager.run("Vytvoř jednoduchou aplikaci Hello World")
print(code)
```

### Jak přispět
Budeme rádi za pull requesty. Forkněte repozitář, vytvořte větev a odešlete návrh ke schválení.

### Hlášení chyb
Pro nahlášení chyby nebo návrh nového vylepšení založte issue na GitHubu.

### Licence
Tento projekt je publikován pod licencí [MIT License](LICENSE).

