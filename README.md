
# MemLens 🔍

### Real-Time Memory Monitoring and Analysis Tool

MemLens is a Python-based system monitoring project designed to track memory usage, monitor running processes, and visualize system health through an interactive Streamlit dashboard.

## 🚀 Features

- Real-time RAM usage monitoring
- System Health Overview
- Running process monitoring
- Process memory usage tracking
- Memory allocation tracking using Python's tracemalloc
- Interactive Streamlit dashboard

## 🛠️ Technologies Used

- Python
- Streamlit
- Git and GitHub
- Python memory profiling tools

## 📁 Project Structure

```text
MemLens/
│
├── dashboard/
│   └── app.py
│
├── monitor/
│   ├── allocation_tracker.py
│   └── process_monitor.py
│
├── tests/
│   └── sample_workload.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/pratikshasunkapur15/Memlens.git
```

2. Navigate into the project:

```bash
cd Memlens
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the environment (Windows PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

```bash
streamlit run dashboard/app.py
```

## 🎯 Project Objective

The objective of MemLens is to provide an interactive way to observe system memory consumption, understand running processes, and explore memory allocation behaviour.

## 👩‍💻 Developer

**Pratiksha Sunkapur**

GitHub: [pratikshasunkapur15](https://github.com/pratikshasunkapur15)
