Using a **virtual environment (venv)** is a best practice for Python projects. It helps manage dependencies and ensures your project runs in an isolated environment. Here's how you can set up and use a virtual environment for the **Web Vulnerability Scanner** project:

---

### **Step 1: Create a Virtual Environment**

1. Open your terminal or command prompt.
2. Navigate to the root directory of your project (`web-vuln-scanner/`).
3. Run the following command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

   This will create a folder named `venv` in your project directory, which contains the virtual environment.

---

### **Step 2: Activate the Virtual Environment**

#### **On Windows:**
```bash
venv\Scripts\activate
```

#### **On macOS/Linux:**
```bash
source venv/bin/activate
```

Once activated, you'll see `(venv)` at the beginning of your terminal prompt, indicating that the virtual environment is active.

---

### **Step 3: Install Dependencies**

1. With the virtual environment activated, install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies for the dynamic crawler:

   ```bash
   cd core/crawler
   npm install puppeteer
   cd ../..
   ```

---

### **Step 4: Run the Project**

1. Start the Flask application:

   ```bash
   python run.py
   ```

2. Access the web interface by opening `http://localhost:5000` in your browser.

---

### **Step 5: Deactivate the Virtual Environment**

When you're done working on the project, you can deactivate the virtual environment by running:

```bash
deactivate
```

This will return your terminal to the global Python environment.

---

### **Step 6: Using Virtual Environment in IDEs**

#### **VS Code**
1. Open the project in VS Code.
2. Press `Ctrl+Shift+P` and search for **Python: Select Interpreter**.
3. Choose the interpreter located in the `venv` folder (e.g., `venv/bin/python` on macOS/Linux or `venv\Scripts\python.exe` on Windows).

#### **PyCharm**
1. Open the project in PyCharm.
2. Go to `File > Settings > Project: web-vuln-scanner > Python Interpreter`.
3. Click the gear icon and select `Add`.
4. Choose `Existing environment` and select the Python executable from the `venv` folder.

---

### **Step 7: Add `venv` to `.gitignore`**

To avoid committing the virtual environment to your Git repository, add the `venv` folder to your `.gitignore` file:

```bash
# .gitignore
venv/
```

---

### **Step 8: Recreate the Virtual Environment (Optional)**

If you need to recreate the virtual environment (e.g., on a new machine), follow these steps:

1. Delete the existing `venv` folder:
   ```bash
   rm -rf venv
   ```

2. Recreate the virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment and install dependencies again:
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

---
