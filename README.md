# ProAcces-TTS

ProAcces-TTS is a text-to-speech synthesis project designed to support multiple languages with advanced phonetic and prosodic features.

## Overview
This project is structured to support modular development, separating concerns between synthesis core, prosody management, phonemization, and data handling.

## Structure
- **/core/**: Core synthesis logic.
- **/prosody_engine/**: Prosody handling.
- **/phonemizer/**: Text to phoneme conversion.
- **/data_management/**: Data loading and preprocessing.
- **/utils/**: Utility scripts for various functions.
- **/languages/**: Language-specific configurations.

## Installation
To install the necessary dependencies, use:
```bash
pip install -r requirements.txt
```

## Usage
Run the synthesis engine by executing:
```bash
python -m core.synthesis
```
