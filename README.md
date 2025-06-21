# PromptLens

PromptLens is a simple yet powerful web-based tool built with Gradio and Python for testing and comparing prompts across different OpenAI GPT models. It provides a clean interface for rapid prompt engineering, allowing you to see how different models respond to the same input and how many tokens each interaction consumes.

## Features

-   **Single Model Testing**: Send a prompt to a specific model (`gpt-3.5-turbo` or `gpt-4`) and view the response.
-   **Side-by-Side Comparison**: Send a single prompt to both `gpt-3.5-turbo` and `gpt-4` simultaneously to directly compare their outputs.
-   **Token Usage Tracking**: See detailed token counts (prompt, completion, and total) for every API call to monitor costs and performance.
-   **Prompt History**: Keeps a running history of your recent prompts for easy reference and reuse.