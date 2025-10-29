# File: `Services/WorkerPool.cs`

**Namespace:** `RepoScribe.Core.Services`

## Documentation Coverage

- **Coverage:** 100.0%
- **Total Elements:** 6
- **Documented:** 6

---

## Class: `WorkerPool`

A class that manages a pool of worker threads for executing tasks concurrently.

**Purpose:** Enables efficient processing of multiple tasks by distributing them among a configurable number of workers.

### Methods

  ### `EnqueueTask`

  Adds a new task to the worker pool's task queue for asynchronous processing.

  **Parameters:**
  - `task`: A function that returns a Task, representing the work to be done

  ### `Stop`

  Cancels the cancellation token source and completes adding tasks to the blocking collection, effectively stopping all worker threads.

  ### `WorkerPool`

  Initializes a new instance of WorkerPool with the specified number of workers.

  **Parameters:**
  - `workerCount`: The number of worker threads to create.

### Fields

  ### `_cts`

  A CancellationTokenSource used to signal the worker tasks to stop processing new items when the pool is shut down.

  ### `_taskQueue`

  A blocking collection used to queue tasks for worker threads to process.

