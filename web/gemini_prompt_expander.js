import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "Comfy.GeminiPromptExpander",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "GeminiPromptExpander") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                onNodeCreated?.apply(this, arguments);

                // Add a widget for expanded text
                const expandedTextWidget = ComfyWidgets.STRING(this, "Final Prompt", ["STRING", { multiline: true }], app);
                expandedTextWidget.widget.inputEl.readOnly = true;
                expandedTextWidget.widget.inputEl.style.opacity = 0.6;
                expandedTextWidget.widget.inputEl.style.minHeight = "10px";
                this.expandedTextWidget = expandedTextWidget.widget;

                // Modify the API key input behavior
                const apiKeyWidget = this.widgets.find(w => w.name === "api_key");
                if (apiKeyWidget) {
                    const originalOnChange = apiKeyWidget.callback;
                    apiKeyWidget.callback = function(value) {
                        if (value) {
                            // API key entered, trigger the node execution
                            app.graph.runStep();
                        }
                        originalOnChange?.(value);
                    };
                }
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                onExecuted?.apply(this, arguments);
                if (message && message.text && this.expandedTextWidget) {
                    let expandedText = message.text[0];
                    if (Array.isArray(expandedText)) {
                        expandedText = expandedText.join('');
                    }
                    
                    this.expandedTextWidget.value = expandedText;
                    this.expandedTextWidget.inputEl.value = expandedText;
                    this.expandedTextWidget.inputEl.style.height = 'auto';
                    this.expandedTextWidget.inputEl.style.height = this.expandedTextWidget.inputEl.scrollHeight + 'px';
                }

                // Clear the API key input after execution
                const apiKeyWidget = this.widgets.find(w => w.name === "api_key");
                if (apiKeyWidget) {
                    apiKeyWidget.value = "";
                    apiKeyWidget.inputEl.value = "";
                }
            };
        }
    }
});