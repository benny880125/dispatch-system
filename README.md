# Dispatch System (MVP)

## Overview
This project is a simplified backend system that simulates a ride-hailing / delivery dispatch process.

The system assigns the nearest available driver to incoming orders and manages the lifecycle of each order.

---

## Features
- Driver management (add / status tracking)
- Order creation
- Nearest-driver dispatch algorithm
- Order lifecycle:
  - pending → assigned → completed

---

## System Design
The system is structured into three main components:

- `models.py`
  - Defines core data models (Driver, Order, Location)

- `services.py`
  - Contains business logic such as dispatch and order completion

- `main.py`
  - Simulates the workflow of the system

---

## Dispatch Logic
The current dispatch strategy is:

- Filter idle drivers
- Compute distance to pickup location
- Select the nearest driver

This is a greedy approach and serves as a baseline for future improvements.

---

## How to Run
```bash
python main.py