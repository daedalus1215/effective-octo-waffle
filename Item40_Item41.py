# Initialize Paren Classes with super
# prior approach was to call parent's __init__, but this has issues in many cases.
# To solve the standard method resolution order (MRO), Python provides the super keyword.
# The MRO defines the ordering in which superclasses are initialized, following an algo called C3 linearization
# Diamond-shaped class hierarchy:

class MyBaseClass:
    def __init__(self, value):
        self.value = value



class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

# MyBaseClass.__init__, is run only a single time. The other parent classes are run in the order specified in the
# class statement:
class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)


food = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', food.value)


# If you find yourself desiring the convenience and encap that come with multi inheritance,
# but want to avoid potential headaches, consider writing a mix-in instead.

# mixin is a class that defines only a small set of additional methods for its child classes to provide.
# mixins classes dont define their own instance attributes nor require their __init__ constructor to be called

class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# Make a binary tree class that leverages the mixin
class BinaryTree(ToDictMixin):
    def __init__(self,value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))

print(tree.to_dict())

# Can pick and choose which mixin methods you want to leverage and which you want to override.
class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # prevent cycles
        else:
            return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(0, parent=root.left)
print(root.to_dict())





