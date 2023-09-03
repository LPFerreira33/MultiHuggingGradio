from largelanguagemodel.interface.gradio_ui import GradioApp

if __name__ == "__main__":
    gui = GradioApp(model_config='chat_config.yaml')
    gui.run()
