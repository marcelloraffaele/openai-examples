# pip install gradio
import gradio as gr

def greet(name, intensity, file1):
    return (
        "# Hello, " + name + "!" * int(intensity) +
        "\n## Files" +
        "\n- First file chosen: " + file1.name,
        file1
    )

demo = gr.Interface(
    fn=greet,
    inputs=[
        "text",
        "slider",
        gr.File(label="First file"),
        
    ],
    outputs=[ gr.Markdown(), gr.Image(label="Image") ],
    title="Compare",
)

demo.launch()