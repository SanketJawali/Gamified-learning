# 🚀 Chapter 5: Loops in Python – The Power of Repetition!  

Welcome, future Python pro! 🎉 Now that you've mastered conditional statements, it’s time to make your code even more powerful with loops!  

Imagine you have to print numbers from 1 to 100. Would you type 100 print statements? Of course not! That’s where loops come in—your personal assistant that repeats tasks for you! 🔄✨  

By the end of this chapter, you’ll be able to:  
✅ Understand the concept of loops in Python.  
✅ Use `for` loops and `while` loops efficiently.  
✅ Control loops using `break`, `continue`, and `pass`.  
✅ Loop through strings, lists, and ranges.  

So, grab your Python wand 🪄 and let’s get looping!  

---

## 🎭 What Are Loops? – The Time-Saving Spell  

A **loop** allows you to repeat a block of code multiple times without writing it again and again. Python has two types of loops:  

1️⃣ **For Loop** – Used when you know how many times you want to repeat something.  
2️⃣ **While Loop** – Used when you want to repeat something **until** a condition is met.  

Let’s explore both!  

---

## 🔄 1️⃣ The `for` Loop – A Smart Repeater  

A `for` loop repeats a task for a fixed number of times. It’s often used with lists, strings, and ranges.  

### 🔹 Example: Printing Numbers from 1 to 5  

```python
for i in range(1, 6):  
    print(i)  
```  

**Output:**  
```
1  
2  
3  
4  
5  
```  

📌 **How it works:**  
- `range(1, 6)` generates numbers from 1 to 5 (6 is **excluded**).  
- The loop repeats for each number in the range.  
- `print(i)` displays the current number.  

---

## 🧑‍🎨 Looping Through Lists and Strings  

Python allows you to loop through lists and even strings!  

### 🔹 Example: Looping Through a List  

```python
colors = ["red", "green", "blue"]  
for color in colors:  
    print(color)  
```  

**Output:**  
```
red  
green  
blue  
```  

### 🔹 Example: Looping Through a String  

```python
word = "Python"  
for letter in word:  
    print(letter)  
```  

**Output:**  
```
P  
y  
t  
h  
o  
n  
```  

---

## 🔁 2️⃣ The `while` Loop – The Guardian of Conditions  

A `while` loop repeats **as long as** a condition is true. It’s perfect when you don’t know how many times you need to repeat.  

### 🔹 Example: Counting Down  

```python
count = 5  
while count > 0:  
    print(count)  
    count -= 1  
```  

**Output:**  
```
5  
4  
3  
2  
1  
```  

📌 **How it works:**  
- The loop **runs while** `count > 0`.  
- `count -= 1` reduces `count` each time, stopping when it reaches 0.  

---

## ⚡ Loop Control: `break`, `continue`, and `pass`  

Python gives you **superpowers** to control loops!  

### 🔥 `break` – Stops the Loop  

```python
for i in range(1, 10):  
    if i == 5:  
        break  
    print(i)  
```  

**Output:**  
```
1  
2  
3  
4  
```  

🚀 The loop **stops** when `i == 5`.  

### 🔄 `continue` – Skips the Current Iteration  

```python
for i in range(1, 6):  
    if i == 3:  
        continue  
    print(i)  
```  

**Output:**  
```
1  
2  
4  
5  
```  

📌 **Skips** `3` but continues with the rest.  

### 😴 `pass` – Does Nothing (A Placeholder)  

```python
for i in range(1, 6):  
    if i == 3:  
        pass  # Placeholder  
    print(i)  
```  

📌 `pass` is useful when planning code but **not** ready to implement logic.  

---

## 🎯 Quick Recap  

✅ `for` loops repeat for a known number of times.  
✅ `while` loops repeat **until** a condition is false.  
✅ Use `break` to stop a loop.  
✅ Use `continue` to skip an iteration.  
✅ Use `pass` as a placeholder.  

---

## 🔮 What’s Next?  

🌟 **Chapter 6: Functions – Writing Reusable Code!** Get ready to make your programs smarter with functions! 🚀  
