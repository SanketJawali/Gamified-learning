# Chapter 13: Polymorphism - The Art of Flexibility! 🎭

## 🎭 What is Polymorphism?
Imagine you have a **remote control** that can work with different devices—TV, AC, or a Music System. 
Even though they are different objects, the same remote can interact with them. This is **Polymorphism**!

In Python, **polymorphism** allows objects of different classes to be treated **as if they were the same**. 
It helps in writing flexible and reusable code! 🚀

---
## 🐶 Same Method, Different Behavior!

Different classes can have **methods with the same name** but different behavior.

### Example:

```python
class Dog:
    def speak(self):
        return "Woof! 🐶"

class Cat:
    def speak(self):
        return "Meow! 🐱"

# Using polymorphism
animals = [Dog(), Cat()]

for animal in animals:
    print(animal.speak())  
```
### Output:
```
Woof! 🐶
Meow! 🐱
```
Even though both `Dog` and `Cat` have a `speak()` method, they behave differently! 🐕🐈

---
## 🏛️ Polymorphism with Inheritance

A **child class** can override methods of the **parent class**, following its own behavior.

### Example:

```python
class Animal:
    def speak(self):
        return "I make some sound!"

class Dog(Animal):
    def speak(self):
        return "Woof! 🐶"

class Cat(Animal):
    def speak(self):
        return "Meow! 🐱"

animals = [Dog(), Cat(), Animal()]

for animal in animals:
    print(animal.speak())
```
### Output:
```
Woof! 🐶
Meow! 🐱
I make some sound!
```
The **same method** behaves differently in different classes! 🐾

---
## 📚 Polymorphism with Functions

A function can work with **objects of different classes** if they have the same method.

### Example:

```python
def animal_sound(animal):
    print(animal.speak())

dog = Dog()
cat = Cat()

animal_sound(dog)  # Output: Woof! 🐶
animal_sound(cat)  # Output: Meow! 🐱
```
This function works for **both** `Dog` and `Cat`, thanks to polymorphism! 🎭

---
## 🛠 Polymorphism with Built-in Methods

Python’s built-in functions like `len()` work on **different objects**.

### Example:

```python
print(len("Python"))  # Output: 6 (String)
print(len([1, 2, 3, 4]))  # Output: 4 (List)
print(len({"name": "Alice", "age": 25}))  # Output: 2 (Dictionary)
```
Even though **string, list, and dictionary** are different types, `len()` works on all of them! 🎯

---
## 🎭 Summary

- **Polymorphism** allows different objects to share the same method name but behave differently.
- **Inheritance** helps in method overriding, making it useful for polymorphism.
- **Functions** can handle different objects using polymorphism.
- **Built-in functions** like `len()` use polymorphism in Python.

With **Polymorphism**, you can make your code **more dynamic, flexible, and reusable**! 🚀🎭
