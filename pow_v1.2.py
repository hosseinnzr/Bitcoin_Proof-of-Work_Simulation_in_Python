import hashlib
import json
import time
import matplotlib.pyplot as plt

class Block:
    def __init__(self, index, prev_hash, data, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = 0

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        encoded = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        start_time = time.time()
        while True:
            hash_value = self.calculate_hash()
            if hash_value.startswith(target):
                return time.time() - start_time
            self.nonce += 1


class Blockchain:
    def __init__(self, initial_difficulty):
        self.chain = []
        self.difficulty = initial_difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", "Genesis Block")
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, difficulty):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), prev_block.calculate_hash(), data)
        mining_duration = new_block.mine(difficulty)
        self.chain.append(new_block)
        return mining_duration


# Create a single blockchain
difficulty_levels = [1, 2, 3, 4, 5]
mining_times = []

# Initialize blockchain with initial difficulty (e.g., 2)
blockchain = Blockchain(initial_difficulty=difficulty_levels[0])

for i, difficulty in enumerate(difficulty_levels):
    # Mine a new block with the corresponding difficulty
    elapsed = blockchain.add_block(data=f"Block {i + 1} Data", difficulty=difficulty)
    mining_times.append(elapsed)
    print(f"Block {i + 1} (Difficulty {difficulty}): {elapsed:.4f} seconds")

# Visualize the results
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(mining_times) + 1), mining_times, marker="o", color="green", linestyle="--")
plt.xlabel("Block Number")
plt.ylabel("Mining Time (seconds)")
plt.title("Mining Time per Block with Increasing Difficulty")
plt.grid(alpha=0.4)
plt.show()
