import psutil


def get_running_processes():
    processes = []

    for process in psutil.process_iter(
        ['pid', 'name', 'memory_info', 'cpu_percent']
    ):
        try:
            info = process.info

            memory_mb = info['memory_info'].rss / (1024 * 1024)

            processes.append({
                'PID': info['pid'],
                'Process Name': info['name'],
                'Memory (MB)': round(memory_mb, 2),
                'CPU (%)': info['cpu_percent']
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sorted(
        processes,
        key=lambda process: process['Memory (MB)'],
        reverse=True
    )


if __name__ == "__main__":
    running_processes = get_running_processes()

    print("\n========== MemLens Memory Monitor ==========\n")

    for process in running_processes[:15]:
        print(
            f"PID: {process['PID']} | "
            f"Name: {process['Process Name']} | "
            f"Memory: {process['Memory (MB)']} MB | "
            f"CPU: {process['CPU (%)']}%"
        )