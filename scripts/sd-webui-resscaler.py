import contextlib
from pathlib import Path

import gradio as gr

import modules.scripts as scripts
from modules.ui_components import ToolButton

class RSButton(ToolButton):
    def __init__(self, mul=1.0, **kwargs):
        super().__init__(**kwargs)

        self.mul = mul

    def apply(self, w, h):
        w = self.mul * w
        h = self.mul * h
        return list(map(round, [w, h]))

#     def reset(self, w, h):
#         return [self.res, self.res]

class ResScalerScript(scripts.Script):
    def title(self):
        return "Scale resolution saving aspect ratio"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Row(elem_id=f'{"img" if is_img2img else "txt"}2img_row_res_scaler'):
            btns = [
                RSButton(ar=0.5, value="0.5"),
                RSButton(ar=0.75, value="0.75"),
                RSButton(ar=1.5, value="1.5"),
                RSButton(ar=2, value="2")
            ]

            with contextlib.suppress(AttributeError):
                for b in btns:
                    if is_img2img:
                        resolution = [self.i2i_w, self.i2i_h]
                    else:
                        resolution = [self.t2i_w, self.t2i_h]

                    b.click(
                        b.apply,
                        inputs=resolution,
                        outputs=resolution,
                    )

    # https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/7456#issuecomment-1414465888
    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_width":
            self.t2i_w = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.t2i_h = component

        if kwargs.get("elem_id") == "img2img_width":
            self.i2i_w = component
        if kwargs.get("elem_id") == "img2img_height":
            self.i2i_h = component
