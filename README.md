# NameCheck-Pro
### Company Name Availability Checker & Generator

This application checks the availability of a proposed company name against a list of existing company names. If the proposed name is already taken or too similar to an existing name, the app will suggest alternative names based on additional inputs provided by the user.

## Features

- **Name Availability Check**: Check if the proposed company name is available or similar to existing names.
- **Similar Name Detection**: Identify and display similar names that are already taken.
- **Name Suggestions**: Generate new name suggestions based on the industry and unique features provided by the user.
- **Updated Name Suggestions**: Generate slightly updated versions of the similar names to make them distinct.

## Project Structure

- `app.py`: The main Streamlit app file.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Ahmedsamy96/NameCheck-Pro.git
    cd NameCheck-Pro
    ```

2. **Install the Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

2. **Enter the Proposed Company Name**:
    - The app will check if the name is available or if it matches any existing names.

3. **If the Name is Taken**:
    - The app will display a list of similar names already taken.
    - Provide additional details (Industry and Unique Feature) to generate new suggestions.

4. **If the Name is Available**:
    - The app will inform you that the name is available for use.

## Dependencies

- `streamlit`: Used to create the web application interface.
- `google.generativeai`: Used to interact with the Gemini API for generating company name suggestions.
- `difflib`: Used to compute similarity ratios between names.
- `ast`: Used to safely evaluate string representations of Python expressions.

## Gemini API Setup

To use the Gemini API for generating name suggestions, you must set up the API as follows:

1. **Install the Gemini API Client**:
    ```bash
    pip install google-generativeai
    ```

2. **Set Up Authentication**:
    - Ensure you have an API key from Google Generative AI (Gemini).
    - Follow the [Google Generative AI documentation](https://developers.google.com/genai) for setup instructions.

## Future Enhancements

- Improve the name suggestion logic by incorporating more business-specific criteria.
- Add additional filtering options to refine name suggestions further.
- Integrate more robust error handling and user input validation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to discuss any changes or enhancements.

## License

This project is licensed under the Apache License. See the `LICENSE` file for more details.


