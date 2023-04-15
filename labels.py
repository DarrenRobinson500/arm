from settings import *
import os

class MyLabel:
    def __init__(self, name, model, colour, width, height, external_update=True):
        self.number = len(model.labels)
        self.name = name
        self.model = model
        self.colour = colour
        self.width = width
        self.height = height
        self.model.labels.append(self)
        if external_update:
            model.write_labels_to_file()

    def __str__(self):
        return f"Label Name: {self.name} Number: {self.number} Colour: {self.colour}"

    def delete(self):
        self.model.labels.remove(self)
        self.model.write_labels_to_file()




# load_labels()

# print(labels)

