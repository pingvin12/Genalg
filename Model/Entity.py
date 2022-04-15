import random as rnd

class Entity:
    def __init__(self, body):
        self.hash = rnd.getrandbits(128)
        self.body = body
        self.children = []
        self.parent = None

    def get_body(self) -> str: return self.body
    def set_body(self, body : str): self.body = body

    def get_hash(self) -> str: return self.hash

    def get_parent(self) -> 'Entity': return self.parent

    def set_parent(self, parent: 'Entity'): self.parent = parent

    def get_children(self) -> []: return self.children

    def add_children(self, children: 'Entity'): self.children.append(children)
