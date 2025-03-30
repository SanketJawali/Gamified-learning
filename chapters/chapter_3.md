# 🚀 Chapter 3: Operators & Expressions – The Magic Behind Calculations!  

Welcome to **Chapter 3**! Now that you’ve learned about variables and data types, it's time to unleash the true power of Python! 🎩✨  

Have you ever wondered how calculators work? How do video games determine scores? How does a chatbot decide what to say next?  

The answer lies in **Operators & Expressions!** 🎯  

By the end of this chapter, you will:  
✅ Master different types of operators in Python.  
✅ Understand how to perform calculations and logical operations.  
✅ Learn how to combine variables to create powerful expressions.  
✅ Discover the magic of Boolean logic (True/False decisions).  

---

## 🧮 1️⃣ Arithmetic Operators: The Basics of Math  

Python can perform all kinds of mathematical operations just like a calculator. Here are the key arithmetic operators:  

| Operator | Symbol | Example | Result |
|----------|--------|---------|--------|
| Addition | `+` | `5 + 3` | `8` |
| Subtraction | `-` | `10 - 4` | `6` |
| Multiplication | `*` | `6 * 3` | `18` |
| Division | `/` | `8 / 2` | `4.0` |
| Floor Division | `//` | `7 // 2` | `3` (Removes decimal part) |
| Modulus (Remainder) | `%` | `10 % 3` | `1` |
| Exponentiation | `**` | `2 ** 3` | `8` |

🔹 **Example:**  

```python
a = 10
b = 3
print("Addition:", a + b)   # 13
print("Subtraction:", a - b)  # 7
print("Multiplication:", a * b)  # 30
print("Division:", a / b)  # 3.3333
print("Floor Division:", a // b)  # 3
print("Modulus:", a % b)  # 1
print("Exponentiation:", a ** b)  # 1000
```

🚀 **Fun Fact:** Python follows **PEMDAS** (Parentheses, Exponents, Multiplication & Division, Addition & Subtraction) just like in math!  

---

## ⚖️ 2️⃣ Comparison Operators: Making Decisions  

Comparison operators compare values and return either `True` or `False`.  

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `10 > 3` | `True` |
| `<` | Less than | `2 < 5` | `True` |
| `>=` | Greater than or equal to | `7 >= 7` | `True` |
| `<=` | Less than or equal to | `4 <= 6` | `True` |

🔹 **Example:**  

```python
x = 15
y = 20
print(x > y)  # False
print(x < y)  # True
print(x == y)  # False
print(x != y)  # True
```

🔮 **Where is this used?**  
- Checking if a user is old enough to access a website.  
- Determining who wins in a game.  
- Comparing prices in an online shopping app.  

---

## 🤖 3️⃣ Logical Operators: The Brain of Python  

Logical operators help us combine multiple conditions using **AND, OR, and NOT**.  

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `and` | Both conditions must be True | `5 > 3 and 10 > 2` | `True` |
| `or` | At least one condition must be True | `5 > 10 or 10 > 2` | `True` |
| `not` | Reverses the result | `not(5 > 3)` | `False` |

🔹 **Example:**  

```python
age = 20
has_id = True

if age >= 18 and has_id:
    print("You can enter the club!")  # ✅
else:
    print("Sorry, you can't enter!")  # ❌
```

🤯 **Did You Know?**  
- **AND** is like a strict teacher (both must be true).  
- **OR** is like a cool friend (just one is enough).  
- **NOT** is like a rule-breaker (flips the result).  

---

## 🧪 4️⃣ Assignment Operators: Storing Values  

Assignment operators assign and update values.  

| Operator | Example | Meaning |
|----------|---------|---------|
| `=` | `x = 5` | Assign `5` to `x` |
| `+=` | `x += 2` | `x = x + 2` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 4` | `x = x * 4` |
| `/=` | `x /= 2` | `x = x / 2` |
| `%=` | `x %= 3` | `x = x % 3` |

🔹 **Example:**  

```python
x = 10
x += 5  # x = x + 5
print(x)  # 15
x *= 2  # x = x * 2
print(x)  # 30
```

---

## 🎭 5️⃣ Identity & Membership Operators  

### 🔍 Identity Operators (`is`, `is not`)  
They check if two variables refer to the same object in memory.  

🔹 **Example:**  

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True (values are same)
print(a is b)  # False (different objects)
```

### 🔎 Membership Operators (`in`, `not in`)  
They check if a value exists in a list, string, or tuple.  

🔹 **Example:**  

```python
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)  # True
print("grape" not in fruits)  # True
```

---

## 📝 Quick Recap: What We Learned  

✅ Arithmetic operators help in performing math operations.  
✅ Comparison operators help compare values.  
✅ Logical operators help combine multiple conditions.  
✅ Assignment operators update variable values.  
✅ Identity and Membership operators check for references and elements in collections.  

---

## 🎯 What’s Next?  
🔜 **Chapter 4: Conditional Statements** – Learn how to make smart decisions in Python using `if-else` statements! 🌟  
