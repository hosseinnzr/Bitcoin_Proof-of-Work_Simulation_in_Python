import hashlib
import json
import time
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    return get_display(arabic_reshaper.reshape(text))

class Block:
    def __init__(self):
        self.nonce = 0

    def calculate_hash(self):
        data = json.dumps({"nonce": self.nonce}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        start = time.time()
        while True:
            h = self.calculate_hash()
            # print(f"{h}")
            if h.startswith(target):
                return time.time() - start
            self.nonce += 1


difficulties = [2, 3, 4, 5, 6, 7]
times = []

for d in difficulties:
    block = Block()
    t = block.mine(d)
    times.append(t)
    print(f"Difficulty {d}: {t:.4f} seconds")

plt.figure(figsize=(8, 5))
plt.plot(difficulties, times, marker="o")
plt.xlabel(fa("درجه سختی (Difficulty)"))
plt.ylabel(fa("زمان استخراج (ثانیه)"))
plt.title(fa("رابطه سختی و زمان استخراج در Proof of Work"))
plt.grid(True)
plt.show()
