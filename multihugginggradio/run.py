from multihugginggradio.interface.gradio_ui import GradioApp

if __name__ == "__main__":
    gui = GradioApp(model_config='config.yaml')
    gui.run()
