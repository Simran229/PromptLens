import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory prompt history
history = []

# Single model prompt call
def ask_llm(prompt, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        usage = response.usage

        # Save to history
        history.append({
            "prompt": prompt,
            "model": model,
            "response": answer
        })

        token_info = (
            f"Prompt Tokens: {usage.prompt_tokens}, "
            f"Completion Tokens: {usage.completion_tokens}, "
            f"Total: {usage.total_tokens}"
        )

        return answer, token_info

    except Exception as e:
        return f"Error: {str(e)}", ""

# --- Compare GPT-3.5 and GPT-4 ---
def ask_both_models(prompt):
    try:
        responses = {}
        token_info = {}

        for model in ["gpt-3.5-turbo", "gpt-4"]:
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            responses[model] = res.choices[0].message.content
            usage = res.usage
            token_info[model] = (
                f"Prompt: {usage.prompt_tokens}, "
                f"Completion: {usage.completion_tokens}, "
                f"Total: {usage.total_tokens}"
            )

        # Save comparison to history
        history.append({
            "prompt": prompt,
            "model": "both",
            "response": responses
        })

        return (
            responses["gpt-3.5-turbo"],
            token_info["gpt-3.5-turbo"],
            responses["gpt-4"],
            token_info["gpt-4"]
        )

    except Exception as e:
        return f"Error: {str(e)}", "", "", ""

# Format recent history for display
def format_history():
    if not history:
        return "No history yet."
    formatted = ""
    for i, entry in enumerate(reversed(history[-5:])):
        formatted += f"🔹 Prompt {len(history)-i} [{entry['model']}]:\n{entry['prompt']}\n→ {entry['response'] if isinstance(entry['response'], str) else '[Multiple Responses]'}\n\n"
    return formatted

# Reload prompt from history
def fill_prompt(index):
    idx = len(history) - 1 - index  # reverse index
    entry = history[idx]
    return entry["prompt"], entry["model"] if entry["model"] != "both" else "gpt-3.5-turbo"

# UI
with gr.Blocks() as demo:
    gr.Markdown("# Prompt Debugger with Side-by-Side Comparison")

    with gr.Tab("Single Model"):
        with gr.Row():
            prompt_input = gr.Textbox(label="Enter Prompt", lines=4)
            model_select = gr.Dropdown(["gpt-3.5-turbo", "gpt-4"], value="gpt-3.5-turbo", label="Select Model")

        submit_btn = gr.Button("Submit")

        with gr.Row():
            output_box = gr.Textbox(label="LLM Response", lines=8)
            tokens_box = gr.Textbox(label="Token Usage", max_lines=1)

        history_display = gr.Textbox(label="Recent Prompt History", lines=12)

        # Submit action
        submit_btn.click(
            fn=ask_llm,
            inputs=[prompt_input, model_select],
            outputs=[output_box, tokens_box]
        ).then(
            fn=lambda: format_history(),
            inputs=[],
            outputs=[history_display]
        )

    with gr.Tab("Compare GPT-3.5 vs GPT-4"):
        compare_prompt = gr.Textbox(label="Enter Prompt", lines=4)
        compare_btn = gr.Button("Compare")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### GPT-3.5 Output")
                gpt35_output = gr.Textbox(label="GPT-3.5 Response", lines=8)
                gpt35_tokens = gr.Textbox(label="Token Usage (3.5)")

            with gr.Column():
                gr.Markdown("### GPT-4 Output")
                gpt4_output = gr.Textbox(label="GPT-4 Response", lines=8)
                gpt4_tokens = gr.Textbox(label="Token Usage (4)")

        compare_btn.click(
            fn=ask_both_models,
            inputs=[compare_prompt],
            outputs=[gpt35_output, gpt35_tokens, gpt4_output, gpt4_tokens]
        )

demo.launch()
