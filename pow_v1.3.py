import hashlib
import json
import time
import matplotlib.pyplot as plt

class Block:
    def __init__(self, index, prev_hash, data, difficulty, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.difficulty = difficulty

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "difficulty": self.difficulty
        }
        encoded = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def mine(self):
        target = "0" * self.difficulty
        start_time = time.time()
        while True:
            h = self.calculate_hash()
            if h.startswith(target):
                return time.time() - start_time
            self.nonce += 1


class Blockchain:
    def __init__(self, initial_difficulty=2):
        self.chain = []
        self.difficulty = initial_difficulty
        self.times = []
        self.difficulties = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", "Genesis Block", self.difficulty)
        t = genesis.mine()
        self.chain.append(genesis)
        self.times.append(t)
        self.difficulties.append(self.difficulty)
        print(f"Block #{genesis.index} | Difficulty: {genesis.difficulty} | Time: {t:.4f} seconds")

    def get_latest_block(self):
        return self.chain[-1]

    def adjust_difficulty(self):
        # Implement the requested logic: Adjust based on the trend of the last 3 times
        if len(self.times) >= 3:
            t_curr = self.times[-1]
            t_prev = self.times[-2]
            t_prev2 = self.times[-3]
            
            # 1. Strictly Increasing Trend: t_curr > t_prev > t_prev2
            if t_curr > t_prev and t_prev > t_prev2:
                print("--- Difficulty Adjustment: Trend Increasing -> DECREASING Difficulty ---")
                if self.difficulty > 1:
                    self.difficulty -= 1
            
            # 2. Strictly Decreasing Trend: t_curr < t_prev < t_prev2
            elif t_curr < t_prev and t_prev < t_prev2:
                print("--- Difficulty Adjustment: Trend Decreasing -> INCREASING Difficulty ---")
                if self.difficulty < 7:
                    self.difficulty += 1
            
            # 3. Otherwise (Stagnant or Fluctuating), keep difficulty as is.
            else:
                print(f"--- Difficulty Adjustment: Trend Stable/Fluctuating. Difficulty remains {self.difficulty} ---")
                
    def add_block(self, data):
        prev_block = self.get_latest_block()
        # Use the difficulty *before* adjustment for the new block mining
        current_difficulty_for_mining = self.difficulty 
        
        new_block = Block(len(self.chain), prev_block.calculate_hash(), data, current_difficulty_for_mining)
        t = new_block.mine()
        
        self.chain.append(new_block)
        self.times.append(t)
        self.difficulties.append(current_difficulty_for_mining)
        
        # Print required log immediately after mining
        print(f"Block #{new_block.index} | Difficulty: {new_block.difficulty} | Time: {t:.4f} seconds")
        
        # Adjust difficulty for the *next* block
        self.adjust_difficulty()


# Simulation for 20 blocks
blockchain = Blockchain(initial_difficulty=3) # Start higher to see effect faster
num_blocks = 20

print("\n--- Starting Adaptive PoW Simulation ---\n")
for i in range(1, num_blocks):
    blockchain.add_block(f"Block #{i} Data")
print("\n--- Simulation Complete ---\n")

# Visualization
plt.figure(figsize=(10, 6))
x_labels = [f"{i} (D={d})" for i, d in enumerate(blockchain.difficulties)]
plt.plot(range(len(blockchain.times)), blockchain.times, marker="o", color="red", linestyle='--')
plt.xticks(range(len(blockchain.times)), x_labels, rotation=45)
plt.xlabel("Block Number (with difficulty applied to that block)")
plt.ylabel("Mining Time (seconds)")
plt.title("Trend-Based Adaptive Difficulty Simulation")
plt.grid(alpha=0.5)
plt.tight_layout()
plt.show()
