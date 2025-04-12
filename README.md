# Reddit Persona Generator

## Description
The Reddit Persona Generator is a Python script that utilizes the Reddit API to gather data and generate realistic personas for use in Reddit marketing and research.

## Requirements
*   Python 3.x
*   praw
*   uuid

## Installation
1.  Install the required packages:
    ```
    pip install praw
    ```
2.  Create a Reddit API application and obtain your client ID and client secret.
3.  Update the `data_gathering.py` and `persona_generation.py` files with your Reddit API credentials.

## Usage
1.  Run the `persona_generation.py` script:
    ```
    python persona_generation.py
    ```
2.  The script will generate a persona based on the specified username and output the persona to the console and to a file named `{username}_persona.txt`.

## Example
```
python persona_generation.py
```

## Documentation
*   `data_gathering.py`: This file contains the functions for gathering data from the Reddit API.
*   `persona_generation.py`: This file contains the functions for generating and formatting personas.

## Contributing
Contributions are welcome! Please submit a pull request with your changes.
