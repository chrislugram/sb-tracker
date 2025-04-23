# sb-tracker

**sb-tracker** is a lightweight personal project designed to help individuals track time, costs, and profits for small-scale or personal ventures. Built with [Streamlit](https://streamlit.io/), it offers a simple and interactive interface for managing basic business metrics without the complexity of larger tools.

## Technologies Used

- **Streamlit**: Primary framework for building the interactive web application
- **Python**: Core programming language for application logic
- **Pandas**: Data manipulation and analysis
- **Poetry**: Dependency management and packaging
- **Flake8**: Code linting to maintain code quality
- **Pre-commit**: Automated checks before commits

## Getting Started

To run the application locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/chrislugram/sb-tracker.git
   cd sb-tracker
   ```

2. **Configuration**:

   Review `config.ini` before run the project, need some paths for store the .parquet files

3. **Install dependencies using Poetry**:

   Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed. Then run:

   ```bash
   poetry install
   ```

4. **Run the application**:

   ```bash
   make start
   ```

   The application will open in your default web browser.

## Project Structure

- `main.py`: Entry point of the Streamlit application
- `components`: UI components for managging the differents tab of the app
- `config`: Configuration files and settings
- `definition`: Data models and definitions
- `storage`: Module for read and save information
- `logger.py`: Logging configuration for the application
- `pyproject.toml`: Project metadata and dependencies managed by Poetry
- `.pre-commit-config.yaml`: Configuration for pre-commit hooks

## 📄 Licene

This project is licensed under the [Apache 2.0 License](https://github.com/chrislugram/sb-tracker/blob/main/LICENE).
