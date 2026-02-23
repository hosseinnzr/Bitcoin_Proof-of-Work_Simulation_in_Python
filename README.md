# ⛏️ Simple PoW Blockchain Implementation with Difficulty Visualization

This repository contains a minimal, yet functional, implementation of a **Proof-of-Work (PoW) Blockchain** written in Python. The primary objective of this code is to simulate the core mechanics of a cryptocurrency ledger, specifically demonstrating how the **mining difficulty** directly impacts the **time required to mine a new block**.

The project utilizes the `hashlib` for secure hashing and `matplotlib` for visualizing the relationship between block difficulty and mining duration.

## ✨ Features

-   **`Block` Class**: Encapsulates block data, including index, previous hash, transaction data, timestamp, and the **nonce** required for mining.
-   **SHA-256 Hashing**: Secure cryptographic hashing for block integrity.
-   **Proof-of-Work (PoW) Simulation**: Implements the mining process where the block's hash must meet a certain difficulty target (starting with a number of leading zeros).
-   **`Blockchain` Class**: Manages the chain structure, including the creation of a **Genesis Block** and the logic for adding new, valid blocks.
-   **Difficulty Scaling Test**: Dynamically tests and measures the time taken to mine consecutive blocks while progressively increasing the mining difficulty (`difficulty = 1` to `5`).
-   **Visualization**: Generates a plot showing the exponential increase in mining time as the difficulty level rises.

## 📋 Prerequisites

You need Python 3.x installed on your system. The following external libraries are required:

-   `matplotlib`

## 💾 Installation

Follow these steps to set up the environment and run the simulation:

### 1. Clone the Repository (Optional for a single file)
If this code is in a file named `blockchain_simulator.py`:
```bash
git clone <repository-url>
cd <repository-name>
