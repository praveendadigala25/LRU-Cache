import streamlit as st
from collections import OrderedDict

# LRU Cache class definition
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def display(self):
        # Return items from MRU to LRU
        return list(self.cache.items())[::-1]


# Page settings
st.set_page_config(
    page_title="LRU Cache App",
    layout="centered"
)

st.title("📦 LRU Cache Visual Simulator")

# Informational Section
with st.expander("ℹ️ What is LRU Cache?"):
    st.markdown("""
    LRU (**Least Recently Used**) Cache stores a **fixed number** of items.
    When full, it removes the **least recently used** item to make space for new data.

    This ensures **efficient memory usage and faster access**.
    """)

with st.expander("⚙️ How It Works"):
    st.markdown("""
    - 🔹 **Set the cache size** before using it.
    - 🔹 Use **Put** to store key-value pairs.
    - 🔹 Use **Get** to retrieve values (moves item to front).
    - 🔹 If full, the **Least Recently Used** item is removed.
    """)

with st.expander("🌐 Where is LRU Cache Used?"):
    st.markdown("""
    ✅ **Operating Systems** – Manages memory pages.

    ✅ **Web Browsers** – Stores frequently visited sites.

    ✅ **Databases** – Optimizes query caching.

    ✅ **Networking** – Used in Content Delivery Networks (CDNs).
    """)

# Cache Initialization
if "cache_initialized" not in st.session_state:
    st.session_state.cache_initialized = False

if not st.session_state.cache_initialized:
    with st.form("init_cache"):
        capacity = st.number_input(
            "🔧 Enter Cache Capacity",
            min_value=1,
            step=1,
            format="%d"
        )

        if st.form_submit_button("Initialize"):
            st.session_state.cache = LRUCache(capacity)
            st.session_state.capacity = capacity
            st.session_state.cache_initialized = True

# Main UI
if st.session_state.cache_initialized:

    st.success(
        f"✅ Cache Initialized with capacity = {st.session_state.capacity}"
    )

    col1, col2 = st.columns(2)

    # PUT Operation
    with col1:
        st.subheader("➕ Insert / Update")

        with st.form("put_form"):
            put_key = st.number_input(
                "Key",
                step=1,
                format="%d",
                key="put_key"
            )

            put_value = st.number_input(
                "Value",
                step=1,
                format="%d",
                key="put_value"
            )

            if st.form_submit_button("Put"):
                st.session_state.cache.put(put_key, put_value)
                st.success(f"Put ({put_key}, {put_value})")

    # GET Operation
    with col2:
        st.subheader("🔍 Retrieve")

        with st.form("get_form"):
            get_key = st.number_input(
                "Get Key",
                step=1,
                format="%d",
                key="get_key"
            )

            if st.form_submit_button("Get"):
                value = st.session_state.cache.get(get_key)

                if value == -1:
                    st.warning("❌ Key not found.")
                else:
                    st.success(f"Value = {value}")

    st.divider()

    # Cache Display
    st.subheader("📊 Cache State (MRU → LRU)")

    items = st.session_state.cache.display()

    if items:
        cols = st.columns(len(items))

        for idx, (k, v) in enumerate(items):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="
                        padding:15px;
                        background:#4CAF50;
                        color:white;
                        border-radius:10px;
                        text-align:center;
                    ">
                        <b>{k}</b><br>{v}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            "<center>⬅️ MRU | LRU ➡️</center>",
            unsafe_allow_html=True
        )

    else:
        st.info("Cache is empty.")

    # Reset Button
    if st.button("🔁 Reset"):
        for key in ["cache_initialized", "cache", "capacity"]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
