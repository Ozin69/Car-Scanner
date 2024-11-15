# Car Scanner

A simple GUI application to extract license plate information from images and fetch car details using APIs.

---

## Features

- Upload images to detect license plates.
- Draw bounding boxes around detected plates in the image.
- Fetch car details from the DVLA database.
- Option to enable test mode to bypass API calls.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.7+**: Download from [python.org](https://www.python.org/).
- **Pillow**: Python Imaging Library for image processing.
- **Requests**: For making HTTP requests.
- **Tkinter**: Comes pre-installed with Python.

### Steps

1a. Clone the repository:
   ```bash
   git clone https://github.com/Ozin69/Car-Scanner
   ```
1b. Or, download the python file from the github:
   - Go to the repository, either download as zip or manual download of main.py.
     
2. Navigate to the project directory:
   ```bash
   cd Car-Scanner
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up API keys:
   - Replace the placeholder `PLATE_RECOGNIZER_API_KEY` with your Plate Recognizer API key.
   - Replace the placeholder `x-api-key` in `fetch_car_details` function with your DVLA API key.

---

## Usage

### Basic Usage

1. Start the application:
   ```bash
   python app.py  OR  double click python file  OR  import into IDE and run inside.
   ```
2. Use the **Upload Image** button to select an image containing a license plate.
3. If a license plate is detected:
   - The extracted plate number will appear.
   - The bounding box will be drawn on the image.
   - Vehicle details will be displayed (if available).
4. Enable "Test Mode" to skip API calls and display a placeholder result.

### Examples

After uploading photo of car, the licence plate will have a box highlighting it, returning information such as:
```plaintext
License Plate: ABC123
Make: Ford
Model: Fiesta
Year: 2020
Color: Blue
```

---

## Dependencies

List the key dependencies required to run the project:

- **Pillow**: Image processing library.
- **Requests**: HTTP library for API requests.
- **Tkinter**: GUI framework for Python (comes pre-installed).

You can install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this software.

---

