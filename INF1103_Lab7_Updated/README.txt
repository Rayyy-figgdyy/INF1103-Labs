INF1103 Lab 7 - Updated Inventory Management System

Run from this folder:
    python inventory_manager.py

Docker bind-mount workflow (PowerShell, from this folder):
    docker run --rm -it -v "${PWD}:/app" -w /app inf1103-labs-smart-auditor python inventory_manager.py

IMPORTANT: If reusing a Lab 6 inventory.json, migrate each existing product:
  - physical: add "type": "physical" and "weight": <number in kg>
  - digital:  add "type": "digital" and "download_size": <number in MB>
The program will refuse untyped records rather than inventing product types.

Shipping rule: SGD 2.00 per kilogram, for demonstration only.

The optional SubscriptionProduct reflection exercise is not included.
The UML source is in UML_Class_Diagram.md (Mermaid).
