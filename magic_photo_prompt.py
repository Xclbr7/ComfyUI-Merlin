import json
import os

class MagicPhotoPrompter:
    @classmethod
    def INPUT_TYPES(s):
        # Load options from JSON file
        options = s.load_options()
        return {
            "optional": {
		"prompt": ("STRING", {"multiline": True}),
                "camera": (list(options["camera"].keys()),),
                "composition_shot": (list(options["composition_shot"].keys()),),
                "time_of_day": (list(options["time_of_day"].keys()),),
                "color_grading": (list(options["color_grading"].keys()),),
                "lighting": (list(options["lighting"].keys()),),
                "environment": (list(options["environment"].keys()),),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Prompter"

    @staticmethod
    def load_options():
        # Load the JSON file containing the options and prompts
        json_path = os.path.join(os.path.dirname(__file__), "magic_options.json")
        with open(json_path, 'r') as file:
            return json.load(file)

    def generate_prompt(self, prompt, camera, composition_shot, time_of_day, color_grading, lighting, environment):
        options = self.load_options()
        
        # Concatenate the prompts for each selected option
        prompt_parts = [
        part for part in [
            prompt,
            options["composition_shot"].get(composition_shot, ""),
            options["environment"].get(environment, ""),
            options["time_of_day"].get(time_of_day, ""),
            options["lighting"].get(lighting, ""),
            options["camera"].get(camera, ""),
            options["color_grading"].get(color_grading, "")
        ] if part.strip() != ""
    ]
        # Join the prompt parts with commas
        final_prompt = ". ".join(prompt_parts)
        
        return ("Photograph of " + final_prompt,)

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "Magic Photo Prompter 🪄": MagicPhotoPrompter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Magic Photo Prompter 🪄": "Magic Photo Prompter"
}