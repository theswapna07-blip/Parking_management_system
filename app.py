import streamlit as st
from datetime import datetime
import re


# ============================================================
# PARKING LOT MANAGEMENT SYSTEM
# Data Structures used:
# 1. Array       -> parking slots
# 2. Queue       -> waiting vehicles (FIFO)
# 3. Stack       -> undo operation history (LIFO)
# 4. Sorting     -> sort parking records
# 5. BST         -> vehicle search
# 6. Traversals  -> inorder, preorder, postorder
# 7. Max Heap    -> priority parking
# ============================================================


# ============================================================
# QUEUE
# ============================================================

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, vehicle):
        self.items.append(vehicle)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def contains(self, vehicle):
        return vehicle in self.items

    def remove(self, vehicle):
        """Remove a specific waiting vehicle while preserving the others' order."""
        if vehicle in self.items:
            self.items.remove(vehicle)
            return True
        return False

    def get_all(self):
        return self.items.copy()


# ============================================================
# STACK
# ============================================================

class Stack:
    def __init__(self):
        self.items = []

    def push(self, state):
        self.items.append(state)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# ============================================================
# BINARY SEARCH TREE
# ============================================================

class BSTNode:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, vehicle):
        self.root = self._insert(self.root, vehicle)

    def _insert(self, node, vehicle):
        if node is None:
            return BSTNode(vehicle)

        if vehicle < node.vehicle:
            node.left = self._insert(node.left, vehicle)

        elif vehicle > node.vehicle:
            node.right = self._insert(node.right, vehicle)

        return node

    def search(self, vehicle):
        return self._search(self.root, vehicle)

    def _search(self, node, vehicle):
        if node is None:
            return False

        if vehicle == node.vehicle:
            return True

        if vehicle < node.vehicle:
            return self._search(node.left, vehicle)

        return self._search(node.right, vehicle)

    def delete(self, vehicle):
        self.root = self._delete(self.root, vehicle)

    def _delete(self, node, vehicle):
        if node is None:
            return None

        if vehicle < node.vehicle:
            node.left = self._delete(node.left, vehicle)

        elif vehicle > node.vehicle:
            node.right = self._delete(node.right, vehicle)

        else:
            # Case 1: no child
            if node.left is None and node.right is None:
                return None

            # Case 2: only right child
            if node.left is None:
                return node.right

            # Case 3: only left child
            if node.right is None:
                return node.left

            # Case 4: two children
            successor = self._minimum(node.right)
            node.vehicle = successor.vehicle
            node.right = self._delete(
                node.right, successor.vehicle
            )

        return node

    def _minimum(self, node):
        current = node

        while current.left is not None:
            current = current.left

        return current

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.vehicle)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is not None:
            result.append(node.vehicle)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.vehicle)


# ============================================================
# MAX HEAP
# ============================================================

class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.heap[parent][0] >= self.heap[index][0]:
                break

            self.heap[parent], self.heap[index] = (
                self.heap[index],
                self.heap[parent]
            )

            index = parent

    def extract_max(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        maximum = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return maximum

    def _heapify_down(self, index):
        size = len(self.heap)

        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if (
                left < size
                and self.heap[left][0] > self.heap[largest][0]
            ):
                largest = left

            if (
                right < size
                and self.heap[right][0] > self.heap[largest][0]
            ):
                largest = right

            if largest == index:
                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index]
            )

            index = largest

    def get_all(self):
        return self.heap.copy()


# ============================================================
# SORTING ALGORITHMS
# ============================================================

