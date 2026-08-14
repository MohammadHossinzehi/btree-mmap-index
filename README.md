# B-Tree Memory-Mapped Index

A production-grade thread-safe B-tree index with memory-mapped storage for fast, persistent key-value operations. Designed for scenarios where you need O(log N) search and insertion on datasets larger than RAM.

## Features

- **B-Tree Data Structure**: Maintains O(log N) operations on large datasets
- - **Memory-Mapped Storage**: File-backed index for data persistence
  - - **Thread-Safe**: RW locks prevent corruption during concurrent access
    - - **Serialization**: Nodes packed as fixed-size records for O(1) random access
     
      - ## Installation
     
      - ```bash
        git clone https://github.com/MohammadHossinzehi/btree-mmap-index
        cd btree-mmap-index
        python -m pip install -e .
        ```

        ## Usage

        ```python
        from btree_mmap import MmapBTree

        db = MmapBTree('my_db.dat', t_order=3)

        db.insert(42)
        db.insert(25)
        db.insert(117)

        if db.search(42):
            print("Found key 42!")

        if not db.search(999):
            print("Key 999 does not exist")
        ```

        ## Architecture

        - **Node Serialization**: Each B-tree node is packed into a fixed-size binary record in the file, identified by node ID for O(1) direct access
        - - **Lock Strategy**: Reader-writer locks ensure consistent reads and exclusive writes during multithreaded access
          - - **Offset Tracking**: File offsets for each node allow caching and fast random access
           
            - ## Design Decisions
           
            - - **Fixed-Size Serialization**: Enables O(1) random access without scanning entire file
              - - **RW Locks over Global**: Lower overhead while preventing concurrent corruption
                - - **No Rebalancing Yet**: Current implementation handles sequential/random inserts; future work adds split/merge for optimal tree height
                 
                  - ## Testing
                 
                  - Run the test suite:
                 
                  - ```bash
                    python -m unittest test_btree.py -v
                    ```

                    Tests cover:
                    - `test_search_empty`: Confirms empty tree returns False for all keys
                    - - `test_insert_and_search`: Verifies basic insert/search correctness
                      - - `test_insert_multiple`: Larger keysets are correctly indexed
                        - - `test_thread_safety`: Concurrent reads and writes maintain consistency
                         
                          - ## Performance
                         
                          - - N random inserts: O(N log N)
                            - - R random searches: O(R log N)
                              - - File I/O: O(k) where k = node size with optional caching
                                - - Memory overhead: Fixed per node, minimal resident set for large datasets
