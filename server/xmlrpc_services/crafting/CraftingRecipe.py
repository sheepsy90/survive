
class CraftingRecipe():

    def __init__(self, id, name, representation_string, forbidden):
        self.id = id
        self.forbidden = forbidden
        self.name = name
        self.representation_string = representation_string
        self.results = []

    def get_representation_string(self):
        return self.representation_string

    def add_result(self, result):
        self.results.append(result)

    def get_recipe_result(self):
        return [(e.type_id, e.shape, e.initial_uses) for e in self.results]