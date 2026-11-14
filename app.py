import cv2
import gradio as gr
from filters import anonymize

def anonymize_photo(image, method):
    if image is None:
        return None
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    covered = anonymize(bgr, method)
    return cv2.cvtColor(covered, cv2.COLOR_BGR2RGB)

demo = gr.Interface(
    fn=anonymize_photo,
    inputs=[
        gr.Image(type="numpy", label="Photo"),
        gr.Radio(["blur", "pixelate", "box"], value="box", label="Method"),
    ],
    outputs=gr.Image(label="Anonymized"),
    title="Face anonymizer",
)

if __name__ == "__main__":
    demo.launch()
