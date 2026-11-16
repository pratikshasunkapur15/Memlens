import tracemalloc


def start_tracking():
    tracemalloc.start()
    print("MemLens: Memory tracking started!")


def get_memory_usage():
    current, peak = tracemalloc.get_traced_memory()

    return {
        "Current Memory (MB)": round(current / (1024 * 1024), 4),
        "Peak Memory (MB)": round(peak / (1024 * 1024), 4)
    }


def get_top_allocations():
    snapshot = tracemalloc.take_snapshot()

    top_stats = snapshot.statistics("lineno")

    results = []

    for stat in top_stats[:10]:
        results.append({
            "Location": str(stat.traceback),
            "Memory (MB)": round(stat.size / (1024 * 1024), 4),
            "Count": stat.count
        })

    return results


def stop_tracking():
    if tracemalloc.is_tracing():
        tracemalloc.stop()
        print("MemLens: Memory tracking stopped!")


if __name__ == "__main__":
    start_tracking()

    sample_data = [[0] * 500000 for _ in range(5)]

    print("\n========== Memory Usage ==========")

    memory = get_memory_usage()

    for key, value in memory.items():
        print(f"{key}: {value}")

    print("\n========== Top Memory Allocations ==========")

    for item in get_top_allocations():
        print(item)

    stop_tracking()