
🚗 Smart Parking Lot Management System

A highly optimized, full-stack desktop application built with Streamlit that simulates and manages real-time parking lot operations. Instead of relying on standard database queries, this system is built entirely from the ground up using core Data Structures and Algorithms (DSA) to handle vehicle processing, searching, and queuing efficiently.

🛠️ Data Structures & Algorithms Implemented

• Fixed Array: Tracks the current state of active physical parking slots for O(1) status checks.
• Queue (FIFO): Manages a waiting list for incoming vehicles when the parking lot is completely full, ensuring fair, first-come, first-served processing.
• Stack (LIFO): Powers an Undo Operation History, allowing operators to reverse recent parking actions sequentially.
• Binary Search Tree (BST): Optimizes vehicle searching and record lookups by license plate, reducing search complexity to O(log n). Supports Inorder, Preorder, and Postorder tree traversals for comprehensive reporting.
• Max Heap: Implements a priority parking framework, allowing emergency or VIP vehicles to leapfrog the standard waiting queue based on priority scores.
• Custom Sorting Engines: Features hand-coded implementations of Bubble Sort, Selection Sort, Insertion Sort, and Heap Sort to sort and filter parking transaction history without external library dependencies.

🚀 Key Features

• Real-time Slot Allocation: Automatically updates available spaces and shifts vehicles smoothly from the waiting queue to open slots.
• Priority Overrides: Seamlessly handles emergency vehicles using a binary max-heap system.
• Interactive UI: A modern, clean dashboard built entirely using Python and Streamlit.
• Transactional Safety: Includes a multi-step undo functionality driven by internal memory stacks.
