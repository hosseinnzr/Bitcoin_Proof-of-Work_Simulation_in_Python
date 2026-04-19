import hashlib
import json
import time
import matplotlib.pyplot as plt


# =====================================================
# Block Class
# =====================================================
class Block:
    def __init__(self, index, prev_hash, data, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = None
        self.mining_time = None 

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        encoded_data = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_data).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        start_time = time.time()

        while True:
            current_hash = self.calculate_hash()
            if current_hash.startswith(target):
                self.hash = current_hash
                self.mining_time = time.time() - start_time
                return self.mining_time

            self.nonce += 1


# =====================================================
# Blockchain Class
# =====================================================
class Blockchain:
    def __init__(self, initial_difficulty):
        self.chain = []
        self.initial_difficulty = initial_difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", "Genesis Block")
        genesis_block.mine(self.initial_difficulty)
        self.chain.append(genesis_block)

        print("\n✅ Genesis Block Mined")
        print(f"Hash        : {genesis_block.hash}")
        print(f"Mining Time : {genesis_block.mining_time:.4f} seconds")
        print("=" * 60)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, difficulty):
        previous_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            prev_hash=previous_block.hash,
            data=data
        )

        mining_time = new_block.mine(difficulty)
        self.chain.append(new_block)

        self.print_block_info(new_block, difficulty)

        return mining_time

    @staticmethod
    def print_block_info(block, difficulty):
        print(f"* Block {block.index} Mined")
        print(f"Difficulty  : {difficulty}")
        print(f"Nonce       : {block.nonce}")
        print(f"Hash        : {block.hash}")
        print(f"Prev Hash   : {block.prev_hash}")
        print(f"Mining Time : {block.mining_time:.4f} seconds")
        print("-" * 60)


# =====================================================
# Blockchain Simulation
# =====================================================
if __name__ == "__main__":

    difficulty_levels = [1, 2, 3, 4, 5]
    mining_times = []

    blockchain = Blockchain(initial_difficulty=difficulty_levels[0])

    for i, difficulty in enumerate(difficulty_levels, start=1):
        elapsed_time = blockchain.add_block(
            data=f"Block {i} Data",
            difficulty=difficulty
        )
        mining_times.append(elapsed_time)

    # =================================================
    # Visualization
    # =================================================
    plt.figure(figsize=(8, 5))
    plt.plot(
        range(1, len(mining_times) + 1),
        mining_times,
        marker="o",
        linestyle="--",
        color="green"
    )

    plt.xlabel("Block Number")
    plt.ylabel("Mining Time (seconds)")
    plt.title("Mining Time per Block with Increasing Difficulty")
    plt.grid(alpha=0.4)
    plt.tight_layout()
    plt.show()
