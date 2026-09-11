# Agent Diary - LOXS Performance & Bug Fixes

## 2024-09-11 - LOXS Scanner Bottlenecks and Bug Classes
**Learning:** In interactive multi-scanner tools, using `sys.exit()` in subroutines prevents returning to main menu. Inner loops iterating over all input URLs per payload result cause O(N² M) quadratic bottlenecks. Modifying shared dictionaries/integers across worker threads in `ThreadPoolExecutor` causes data races and lost updates in Python.
**Action:** Replace `sys.exit()` in scanner functions with clean returns. Replace O(N) URL string stripping loops with O(1) direct string replace/slice. Guard shared state updates with `threading.Lock`. Guard divisions by `total_scanned` to prevent `ZeroDivisionError`.
