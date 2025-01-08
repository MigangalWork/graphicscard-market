# Mercado Tarjetas

A simulation of a GPU market with economic agents.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Testing](#testing)

## Introduction

This project simulates a GPU market, modeling interactions between economic agents. It uses Python and SQLAlchemy to manage data and processes.

## Requirements

- Python >= 3.8
- `pip` (Python package installer)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MigangalWork/graphicscard-market.git
   cd graphicscard-market
    ```

2. **Create a Virtual Environment:**

    Create a virtual environment to isolate project dependencies:
    ```bash
    python -m venv venv
    ```

    Activate the Virtual Environment:

    On Linux/Mac:


            source venv/bin/activate
            
    On Windows:

        venv\Scripts\activate

3. **Install Dependencies: Use pip to install the project and its dependencies:**
    ```bash
    python -m pip install .
    ```

If you also want to install development dependencies, use:
```bash
python -m pip install .[dev]
```

## Running the Project

After installation, you can run the simulation using:

```bash
python -m mercado_tarjetas
```

## Testing

To run the test suite, ensure pytest is installed and execute:

```bash
pytest
```
