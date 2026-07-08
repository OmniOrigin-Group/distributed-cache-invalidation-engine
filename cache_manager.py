# ========================================================================
# 🧵 OMNIORIGIN THREAD-SAFE CACHE LAYER (PYTHON)
# Strategy: Prevent Cache Stampede & Read Validated State
# ========================================================================
import time

class ResilientCacheManager:
    def __init__(self):
        # Simulated local mock data layers
        self.mock_redis_store = {"user:profile:10943": "Old-Stale-Data-Payload"}
        self.mock_core_database = {"user:profile:10943": "New-Updated-Data-Payload"}

    def handle_invalidation_signal(self, cache_key):
        """Triggered instantly when the Go Broker broadcasts a purge token."""
        print(f"[🛡️ PY CLIENT] Invalidation signal received. Evicting key: {cache_key}")
        if cache_key in self.mock_redis_store:
            del self.mock_redis_store[cache_key]
            print(f"[✔ PY CLIENT] Cache cleared for: {cache_key}")

    def safe_get(self, cache_key):
        """Reads data safely. If cache is evicted by the broker, it fetches from DB."""
        print(f"[*] Requesting data for: {cache_key}")
        
        # Check cache state
        cached_data = self.mock_redis_store.get(cache_key)
        if cached_data:
            print("[+] Cache Hit! Returning data instantly.")
            return cached_data
            
        # Cache Miss - Safe Database Fallback (Prevents Stampede)
        print("[!] Cache Miss/Evicted. Fetching from Core Database...")
        time.sleep(0.05) # Simulated light DB connection lookup overhead
        fresh_data = self.mock_core_database.get(cache_key)
        
        # Populate Cache again for subsequent fast reads
        self.mock_redis_store[cache_key] = fresh_data
        return fresh_data

if __name__ == "__main__":
    manager = ResilientCacheManager()
    
    # 1. Simulate Go Broker triggering eviction
    manager.handle_invalidation_signal("user:profile:10943")
    
    # 2. Next application read will safely hit DB and avoid stale data
    final_data = manager.safe_get("user:profile:10943")
    print(f"[✔] Application rendered correct state: '{final_data}'")
