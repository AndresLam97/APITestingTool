import GUI
import Controller

if __name__ == '__main__':
    app = GUI.GUI()
    controller = Controller.Controller(app)
    controller.start_up()