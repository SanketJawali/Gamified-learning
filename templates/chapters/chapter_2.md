# 🚀 Chapter 2: Variables and Data Types – Storing the Magic in Python!

Welcome back, future Python pro! 🎉 Now that you’ve written your first Python program, it’s time to learn how to store and manipulate data using variables and data types. Think of variables as magical containers that hold information, ready to be used whenever needed! ✨

## By the end of this chapter, you’ll be able to:
✅ Understand what variables are and how to use them.  
✅ Learn about different data types in Python.  
✅ Perform basic operations with variables.  
✅ Take user input and store it in variables.  

So, grab your wand (or keyboard) and let’s dive in! 🧙‍♂️  

---

## 🎭 What Are Variables? – The Storage Boxes of Python

Imagine you have a magical storage box where you can put different things—numbers, words, or even entire books! In Python, these storage boxes are called variables.

### Here’s how you create a variable:

```python
name = "Alice"
age = 25
```

In the above example:
- `name` stores the text `"Alice"` (a string).
- `age` stores the number `25` (an integer).

---

## 🎨 Naming Variables – The Do’s and Don’ts

✔️ **Allowed:**  
- ✅ Use letters, numbers, and underscores (`_`)
- ✅ Must start with a letter or underscore, not a number
- ✅ Should be descriptive (`user_name` is better than `x`)

❌ **Not Allowed:**  
- 🚫 `2name = "Bob"` (Cannot start with a number)
- 🚫 `user-name = "Charlie"` (No hyphens)
- 🚫 `class = "Python"` (Avoid reserved keywords like `class`, `if`, `def`)

---

## 🧪 Data Types in Python – The Ingredients of Your Code

Python automatically recognizes different types of data. Let’s explore the most common ones:

### 1️⃣ Strings (Text Data)
Used for storing words, sentences, or any text. Enclose them in single or double quotes.

```python
greeting = "Hello, Python!"
```

🎯 **Fun Fact:** You can combine strings using `+` (concatenation):

```python
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)  # Output: John Doe
```

### 2️⃣ Numbers (Integers & Floats)
- **Integers (`int`)** → Whole numbers (`10`, `-5`, `1000`)
- **Floats (`float`)** → Decimal numbers (`3.14`, `-2.5`, `100.99`)

```python
score = 100      # Integer
pi = 3.14159     # Float
```

### 3️⃣ Boolean (True/False)
Booleans represent yes/no or true/false conditions.

```python
is_sunny = True
has_coffee = False
```

### 4️⃣ Lists – Collections of Data
A list stores multiple values in a single variable.

```python
colors = ["red", "green", "blue"]
print(colors[0])  # Output: red
```

🎯 **Fun Fact:** Lists are ordered and can be modified!

---

## ✨ Playing with Variables – Let's Do Some Magic!

### 🎲 Mathematical Operations
Python can act like a calculator!

```python
x = 10
y = 5

print(x + y)  # Addition (15)
print(x - y)  # Subtraction (5)
print(x * y)  # Multiplication (50)
print(x / y)  # Division (2.0)
print(x ** y) # Exponentiation (10^5 = 100000)
```

### 🔄 Changing Variable Values
Variables can be reassigned at any time:

```python
age = 20
print(age)  # Output: 20

age = 25
print(age)  # Output: 25
```

🔮 **Python is dynamic!** You don’t need to specify types; Python figures it out automatically!

---

## ⌨️ Taking User Input – Let’s Make It Interactive! 🎤

### 📝 Basic Input Example

```python
name = input("What is your name? ")
print("Hello, " + name + "!")
```

📌 **How It Works:**  
- The `input()` function pauses the program and waits for user input.  
- The entered data is stored in the variable (`name`).  
- The program then prints a greeting with the user's name.  

### 🔢 Taking Numeric Input
By default, `input()` takes everything as a string. If you need a number, convert it using `int()` or `float()`.

```python
age = input("Enter your age: ")
print("You are " + age + " years old!")
```

🚨 **Problem:** This treats `age` as a string. If we try mathematical operations, Python will throw an error.

✔️ **Correct Way:** Convert to Integer (`int`)

```python
age = int(input("Enter your age: "))
print("Next year, you will be", age + 1, "years old!")
```

✔️ **For Decimal Numbers (`float`)**

```python
height = float(input("Enter your height in meters: "))
print("Your height is", height, "meters.")
```

### 🔹 Python Keywords
Python **keywords** are reserved words that have special meanings and cannot be used as variable names. They define the structure and logic of Python programs.

#### List of Python Keywords:

```python
import keyword
print(keyword.kwlist)
```

Common Python keywords:

| Keyword  | Purpose |
|----------|---------|
| `if`     | Conditional statements |
| `for`    | Looping structure |
| `def`    | Function definition |
| `class`  | Class definition |
| `return` | Return a value from a function |
| `import` | Importing modules |
| `try`    | Exception handling |
| `in`     | Membership test |

These keywords help Python understand your code better. For example:

```python
if age >= 18:
    print("You are an adult.")
```

Python will **not allow** using keywords as variable names:

```python
class = "Math"  # ❌ Error! 'class' is a keyword
```
### 🤹‍♂️ Combining Inputs and Outputs
Let's create a simple interactive program!

```python
name = input("Enter your name: ")
fav_color = input("What is your favorite color? ")

print(name + " likes " + fav_color + "!")
```

🎉 Try entering different values and see the magic!

---

## 📝 Quick Recap: What We Learned

✅ Variables store data and can be updated.  
✅ Python has different data types: **strings, numbers, booleans, and lists**.  
✅ You can perform operations on numbers and combine strings.  
✅ The `input()` function allows users to enter data.  
✅ Python keywords are reserved words with special meanings.   
✅ Convert input data using `int()` or `float()` when needed.  

---

## 🎯 What’s Next?
🔜 **Chapter 3: Operators and Expressions** – Learn how to perform calculations and logical operations in Python! 🧮
