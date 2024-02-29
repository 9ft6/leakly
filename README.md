# Leafly Parser

**Description:**

This is a high-speed, asynchronous parser for the cannabis enthusiast community platform, Leafly.com. The parser is built using `aiohttp` for asynchronous web requests and leverages `pydantic` for model serialization. Its primary purpose is to gather information on cannabis strains and their associated comments. The parser allows for strain updates using the `-u` or `--update` flag. A complete dataset of strains(7k+) and comments(350k+) can be collected in approximately 2 minutes.

**Features:**
- **Asynchronous Parsing:** Utilizes `aiohttp` for efficient and fast asynchronous web scraping.
- **Model Serialization:** Employs `pydantic` for streamlined and effective serialization of data models.
- **Data Analysis Focus:** Designed for collecting comments for subsequent analysis.

**Planned Features:**
- **Database Migration:** Transition from a basic pickle storage to a more robust database system, possibly MongoDB.
- **GUI Interface:** Implementation of a graphical user interface for easy browsing and interaction with the database.
- **Graphical Analysis:** Integration of Jupyter Notebooks for graph creation and analysis.
- **Intelligent Parsing Termination:** The parser now includes a feature to automatically stop if it detects that all strains on the current page have already been collected in the database, ensuring efficiency and preventing unnecessary data retrieval.

**Usage:**
- To update strains: `-u` or `--update` flags.
- Complete dataset collection: Approximately 10 minutes.

**Future Development:**
- **Database Transition:** Move from basic pickling to a MongoDB or similar database for enhanced data management.
- **GUI Interface:** Create a user-friendly graphical interface for seamless database interaction.
- **Graphical Analysis:** Integrate Jupyter Notebooks to enable users to generate and analyze graphs based on the collected data.

**Project Structure:**
- `main.py`: The main script for executing the parser.
- `models.py`: Contains `pydantic` models for efficient data serialization.
- `client.py`: Implements the asynchronous parser using `aiohttp`.
- `database.py`: Placeholder for future database integration.

**Installation:**
```bash
pip install -r requirements.txt
```

**Dependencies:**

- Python 3.10
- aiohttp
- pydantic

**Contributing:**
Contributions and suggestions are welcome. Feel free to open an issue or submit a pull request.

**License:**
This project is licensed under the MIT License.

**Acknowledgments:**
Thanks to the Leafly community for providing valuable insights and comments.

**Disclaimer:**
This project is for educational and research purposes only. Ensure compliance with applicable laws and regulations in your jurisdiction.

