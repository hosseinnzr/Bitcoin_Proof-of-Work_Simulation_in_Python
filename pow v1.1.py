import hashlib
import json
import time
import random
import statistics
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display


# -----------------------------
# Persian text helper
# -----------------------------
def fa(text):
    return get_display(arabic_reshaper.reshape(text))


# -----------------------------
# Block
# -----------------------------
class Block:
    def __init__(self, index, prev_hash, data, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = None

    def calculate_hash(self):
        content = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        start = time.time()
        hashes = 0

        while True:
            self.hash = self.calculate_hash()
            hashes += 1
            if self.hash.startswith(target):
                return {
                    "time": time.time() - start,
                    "hashes": hashes
                }
            self.nonce += 1


# -----------------------------
# Blockchain
# -----------------------------
class Blockchain:
    def __init__(self, difficulty=3, target_block_time=2):
        self.chain = []
        self.difficulty = difficulty
        self.target_block_time = target_block_time
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0" * 64, "Genesis Block")
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    def add_block(self, data):
        prev = self.chain[-1]
        block = Block(
            index=len(self.chain),
            prev_hash=prev.hash,
            data=data
        )
        stats = block.mine(self.difficulty)
        self.chain.append(block)
        self.adjust_difficulty(stats["time"])
        return stats

    def adjust_difficulty(self, actual_time):
        if actual_time < self.target_block_time * 0.8:
            self.difficulty += 1
        elif actual_time > self.target_block_time * 1.2:
            self.difficulty = max(1, self.difficulty - 1) #****


# -----------------------------
# Multi‑Miner Simulation
# -----------------------------
def multi_miner_pow(difficulty, miners=4):
    nonces = [0] * miners
    target = "0" * difficulty
    start = time.time()

    while True:
        for i in range(miners):
            data = json.dumps({"nonce": nonces[i]}, sort_keys=True)
            h = hashlib.sha256(data.encode()).hexdigest()
            if h.startswith(target):
                return {
                    "winner": i,
                    "time": time.time() - start
                }
            nonces[i] += random.randint(1, 3)


# -----------------------------
# Statistical Mining Test
# -----------------------------
def average_mining_time(difficulty, runs=5):
    times = []
    hashes = []

    for _ in range(runs):
        block = Block(0, "0", "test")
        stats = block.mine(difficulty)
        times.append(stats["time"])
        hashes.append(stats["hashes"])

    return {
        "mean_time": statistics.mean(times),
        "std_time": statistics.stdev(times),
        "mean_hashes": statistics.mean(hashes)
    }


# -----------------------------
# Experiment
# -----------------------------
difficulties = [2, 3, 4, 5]
mean_times = []
std_times = []

print("=== Statistical Proof of Work Test ===")
for d in difficulties:
    result = average_mining_time(d, runs=5)
    mean_times.append(result["mean_time"])
    std_times.append(result["std_time"])
    print(f"Difficulty {d} | Mean: {result['mean_time']:.3f}s | Std: {result['std_time']:.3f}s")


# -----------------------------
# Plot 1: Difficulty vs Time
# -----------------------------
plt.figure(figsize=(9, 5))
plt.errorbar(
    difficulties,
    mean_times,
    yerr=std_times,
    marker="o",
    capsize=5
)
plt.xlabel(fa("درجه سختی"))
plt.ylabel(fa("میانگین زمان استخراج (ثانیه)"))
plt.title(fa("رابطه درجه سختی و زمان استخراج (Proof of Work)"))
plt.grid(True)
plt.show()


# -----------------------------
# Plot 2: Logarithmic Growth
# -----------------------------
import numpy as np

plt.figure(figsize=(9, 5))
plt.plot(difficulties, np.log(mean_times), marker="o")
plt.xlabel(fa("درجه سختی"))
plt.ylabel(fa("لگاریتم زمان استخراج"))
plt.title(fa("رشد نمایی زمان استخراج در PoW"))
plt.grid(True)
plt.show()


# -----------------------------
# Multi‑Miner Demo
# -----------------------------
print("\n=== Multi‑Miner Competition ===")
result = multi_miner_pow(difficulty=4, miners=5)
print(f"Winner Miner: #{result['winner']} | Time: {result['time']:.3f}s")
