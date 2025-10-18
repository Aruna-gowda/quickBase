```markdown
# 🧪 QuickBase Automation Framework (Pytest + Playwright)

This repository contains an end-to-end **web automation testing framework** built using **Python**, **Pytest**, and **Playwright**.  
It follows the **Page Object Model (POM)** design pattern for better maintainability and scalability.  
Allure is integrated for generating rich HTML test execution reports.

## 📁 Project Structure

quickBase/
│
├── conftest.py               # Pytest fixtures for browser setup & configuration
├── pytest.ini                # Pytest configuration file
├── requirements.txt          # List of dependencies
├── .env                      # Environment variables (URL, credentials, etc.)
│
├── pageObjects/              # Page Object Model layer
│   ├── BasePage.py
│   ├── login_page.py
│   ├── Table_page.py
│   └── **init**.py
│
├── testCases/                # Test scripts using pytest
│   ├── test_login.py
│   ├── test_Table.py
│   └── ...
│
├── configurations/           # Configuration and credentials
│   └── config.ini
│
└── reports/                  # Stores Allure or HTML reports
└── allure-results/


## ⚙️ Features

✅ Built using **Pytest + Playwright**  
✅ Modular design with **Page Object Model (POM)**  
✅ Supports **environment variable management** via `.env`  
✅ Integrated with **Allure Reports** for rich test visualization  
✅ CI/CD-ready with **GitHub Actions**  
✅ Supports **manual or scheduled GitHub runs**  

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/quickBase.git
cd quickBase
````

### 2️⃣ Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create or update `.env` with your credentials:

```
url = app_urk
Email=your_email
Password=your_password
AppPassword = your_apppassword
```
## 🧩 Run Tests Locally

### Run All Tests

```bash
pytest -v --alluredir="./reports"
```

### Run a Specific Test

```bash
pytest testCases/test_login.py --alluredir="./reports
```

### Generate Allure Report

```bash
allure serve "./reports"
```

## 🔄 Framework Flow

1. **Pytest** loads config from `pytest.ini`
2. **conftest.py** initializes browser and fixtures
3. Test scripts under `testCases/` use **pageObjects**
4. Results saved to `./reports`
5. **Allure CLI** converts results to allure HTML report

---

## 🧠 How It Works

| Component          | Description                                 |
| ------------------ | ------------------------------------------- |
| `pytest.ini`       | Defines pytest options and Allure directory |
| `conftest.py`      | Sets up Playwright browser and fixtures     |
| `pageObjects/`     | Encapsulates reusable page logic            |
| `testCases/`       | Test scripts calling Page Object methods    |
| `.env`             | Stores credentials & URLs securely          |
| `reports/`         | Stores Allure report outputs                |
| `requirements.txt` | Defines Python dependencies                 |

---

## 🧰 Key Technologies

* **Python 3.11+**
* **Pytest**
* **Playwright**
* **Allure-pytest**
* **python-dotenv**

## 🔧 CI/CD Integration with GitHub Actions

This framework integrates with **GitHub Actions** to automatically:

* Install dependencies
* Run Pytest + Playwright tests
* Generate Allure reports
* Deploy Allure report to **GitHub Pages**


✅ **Pipeline Highlights:**

* Runs on **manual trigger**
* Stores credentials securely via **GitHub Secrets**
* Publishes allure report to **GitHub Pages**
* Send email with report link to recipients using Gmail credentials in secrets

---

## ▶️ How to Run the Workflow from GitHub Manually

You can trigger the Playwright automation workflow directly from your **GitHub repository** without using the command line.

### 🪜 Steps:

1. Go to your **GitHub repository**.
2. Click on the **“Actions”** tab.
3. Select the workflow name (e.g., *Quickbase Web Automation Testcases*).
4. On the right-hand side, click the **“Run workflow”** dropdown.
5. Choose the **branch** (e.g., `main`).
6. Click **Run workflow**.

> 🔹 This works because of the `workflow_dispatch` event in the YAML file.
> 🔹 The workflow will automatically install dependencies, execute tests, generate the Allure report, and publish it.

### 🧾 Viewing Results

Once the workflow finishes:

* Go to the **Actions → Completed Run → Summary**
* Download the **Allure Report artifact**, or
* Visit your **GitHub Pages link**, for example:

  ```
  https://<username>.github.io/quickBase/
  ```

## 👩‍💻 Author

**Aruna**
Software Quality Analyst | 10+ years of experience
Expertise in **Python, Playwright, Appium, Selenium, webdriverio, Javascript, UFT, Vbscript, CI/CD Pipelines**
📍 Bengaluru, India

## 📜 License
Licensed under the **MIT License** – free to use, modify, and distribute.
