import streamlit as st
import psutil
import pandas as pd
import plotly.express as px
import time
import tracemalloc
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

if not tracemalloc.is_tracing():
    tracemalloc.start()

st.set_page_config(
    page_title="MemLens",
    page_icon="🧠",
    layout="wide"
)
st_autorefresh(
    interval=2000,
    key="memlens_refresh"
)
st.title("🧠 MemLens")
st.subheader("Memory Monitoring and Visualization Tool")

st.markdown("Monitor running processes and understand memory consumption.")

# System memory
memory = psutil.virtual_memory()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total RAM",
    f"{memory.total / (1024**3):.2f} GB"
)

col2.metric(
    "Used RAM",
    f"{memory.used / (1024**3):.2f} GB"
)

col3.metric(
    "RAM Usage",
    f"{memory.percent}%"
)

st.divider()

st.subheader("System Memory Usage")

memory_data = pd.DataFrame({
    "Category": ["Used", "Available"],
    "Memory (GB)": [
        memory.used / (1024**3),
        memory.available / (1024**3)
    ]
})

fig = px.pie(
    memory_data,
    names="Category",
    values="Memory (GB)",
    title="RAM Distribution",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Running Process Memory Usage")

processes = []

for process in psutil.process_iter(
    ["pid", "name", "memory_info"]
):
    try:
        info = process.info

        processes.append({
            "PID": info["pid"],
            "Process": info["name"],
            "Memory (MB)": round(
                info["memory_info"].rss / (1024 * 1024), 2
            )
        })

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

df = pd.DataFrame(processes)

df = df.sort_values(
    by="Memory (MB)",
    ascending=False
)

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.subheader("Top 10 Memory-Consuming Processes")

top_processes = df.head(10)

bar_chart = px.bar(
    top_processes,
    x="Process",
    y="Memory (MB)",
    title="Process Memory Consumption",
    color="Memory (MB)"
)

st.plotly_chart(bar_chart, use_container_width=True)

st.caption("MemLens | Real-time system memory monitoring")


# ==========================================
# MEMORY ALLOCATION TRACKING
# ==========================================

st.divider()

st.header("🧠 Python Memory Allocation Tracking")

# Get current and peak memory
current, peak = tracemalloc.get_traced_memory()

current_mb = current / (1024 * 1024)
peak_mb = peak / (1024 * 1024)

# Display memory metrics
col1, col2 = st.columns(2)

col1.metric(
    "Current Allocated Memory",
    f"{current_mb:.2f} MB"
)

col2.metric(
    "Peak Allocated Memory",
    f"{peak_mb:.2f} MB"
)

# Get allocation snapshot
snapshot = tracemalloc.take_snapshot()

top_stats = snapshot.statistics("lineno")

allocation_data = []

for stat in top_stats[:10]:
    allocation_data.append({
        "Location": str(stat.traceback),
        "Memory (MB)": round(
            stat.size / (1024 * 1024), 4
        ),
        "Count": stat.count
    })

st.subheader("📊 Top 10 Memory Allocations")

allocation_df = pd.DataFrame(allocation_data)

if not allocation_df.empty:

    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Memory Allocation Visualization")

    fig = px.bar(
        allocation_df,
        x="Memory (MB)",
        y="Location",
        orientation="h",
        title="Top Memory Allocations"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("Collecting memory allocation data...")


# ==========================================
# MEMORY GROWTH DETECTION
# ==========================================

st.divider()

st.header("🚨 Memory Growth Detection")

# Compare current snapshot with previous snapshot
previous_snapshot = st.session_state.get(
    "previous_snapshot"
)

if previous_snapshot is not None:

    growth_stats = snapshot.compare_to(
        previous_snapshot,
        "lineno"
    )

    positive_growth = [
        stat for stat in growth_stats
        if stat.size_diff > 0
    ]

    if positive_growth:

        growth_data = []

        for stat in positive_growth[:10]:

            growth_data.append({
                "Location": str(stat.traceback),
                "Memory Growth (MB)": round(
                    stat.size_diff / (1024 * 1024), 4
                ),
                "Count Change": stat.count_diff
            })

        growth_df = pd.DataFrame(growth_data)

        st.subheader("Potential Memory Growth")

        st.dataframe(
            growth_df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Positive memory growth detected since the previous snapshot. "
            "Repeated growth may indicate a possible memory leak."
        )

    else:

        st.success(
            "No positive memory growth detected since the previous snapshot."
        )

else:

    st.info(
        "Collecting the first memory snapshot. "
        "Growth comparison will appear on the next refresh."
    )

# Save current snapshot for next comparison
st.session_state["previous_snapshot"] = snapshot


# ==========================================
# MEMORY USAGE HISTORY
# ==========================================

st.divider()

st.header("📈 Memory Usage History")

# Initialize history
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []

# Collect current readings
history_entry = {
    "Time": datetime.now().strftime("%H:%M:%S"),
    "RAM Usage (%)": psutil.virtual_memory().percent,
    "CPU Usage (%)": psutil.cpu_percent(interval=None)
}

st.session_state.memory_history.append(history_entry)

# Keep only the latest 60 readings
st.session_state.memory_history = (
    st.session_state.memory_history[-60:]
)

history_df = pd.DataFrame(
    st.session_state.memory_history
)

# Display history graph
st.subheader("RAM Usage Over Time")

ram_chart = px.line(
    history_df,
    x="Time",
    y="RAM Usage (%)",
    markers=True,
    title="Historical RAM Usage"
)

st.plotly_chart(
    ram_chart,
    use_container_width=True
)

st.subheader("CPU Usage Over Time")

cpu_chart = px.line(
    history_df,
    x="Time",
    y="CPU Usage (%)",
    markers=True,
    title="Historical CPU Usage"
)

st.plotly_chart(
    cpu_chart,
    use_container_width=True
)


# ==========================================
# MEMORY USAGE ALERTS
# ==========================================

st.divider()

st.header("🚨 Memory Usage Alerts")

ram_usage = psutil.virtual_memory().percent

st.metric("Current RAM Usage", f"{ram_usage:.1f}%")

if ram_usage >= 85:
    st.error("CRITICAL: RAM usage is above 85%!")

elif ram_usage >= 70:
    st.warning("WARNING: RAM usage is high!")

else:
    st.success("NORMAL: RAM usage is under control.")

# Custom alert threshold
st.subheader("Set Your Alert Threshold")

threshold = st.slider(
    "RAM alert threshold (%)",
    min_value=50,
    max_value=100,
    value=80
)

if ram_usage >= threshold:
    st.error(
        f"Alert! RAM usage has crossed your "
        f"custom threshold of {threshold}%."
    )
else:
    st.info(
        f"RAM usage is below your custom "
        f"threshold of {threshold}%."
    )

# ==========================================
# EXPORT MEMLENS MONITORING REPORT
# ==========================================

st.divider()

st.header("📥 Export Monitoring Report")

# Collect current system information
report_data = {
    "Metric": [
        "Total RAM (GB)",
        "Used RAM (GB)",
        "Available RAM (GB)",
        "RAM Usage (%)",
        "CPU Usage (%)"
    ],
    "Value": [
        round(psutil.virtual_memory().total / (1024**3), 2),
        round(psutil.virtual_memory().used / (1024**3), 2),
        round(psutil.virtual_memory().available / (1024**3), 2),
        psutil.virtual_memory().percent,
        psutil.cpu_percent(interval=None)
    ]
}

report_df = pd.DataFrame(report_data)

# Convert report to CSV
csv_report = report_df.to_csv(index=False).encode("utf-8")

st.dataframe(report_df, use_container_width=True)

st.download_button(
    label="📥 Download MemLens Report",
    data=csv_report,
    file_name="MemLens_Monitoring_Report.csv",
    mime="text/csv",
    key="download_memlens_report"
)
# ==========================================
# MEMLENS SIDEBAR
# ==========================================

with st.sidebar:
    st.title("🧠 MemLens")
    st.caption("Memory Monitoring & Visualization Tool")

    st.divider()

    st.subheader("📊 Monitoring Modules")
    st.write("✅ System RAM Monitoring")
    st.write("✅ Process Monitoring")
    st.write("✅ Memory Allocation Tracking")
    st.write("✅ Memory Growth Detection")
    st.write("✅ RAM & CPU History")
    st.write("✅ Memory Usage Alerts")
    st.write("✅ CSV Report Export")

    st.divider()

    st.caption("Developed as an Operating Systems Mini Project.")

# ==========================================
# SYSTEM HEALTH OVERVIEW
# ==========================================

st.divider()

st.header("🖥️ System Health Overview")

# Collect system information
cpu_usage = psutil.cpu_percent(interval=0.2)
ram = psutil.virtual_memory()
process_count = len(psutil.pids())

# Determine health status
if cpu_usage >= 85 or ram.percent >= 85:
    health = "🔴 Critical"
elif cpu_usage >= 70 or ram.percent >= 70:
    health = "🟡 Warning"
else:
    health = "🟢 Healthy"

# Display system health
st.subheader(f"Overall System Status: {health}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("CPU Usage", f"{cpu_usage:.1f}%")
c2.metric("RAM Usage", f"{ram.percent:.1f}%")
c3.metric(
    "Available RAM",
    f"{ram.available / (1024**3):.2f} GB"
)
c4.metric("Running Processes", process_count)

st.caption(
    "System health is based on CPU and RAM usage thresholds."
)
# ==========================================
# PROCESS SEARCH
# ==========================================

st.divider()

st.header("🔎 Search Running Processes")

search_query = st.text_input(
    "Enter process name",
    placeholder="Example: chrome"
)

process_list = []

for process in psutil.process_iter(
    ['pid', 'name', 'memory_info']
):
    try:
        info = process.info

        process_list.append({
            "PID": info["pid"],
            "Process Name": info["name"],
            "Memory (MB)": round(
                info["memory_info"].rss / (1024 * 1024), 2
            )
        })

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

if search_query:
    filtered_processes = [
        process for process in process_list
        if search_query.lower() in
        (process["Process Name"] or "").lower()
    ]

    st.dataframe(
        filtered_processes,
        use_container_width=True
    )

    if not filtered_processes:
        st.info("No matching process found.")
else:
    st.info("Type an application name to search.")
