# Text to Speech Generator

This Python script provides a GUI for generating audio files from text input using the OpenAI text-to-speech API. The generated audio files are saved in a specified directory, and the input text is logged in a separate directory.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- OpenAI API
- Pygame
- pathlib
- datetime
- threading

## Installation

1. Clone the repository or download the script file.

2. Install the required Python packages:

    ```bash
    pip install openai pygame
    ```

3. Ensure you have the OpenAI API key set up. You can do this by setting an environment variable `OPENAI_API_KEY` with your API key.

## Usage

1. Run the script:

    ```bash
    python openAI_tts_gui.py
    ```

2. Enter the text you want to convert to speech in the text box.

3. Select the voice from the dropdown menu.

4. Adjust the speed using the slider.

5. Click the "Generate Audio" button. A message will indicate that the text is being processed.

6. Once the audio files are generated, the message will update to indicate success, and the paths of the generated audio files will be displayed.

7. You can play the last generated audio file by clicking the "Play Last Generated Audio" button.

## Directory Structure

- The generated audio files are saved in the `generated_sounds` directory.
- The input text logs are saved in the `text_logs` directory.

## Notes

- Ensure you have a stable internet connection, as the script communicates with the OpenAI API to generate the audio.
- The script supports multiple voice options provided by the OpenAI API.
- The audio files are generated in MP3 format.

## Troubleshooting

- If the script fails to generate audio, check the API key set for the environment variable `OPENAI_API_KEY` and ensure it is correctly set.
- Make sure the required Python packages are installed and up to date.



