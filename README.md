# Conjunctive Normal Form Converter

This project is a web application that converts logical phrases into their Conjunctive Normal Form (FNC). It's built with Django and Python.

## Features

- Converts logical phrases into CNF.
- Eliminates equivalence and implication from logical phrases.
- Extracts clauses from logical phrases.
- Simplifies logical phrases.
- Generates a graph of the logical expression.

## Installation

1. Clone the repository: git clone https://github.com/kacem999/tpLia.git
2. Install the requirements: pip install -r requirements.txt
3. Run the Django server: python manage.py runserver
4. Open your web browser and navigate to `http://localhost:8000`.

## Usage

1. Enter a logical expression in the input field.
2. Click the "Convert" button to convert the expression into CNF.
3. Click the Show Graph button to display the graph of the logical expression.

- The logical expression must be in propositional logic.
- The logical operators supported are: 
    - `!` for negation.
    - `&` for conjunction.
    - `|` for disjunction.
    - `>` for implication.
    - `=` for equivalence.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Note
You must have the following installed on your machine:
- Python 3.8 or higher : https://www.python.org/downloads/
- Graphviz link : https://graphviz.org/download/

##Authors
- Kacem Cherifi

## License

[MIT](https://choosealicense.com/licenses/mit/)