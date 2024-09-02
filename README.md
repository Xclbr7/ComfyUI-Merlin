# ComfyUI-Merlin: Magical Prompt Engineering Tools 🪄

## Description

ComfyUI-Merlin is a custom node extension for ComfyUI, introducing two powerful tools for enhancing your prompt engineering process: the Magic Photo Prompter and the Gemini Prompt Expander. These tools allow users to easily construct detailed, high-quality prompts for photo-realistic image generation and expand existing prompts using AI.

## Features 🔮

### Magic Photo Prompter

- **User-friendly Interface**: Seamlessly integrates with ComfyUI's node-based system.
- **Customizable Options**: Choose from a variety of photographic elements including:
  - Camera settings
  - Composition shots
  - Time of day
  - Color grading
  - Lighting
  - Environment
- **Dynamic Prompt Generation**: Automatically combines user input with selected options to create comprehensive prompts.
- **Extensible**: Easily add or modify options through the `magic_options.json` file.

### Gemini Prompt Expander

- **AI-Powered Expansion**: Utilizes Google's Gemini AI to expand and enhance input prompts.
- **Structured Output**: Generates expanded prompts with specific sections for Type, Subject, Outfit, Pose & Scene, Extra Details, Background, and Technical Details.
- **API Key Management**: Supports both manual API key input and system environment variable storage.
- **Workflow Integration**: Automatically updates the node's widgets in the ComfyUI workflow.

## Installation

1. Clone this repository into your ComfyUI `custom_nodes` folder:
   git clone https://github.com/your-repo/ComfyUI-Merlin.git
2. Restart ComfyUI.

## Usage

### Magic Photo Prompter

1. Add the "Magic Photo Prompter 🪄" node to your workflow.
2. Connect the node inputs as needed.
3. Select options for camera, composition, time of day, color grading, lighting, and environment.
4. The node will generate a comprehensive prompt based on your selections.

### Gemini Prompt Expander

1. Add the "Gemini Prompt Expander 🪄" node to your workflow.
2. Input your initial prompt in the "input_text" field.
3. Provide your Gemini API key (or set it as an environment variable).
4. The node will generate an expanded, detailed prompt using AI.

## Configuration

### Gemini API Key

To use the Gemini Prompt Expander, you need to set up your Gemini API key. You can do this in three ways:

1. Input the API key directly in the node.
2. Set it as an environment variable named `GEMINI_API_KEY`.
3. For Windows users, it will be stored in the System Environment Variables after the first use.

### Customizing Magic Photo Prompter Options

You can modify the options available in the Magic Photo Prompter by editing the `magic_options.json` file located in the same directory as the node scripts.
