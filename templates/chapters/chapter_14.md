# Chapter 14: Encapsulation - The Secret Vault of Python! 🔐🏦  

## 🔍 What is Encapsulation? 🤔  

Imagine you own **a magical treasure chest**! 🏆✨  
- The **treasure** inside is **your important data** (money, diamonds, secrets).  
- The **chest** itself is your **class** that protects the treasure.  
- The **lock and key** are the **methods** that control access to your treasure.  

**Encapsulation** means **hiding** the details of your treasure chest and **allowing controlled access** to it using a key! 🔑  

In Python, Encapsulation:  
✅ **Protects data** from unauthorized access 🚫  
✅ **Allows controlled modification** via special functions 🔄  
✅ **Prevents accidental changes** that could break your program 🛑  

---

## 🏰 The Three Security Levels of Encapsulation  

In Python, attributes (variables inside a class) can have **three levels of protection**:  

### 🟢 1. Public: The Open Field 🌍  
Data is **fully accessible** by anyone—just like a **park** where anyone can walk in!  

```python
class Hero:
    def __init__(self, name, power):
        self.name = name    # Public attribute
        self.power = power  # Public attribute

superman = Hero("Superman", "Flight")
print(superman.name)   # ✅ Output: Superman
print(superman.power)  # ✅ Output: Flight
```
📢 **Warning:** Since `name` and `power` are public, anyone can **modify** them!  

```python
superman.name = "Batman"  
print(superman.name)  # ❌ Oh no! Superman became Batman!
```

---

### 🟡 2. Protected: Handle with Care! ⚠️  
A **protected** attribute **should not be modified directly**.  
It’s like a **“Do Not Touch” sign**—you *can* access it, but you *shouldn’t*!  

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected attribute

account = BankAccount(5000)
print(account._balance)  # ⚠️ Allowed, but not recommended!
```
🤔 **Why use `_balance` instead of `balance`?**  
🔹 The **underscore (`_`) is a convention** that means:  
🚧 *"I am important! Please don't mess with me directly!"*  

---

### 🔴 3. Private: The Secret Vault! 🔒  
A **private** attribute is **completely hidden**—like a **vault locked with a password**!  

```python
class Safe:
    def __init__(self, secret_code):
        self.__secret_code = secret_code  # Private attribute

vault = Safe("007")
print(vault.__secret_code)  # ❌ ERROR! You can't access it directly!
```
💡 **Python protects `__secret_code` from being accessed directly!**  

---

## 🔑 Unlocking Private Data - The Getter & Setter Keys 🗝️  

Even though **private attributes** are hidden, we can access them using **getter** and **setter** methods!  

### 🏠 Getter (To View Data)  
Think of a getter as a **"peep hole"** into your vault. It lets you **see inside but not change anything**!  

```python
class Safe:
    def __init__(self, secret_code):
        self.__secret_code = secret_code  

    def get_secret_code(self):  # Getter method
        return self.__secret_code  

vault = Safe("007")
print(vault.get_secret_code())  # ✅ Output: 007
```
---

### 🔄 Setter (To Modify Data Safely)  
A setter is like a **secure door**—it lets you **update the value**, but only in a **controlled way**!  

```python
class Safe:
    def __init__(self, secret_code):
        self.__secret_code = secret_code  

    def get_secret_code(self):
        return self.__secret_code  

    def set_secret_code(self, new_code):
        if isinstance(new_code, str) and len(new_code) == 3:
            self.__secret_code = new_code
        else:
            print("❌ Invalid code! It must be a 3-character string.")

vault = Safe("007")
vault.set_secret_code("123")  # ✅ Allowed
print(vault.get_secret_code())  # Output: 123

vault.set_secret_code(999)  # ❌ Error: Only strings allowed!
```
**🔐 Why use setters?**  
- Prevents **accidental overwriting** of important data.  
- Allows **validation** before changing values.  

---

## 🚪 Name Mangling - The Backdoor Entry! 🚷  
Although private variables **cannot** be accessed directly, Python has a **backdoor trick** called **name mangling**. 🚪  

```python
print(vault._Safe__secret_code)  # Output: 123
```
⚠️ **Warning:** **Never use this unless absolutely necessary!** It's meant for debugging, not regular use!  

---

## 🎭 Real-World Example: A Smart TV Remote! 📺  

Think of a **TV remote** as an example of Encapsulation:  
- The **buttons (public methods)** allow users to interact with the TV.  
- The **circuit inside (private data)** controls how the TV works.  
- **You can't modify the circuit directly!** You have to use the buttons.  

```python
class SmartTV:
    def __init__(self):
        self.__volume = 10  # Private variable

    def increase_volume(self):
        if self.__volume < 100:
            self.__volume += 1
            print(f"Volume: {self.__volume}")
        else:
            print("Max volume reached!")

    def get_volume(self):  # Getter method
        return self.__volume

tv = SmartTV()
tv.increase_volume()  # ✅ Output: Volume: 11
print(tv.get_volume())  # ✅ Output: 11
```
💡 **Encapsulation ensures we control the volume safely!**  

---

## 🎯 Summary - Encapsulation in a Nutshell!  

| Encapsulation Level | Symbol | Access | Usage Example |
|---------------------|--------|--------|---------------|
| Public | None | 🌍 Fully accessible | `self.name` |
| Protected | `_single_underscore` | ⚠️ Accessible but discouraged | `self._password` |
| Private | `__double_underscore` | 🔒 Completely hidden | `self.__bank_pin` |

🔹 **Encapsulation** protects data and ensures that only controlled modifications happen!  
🔹 **Use getter & setter methods** to safely interact with private data.  
🔹 **Real-world examples:** Bank accounts, smart TVs, medical records, and more!  

---

## 🏆 Encapsulation Challenge! 🏆  

Create a **BankAccount** class with the following features:  
1️⃣ **Private `__balance` attribute**  
2️⃣ **Getter method `get_balance()`**  
3️⃣ **Setter method `deposit(amount)` (only positive values allowed!)**  
4️⃣ **Setter method `withdraw(amount)` (don’t allow overdraft!)**  

💡 **Bonus:** Print an error message if the user tries to withdraw more than the balance!  

Try coding this and test it yourself! 🚀  
