import os
import subprocess
import google.generativeai as genai

class GeminiPromptExpander:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "expand_prompt"
    CATEGORY = "Text"
    OUTPUT_NODE = True

    @staticmethod
    def get_api_key():
        if os.name == 'nt':  # Windows
            try:
                # Use reg query to get the API key from the Windows registry
                result = subprocess.run(['reg', 'query', 'HKCU\\Environment', '/v', 'GEMINI_API_KEY'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Extract the API key from the output
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if 'GEMINI_API_KEY' in line:
                            return line.split()[-1]
            except Exception:
                pass
        return os.environ.get("GEMINI_API_KEY")

    def expand_prompt(self, input_text, api_key="", unique_id=None, extra_pnginfo=None):
        if api_key:
            # Set the API key as a system environment variable
            if os.name == 'nt':  # Windows
                subprocess.run(f'setx GEMINI_API_KEY "{api_key}"', shell=True)
            else:  # macOS/Linux
                os.environ["GEMINI_API_KEY"] = api_key
                with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
                    bashrc.write(f'\nexport GEMINI_API_KEY="{api_key}"')
        else:
            api_key = self.get_api_key()

        if not api_key:
            raise ValueError("No API key provided. Please enter an API key or set the GEMINI_API_KEY environment variable.")

        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 150,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        prompt = f"""I will provide you a prompt to expand and visually describe. You will provide me the final prompt in the given format below. Remember to keep it under 150 words and try to describe it as best as possible so the AI can generate it perfectly visually. The output prompt must be in exact format like this (Directly start the response with Type:) - 

Type:
Subject:
Outfit:
Pose & Scene:
Extra Details:
Background:
Technical Details:

Example Input Prompt - Photograph of A woman as cinderella, wearing beautiful blue dress. holding a magic wand. wearing crystal glass heels. blue eyes. cinematic.. harmonious golden ratio composition. in a whimsical, storybook setting. using soft, ambient daylight. shot on Hasselblad 500C. using cool tones

Output Prompt - 
Type: Photograph of
Subject: A woman dressed as cinderella. Gorgeous and pretty with blue eyes, holding a magic wand.
Outfit: A blue royal dress, sparkling glass heels.
Pose & Scene: Holding a magic wand, weaving magic.
Extra Details: hollywood style cinematic scene, harmonious golden ratio composition. in a whimsical, storybook setting, using soft, ambient daylight.
Background: forest with deers and cute animals.
Technical Details: shot on Hasselblad 500C.

Here is the input prompt
Input Prompt: '{input_text}'"""
        response = chat_session.send_message(prompt)
        expanded_text = response.text

        # Update the node's widgets_values in the workflow
        if unique_id is not None and extra_pnginfo is not None:
            if isinstance(extra_pnginfo, list) and len(extra_pnginfo) > 0:
                if isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                    workflow = extra_pnginfo[0]["workflow"]
                    node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id)), None)
                    if node:
                        node["widgets_values"] = [input_text, "", expanded_text]  # Set API key to empty string

        return {"ui": {"text": [expanded_text], "api_key": ""}, "result": (expanded_text,)}

    @classmethod
    def IS_CHANGED(cls, input_text, api_key=""):
        return float("nan")  # This ensures the node is always executed

NODE_CLASS_MAPPINGS = {
    "GeminiPromptExpander": GeminiPromptExpander
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiPromptExpander": "Gemini Prompt Expander 🪄"
}