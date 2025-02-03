# class A:
#     # A is an empty class, no methods or attributes

#     class B(A):
#         def __init__(self, a: 'A'):
#             # Store the instance of A
#             self.a = a

#         def display(self):
#             return "This is class B, holding an instance of class A."


# # Instantiate class A (which does nothing)
# a_instance = A()

# # Instantiate class B, passing the instance of A
# b_instance = A.B(a_instance)

# # Call method in B to display information
# print(b_instance.display())  # Output: This is class B, holding an instance of class A.
