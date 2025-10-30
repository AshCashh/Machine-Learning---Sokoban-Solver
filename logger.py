import multiprocessing
import time
import os
import pandas as pd
from sokoban import Warehouse
from mySokobanSolver import solve_weighted_sokoban 

WAREHOUSE_DIR = 'warehouses'
TIMEOUT = 600  # seconds

def run_solver(queue, warehouse):
    try:
        result = solve_weighted_sokoban(warehouse)
        queue.put(('Success', result))
    except Exception as e:
        queue.put(('Error', str(e)))

def run_with_timeout(warehouse, timeout=TIMEOUT):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=run_solver, args=(queue, warehouse))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return 'Timeout', None

    if not queue.empty():
        status, result = queue.get()
        if status == 'Success':
            return 'Solved' if result[0] != 'Impossible' else 'Impossible', result
        else:
            return 'Error', result
    return 'Error', 'No result returned'

def generate_report():
    records = []

    for file in sorted(os.listdir(WAREHOUSE_DIR)):
        if not file.endswith('.txt'):
            continue

        filepath = os.path.join(WAREHOUSE_DIR, file)
        warehouse = Warehouse()
        try:
            warehouse.load_warehouse(filepath)
        except Exception as e:
            print(f"    Skipping {file}: {e}")
            records.append({
                'Warehouse File': file,
                'Status': 'Invalid',
                'Time': '',
                'Cost': '',
                'Solution': str(e)
            })
            continue

        print(f"Solving: {file}")
        start_time = time.time()
        status, result = run_with_timeout(warehouse)
        elapsed = time.time() - start_time

        if status == 'Solved':
            solution, cost = result
            print(" Solved in:", elapsed)
        elif status == 'Impossible':
            solution, cost = 'Impossible', None
            print(" Impossible")
        else:
            solution, cost = status, None
            elapsed = '>600 seconds'
            print(" Time Elapsed")

        records.append({
            'Warehouse File': file,
            'Status': status,
            'Time': elapsed if isinstance(elapsed, str) else round(elapsed, 3),
            'Cost': cost if cost is not None else '',
            'Solution': str(solution)
        })

    df = pd.DataFrame(records)
    df.to_excel('sokoban_report.xlsx', index=False)
    print("Report saved as sokoban_report.xlsx")

if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")  # required for macOS
    generate_report()