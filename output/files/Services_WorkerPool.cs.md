# File: `Services/WorkerPool.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `WorkerPool`

A pool of worker threads that process tasks in a queue. Tasks are added via EnqueueTask and workers will execute them concurrently.

**Purpose:** Provides a way to efficiently manage and execute multiple asynchronous tasks using a pool of reusable worker threads.

### Methods

  ### `EnqueueTask`

  Adds a new task to be processed by the worker pool.

  **Parameters:**
  - `task`: A function that returns a Task representing the work to be done

  ### `Stop`

  Cancels all tasks in the worker pool and stops accepting new ones.

  ### `WorkerPool`

  Initializes a worker pool with specified number of workers.

  **Parameters:**
  - `workerCount`: Number of worker threads to create

### Fields

  ### `_cts`

  Cancellation token source used to signal worker tasks to stop

  ### `_taskQueue`

  A blocking collection used to queue tasks for worker threads

