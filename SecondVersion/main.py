import tags
import Controller

if __name__ == '__main__':
    app = tags.App()
    controller = Controller.Controller(app)
    app.start_up()
    