def bubble_sort(records, key_function):
    arr = records.copy()
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if key_function(arr[j]) > key_function(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def selection_sort(records, key_function):
    arr = records.copy()
    n = len(arr)

    for i in range(n):
        minimum = i

        for j in range(i + 1, n):
            if key_function(arr[j]) < key_function(arr[minimum]):
                minimum = j

        arr[i], arr[minimum] = arr[minimum], arr[i]

    return arr


def insertion_sort(records, key_function):
    arr = records.copy()

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1

        while (
            j >= 0
            and key_function(arr[j]) > key_function(current)
        ):
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = current

    return arr


def heap_sort_numbers(numbers):
    heap = MaxHeap()

    for number in numbers:
        heap.insert((number, number))

    result = []

    while heap.heap:
        item = heap.extract_max()
        result.append(item[1])

    result.reverse()
    return result


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def is_valid_license_plate(plate):
    """Check common Indian vehicle registration formats (format only)."""
    return bool(re.fullmatch(r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{1,4}", plate))


def create_bst_from_parking():
    tree = BST()

    for vehicle in st.session_state.parking_slots:
        if vehicle is not None:
            tree.insert(vehicle)

    return tree


def create_snapshot():
    return {
        "parking_slots": st.session_state.parking_slots.copy(),
        "waiting_queue": st.session_state.waiting_queue.get_all(),
        "priority_heap": st.session_state.priority_heap.get_all(),
        "records": [record.copy() for record in st.session_state.records]
    }


def restore_snapshot(snapshot):
    st.session_state.parking_slots = snapshot["parking_slots"].copy()

    new_queue = Queue()
    for vehicle in snapshot["waiting_queue"]:
        new_queue.enqueue(vehicle)
    st.session_state.waiting_queue = new_queue

    new_heap = MaxHeap()
    for item in snapshot.get("priority_heap", []):
        new_heap.insert(tuple(item))
    st.session_state.priority_heap = new_heap

    st.session_state.records = [
        record.copy() for record in snapshot["records"]
    ]


def save_state_before_change():
    st.session_state.undo_stack.push(create_snapshot())


def add_record(vehicle, slot):
    st.session_state.records.append({
        "vehicle": vehicle,
        "slot": slot,
        "time": datetime.now().strftime("%H:%M:%S")
    })


def remove_record(vehicle):
    st.session_state.records = [
        record
        for record in st.session_state.records
        if record["vehicle"] != vehicle
    ]


# ============================================================
# SESSION STATE
# ============================================================

if "parking_slots" not in st.session_state:
    st.session_state.parking_slots = [None] * 10

if "waiting_queue" not in st.session_state:
    st.session_state.waiting_queue = Queue()

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = Stack()

if "records" not in st.session_state:
    st.session_state.records = []

if "priority_heap" not in st.session_state:
    st.session_state.priority_heap = MaxHeap()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Parking Lot Management System",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# VARIABLES
# ============================================================

parking_slots = st.session_state.parking_slots
waiting_queue = st.session_state.waiting_queue
undo_stack = st.session_state.undo_stack
records = st.session_state.records


# ============================================================
# TITLE
# ============================================================

st.title("🚗 Parking Lot Management System")

st.write(
    "A menu-driven parking application demonstrating "
    "Array, Stack, Sorting, BST, Tree Traversal and a Max Heap for priority-based waiting."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📋 MENU")

choice = st.sidebar.radio(
    "Select an operation:",
    [
        "🏠 Dashboard",
        "🚗 Park Vehicle",
        "🚪 Remove Vehicle",
        "🔍 Search Vehicle",
        "🅿️ Display Parking Slots",
        "⏳ Waiting Queue",
        "↩️ Undo Last Operation",
        "🔃 Sorting",
        "🌳 BST & Tree Traversals",
        "🏆 Priority Parking / Heap"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if choice == "🏠 Dashboard":

    st.header("🏠 Parking Dashboard")

    total = len(parking_slots)
    occupied = sum(
        1 for slot in parking_slots
        if slot is not None
    )
    available = total - occupied

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Slots", total)

    with col2:
        st.metric("Occupied", occupied)

    with col3:
        st.metric("Available", available)

    with col4:
        st.metric(
            "Waiting",
            len(st.session_state.priority_heap.get_all())
        )

    st.divider()

    st.subheader("🅿️ Current Parking Status")

    for i, vehicle in enumerate(parking_slots):

        if vehicle is None:
            st.success(
                f"🟩 Slot {i + 1} — EMPTY"
            )
        else:
            st.error(
                f"🟥 Slot {i + 1} — {vehicle}"
            )


# ============================================================
# PARK VEHICLE
# ============================================================

elif choice == "🚗 Park Vehicle":

    st.header("🚗 Park Vehicle")
    st.caption("Only license plates matching a common Indian registration format are accepted, for example KL07AB1234.")

    car_number = st.text_input(
        "License Plate Number",
        placeholder="Example: KL07AB1234",
        key="park_license_plate"
    )
    priority_value = st.number_input(
        "Waiting priority (1 = lowest, 100 = highest)",
        min_value=1, max_value=100, value=50, step=1,
        help="Used only if all parking slots are full."
    )

    if st.button("🚗 Park Vehicle / Join Waiting List", type="primary", use_container_width=True):
        car_number = car_number.strip().upper()

        if not is_valid_license_plate(car_number):
            st.error("Invalid license plate format. Example: KL07AB1234 (state code + RTO number + series + number).")
        elif car_number in parking_slots:
            st.error("This vehicle is already parked.")
        elif any(vehicle == car_number for _, vehicle in st.session_state.priority_heap.get_all()):
            st.error("This vehicle is already on the waiting list.")
        else:
            available_slot = next((i for i, slot in enumerate(parking_slots) if slot is None), -1)
            save_state_before_change()

            if available_slot != -1:
                parking_slots[available_slot] = car_number
                add_record(car_number, available_slot + 1)
                st.success(f"{car_number} parked successfully in Slot {available_slot + 1}.")
            else:
                st.session_state.priority_heap.insert((int(priority_value), car_number))
                waiting_queue.enqueue(car_number)  # Keep arrival order as a Queue as well.
                st.success(f"Parking lot is full. {car_number} added to the priority waiting list with priority {int(priority_value)}.")
                st.info("The vehicle with the highest priority will get the next available slot.")
elif choice == "🚪 Remove Vehicle":

    st.header("🚪 Remove Vehicle")
    car_number = st.text_input(
        "License Plate Number",
        placeholder="Example: KL07AB1234",
        key="remove_license_plate"
    )

    if st.button("🚪 Remove Vehicle", type="primary"):
        car_number = car_number.strip().upper()

        if not is_valid_license_plate(car_number):
            st.error("Invalid license plate format. Example: KL07AB1234.")
        else:
            found_slot = next((i for i, vehicle in enumerate(parking_slots) if vehicle == car_number), -1)
            if found_slot == -1:
                st.error(f"{car_number} is not currently parked.")
            else:
                save_state_before_change()
                parking_slots[found_slot] = None
                remove_record(car_number)
                st.success(f"{car_number} removed from Slot {found_slot + 1}.")

                # The Max Heap chooses the highest-priority waiting vehicle.
                next_item = st.session_state.priority_heap.extract_max()
                if next_item is not None:
                    priority, next_vehicle = next_item
                    waiting_queue.remove(next_vehicle)
                    parking_slots[found_slot] = next_vehicle
                    add_record(next_vehicle, found_slot + 1)
                    st.success(f"{next_vehicle} (priority {priority}) automatically moved into Slot {found_slot + 1}.")
                else:
                    st.info(f"Slot {found_slot + 1} is now available; no vehicles are waiting.")
elif choice == "🔍 Search Vehicle":

    st.header("🔍 Search Vehicle")

    car_number = st.text_input(
        "License Plate Number",
        placeholder="Example: KL07AB1234"
    )

    if st.button(
        "🔍 Search",
        type="primary"
    ):

        car_number = car_number.strip().upper()

        if car_number == "":
            st.warning("Please enter a vehicle number.")

        else:

            tree = create_bst_from_parking()

            if tree.search(car_number):

                for i, vehicle in enumerate(parking_slots):

                    if vehicle == car_number:

                        st.success("✅ Vehicle Found!")
                        st.info(
                            f"🚗 Vehicle: {car_number}"
                        )
                        st.info(
                            f"🅿️ Slot: {i + 1}"
                        )
                        break

            elif waiting_queue.contains(car_number):

                position = (
                    waiting_queue
                    .get_all()
                    .index(car_number)
                    + 1
                )

                st.warning(
                    f"⏳ {car_number} is waiting in "
                    "the queue."
                )

                st.info(
                    f"Queue Position: {position}"
                )

            else:

                st.error(
                    f"❌ {car_number} was not found."
                )


# ============================================================
# DISPLAY PARKING SLOTS
# ============================================================

elif choice == "🅿️ Display Parking Slots":

    st.header("🅿️ Parking Slots")

    for i, vehicle in enumerate(parking_slots):

        if vehicle is None:
            st.success(
                f"🟩 Slot {i + 1} — EMPTY"
            )
        else:
            st.error(
                f"🟥 Slot {i + 1} — {vehicle}"
            )


# ============================================================
# WAITING QUEUE
# ============================================================

elif choice == "⏳ Waiting Queue":

    st.header("⏳ Priority Waiting List")
    st.write("Vehicles are served by **Max Heap priority**: highest priority first, not arrival order.")

    waiting_items = sorted(st.session_state.priority_heap.get_all(), key=lambda item: item[0], reverse=True)
    if not waiting_items:
        st.success("No vehicles are waiting.")
    else:
        for position, (priority, vehicle) in enumerate(waiting_items, start=1):
            st.write(f"**{position}. {vehicle}** — Priority: {priority}")
        st.divider()
        st.write(f"Total waiting vehicles: **{len(waiting_items)}**")
elif choice == "↩️ Undo Last Operation":

    st.header("↩️ Undo Last Operation")

    st.write(
        "The Stack follows **LIFO "
        "(Last In, First Out)**."
    )

    st.write(
        f"Operations available to undo: "
        f"**{undo_stack.size()}**"
    )

    if st.button(
        "↩️ Undo",
        type="primary"
    ):

        previous_state = undo_stack.pop()

        if previous_state is None:

            st.warning(
                "There is no operation to undo."
            )

        else:

            restore_snapshot(previous_state)

            st.success(
                "✅ Last operation has been undone."
            )

    st.divider()

    st.subheader("How Stack is used")

    st.write(
        "Before every important modification, "
        "the previous parking state is pushed onto "
        "the Stack. Undo pops the most recent state."
    )


# ============================================================
# SORTING
# ============================================================

elif choice == "🔃 Sorting":

    st.header("🔃 Parking Record Sorting")

    if len(records) == 0:

        st.info(
            "No parking records available yet."
        )

    else:

        sort_option = st.selectbox(
            "Sort records by:",
            [
                "Vehicle Number",
                "Parking Slot",
                "Parking Time"
            ]
        )

        if sort_option == "Vehicle Number":
            key_function = lambda record: record["vehicle"]

        elif sort_option == "Parking Slot":
            key_function = lambda record: record["slot"]

        else:
            key_function = lambda record: record["time"]

        algorithm = st.selectbox(
            "Choose sorting algorithm:",
            [
                "Bubble Sort",
                "Selection Sort",
                "Insertion Sort"
            ]
        )

        if algorithm == "Bubble Sort":

            sorted_records = bubble_sort(
                records,
                key_function
            )

        elif algorithm == "Selection Sort":

            sorted_records = selection_sort(
                records,
                key_function
            )

        else:

            sorted_records = insertion_sort(
                records,
                key_function
            )

        st.subheader(
            f"Sorted using {algorithm}"
        )

        for record in sorted_records:

            st.write(
                f"🚗 **{record['vehicle']}**  |  "
                f"🅿️ Slot {record['slot']}  |  "
                f"🕐 {record['time']}"
            )


# ============================================================
# BST + TREE TRAVERSALS
# ============================================================

elif choice == "🌳 BST & Tree Traversals":

    st.header("🌳 Binary Search Tree")

    tree = create_bst_from_parking()

    st.write(
        "The BST stores currently parked vehicle "
        "numbers for efficient searching."
    )

    if tree.root is None:

        st.info(
            "No parked vehicles. Park some vehicles first."
        )

    else:

        st.subheader("Tree Traversals")

        inorder_result = tree.inorder()
        preorder_result = tree.preorder()
        postorder_result = tree.postorder()

        st.write(
            "**Inorder:**",
            " → ".join(inorder_result)
        )

        st.write(
            "**Preorder:**",
            " → ".join(preorder_result)
        )

        st.write(
            "**Postorder:**",
            " → ".join(postorder_result)
        )

        st.divider()

        st.subheader("BST Search")

        search_vehicle = st.text_input(
            "Vehicle number to search in BST",
            key="bst_search"
        )

        if st.button(
            "🔍 Search BST",
            key="bst_search_button"
        ):

            search_vehicle = (
                search_vehicle.strip().upper()
            )

            if tree.search(search_vehicle):

                st.success(
                    f"✅ {search_vehicle} exists in the BST."
                )

            else:

                st.error(
                    f"❌ {search_vehicle} does not exist "
                    "in the BST."
                )

        st.divider()

        st.subheader("BST Delete Demonstration")

        delete_vehicle = st.text_input(
            "Vehicle number to delete from BST",
            key="bst_delete"
        )

        if st.button(
            "🗑️ Delete from BST",
            key="bst_delete_button"
        ):

            delete_vehicle = (
                delete_vehicle.strip().upper()
            )

            if tree.search(delete_vehicle):

                tree.delete(delete_vehicle)

                st.success(
                    f"✅ {delete_vehicle} deleted "
                    "from the BST."
                )

                st.info(
                    "Note: this demonstration changes "
                    "the BST representation only; "
                    "it does not remove the actual car "
                    "from the parking lot."
                )

            else:

                st.error(
                    "Vehicle not found in BST."
                )


# ============================================================
# HEAP / PRIORITY PARKING
# ============================================================

elif choice == "🏆 Priority Parking / Heap":

    st.header("🏆 Max Heap — Live Priority Parking")
    st.write("This heap is connected to the actual parking system. When the lot is full, vehicles added from **Park Vehicle** are stored here. When a parked vehicle leaves, the highest-priority waiting vehicle gets the free slot automatically.")
    heap_items = sorted(st.session_state.priority_heap.get_all(), key=lambda item: item[0], reverse=True)
    if not heap_items:
        st.info("The priority waiting list is empty. Use Park Vehicle to add a vehicle; it will wait here if all slots are occupied.")
    else:
        for position, (priority, vehicle) in enumerate(heap_items, start=1):
            st.write(f"{position}. **{vehicle}** — Priority {priority}")
        st.caption("Priority range: 1 (lowest) to 100 (highest). The heap itself selects the maximum efficiently.")

    st.divider()
    st.subheader("Heap Sort Demonstration")
    numbers_text = st.text_input("Enter numbers separated by commas", key="heap_sort_numbers")
    if st.button("Run Heap Sort"):
        try:
            numbers = [int(value.strip()) for value in numbers_text.split(",") if value.strip()]
            if not numbers:
                st.warning("Enter at least one number.")
            else:
                st.success(f"Sorted numbers: {heap_sort_numbers(numbers)}")
        except ValueError:
            st.error("Please enter only integers separated by commas.")
