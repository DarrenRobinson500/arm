class Setting:
    def __init__(self):
        self.current_class = 0
        self.rectangle_width = 40
        self.rectangle_height = 50
        self.image_directory = "images"
        self.label_directory = "labels"
        self.model_directory = "models"
        self.list_of_labels_path = self.label_directory + "/list_of_labels.txt"
        self.list_of_models_path = self.model_directory + "/list_of_models.txt"
        self.home_string = "C:/Users/darre/PycharmProjects/tkinter"


settings = Setting()
