# 📂 Chapter 8: File Handling in Python – Unlocking the Power of Data Storage! 🚀  

Welcome, Python explorer! 🌍✨ Until now, your programs have worked with data in variables, lists, and dictionaries. But what happens when you close your program? Poof! All that data is **gone**! 😱  

Wouldn't it be amazing if we could **save** our data and bring it back anytime? Well, that’s exactly what **file handling** allows us to do! 📁🔓  

By the end of this chapter, you’ll be able to:  
✅ Open, read, and write files in Python.  
✅ Work with different file modes (`r`, `w`, `a`, `r+`).  
✅ Use the `with open()` statement for safe file handling.  
✅ Handle file-related errors like a pro!  

So, grab your digital notebook, and let’s dive into the world of **file handling!** 🚀  

---

## 📜 Why Do We Need File Handling?  

Imagine you're writing a **diary** app. Without file handling, every time you close the app, all your entries disappear! **File handling** lets us:  
📌 **Store** user data permanently.  
📌 **Read** data from files and process it.  
📌 **Modify** files without losing existing content.  
📌 **Log errors** and track program execution.  

---

## 🔓 Opening a File – The First Step!  

Before reading or writing a file, we must **open** it. Python provides the `open()` function:  

```python
file = open("myfile.txt", "r")  # Open a file in read mode
```

The `open()` function takes **two** parameters:  
1️⃣ **File name**: `"myfile.txt"`  
2️⃣ **Mode**: `"r"` (read), `"w"` (write), `"a"` (append), or `"r+"` (read & write).  

### 🔍 File Modes:
| Mode | Meaning |
|------|---------|
| `"r"`  | Read mode (default) – Opens file for reading. Error if file doesn’t exist. |
| `"w"`  | Write mode – Creates a new file (or overwrites an existing one). |
| `"a"`  | Append mode – Adds new data to the file without deleting existing content. |
| `"r+"` | Read & Write mode – Allows reading and writing in a file. |

---

## 📖 Reading a File – Bringing Data to Life!  

### **1️⃣ Reading the Whole File**
```python
file = open("myfile.txt", "r")
content = file.read()
print(content)  # Displays the file content
file.close()  # Always close the file after reading
```

### **2️⃣ Reading Line by Line**
```python
file = open("myfile.txt", "r")
for line in file:
    print(line.strip())  # Print each line without extra newlines
file.close()
```

---

## ✍️ Writing to a File – Saving Your Work!  

### **1️⃣ Writing New Content (`"w"`)**
```python
file = open("diary.txt", "w")
file.write("Today was an amazing day!\n")
file.write("I learned file handling in Python.\n")
file.close()
```

### **2️⃣ Adding Content (`"a"`)**
```python
file = open("diary.txt", "a")
file.write("Tomorrow, I'll practice more!\n")
file.close()
```

---

## 🔒 The Safe Way: Using `with open()`  

Using `with open()`, you **don’t need** to manually close the file—it’s done automatically!  

```python
with open("myfile.txt", "r") as file:
    content = file.read()
    print(content)  # File closes automatically after this block
```

---

## 🚨 Handling File Errors Like a Pro!  

```python
try:
    with open("nonexistent.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("Oops! The file doesn’t exist.")
```

---

## 🏆 Mini Project: A Simple To-Do List App!  

```python
def add_task(task):
    with open("tasks.txt", "a") as file:
        file.write(task + "\n")

def show_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            if tasks:
                print("\nYour Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.strip()}")
            else:
                print("No tasks yet. Add one!")
    except FileNotFoundError:
        print("No tasks file found. Start by adding a task!")

# Menu
while True:
    print("\n1. Add Task  2. Show Tasks  3. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        task = input("Enter a new task: ")
        add_task(task)
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Try again.")
```

---

## 📝 Quick Recap: What We Learned  

✅ **Opening, reading, and writing files** in Python.  
✅ Different **file modes** (`r`, `w`, `a`, `r+`).  
✅ Using `with open()` for **safe** file handling.  
✅ **Handling file errors** with `try-except`.  
✅ **Creating a simple To-Do List** using file handling!  

---

## 🎯 What’s Next?  
🔜 **Chapter 9: Exception Handling** – Learn how to handle errors and make your code **bug-proof!** 🛠️  
