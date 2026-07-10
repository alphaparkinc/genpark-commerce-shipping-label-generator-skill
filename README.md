# commerce-shipping-label-generator-skill

> **GenPark AI Agent Skill** -- # Commerce Shipping Label & Postage Generator Skill

This repository contains the **Commerce Shipping Label & Postage Generator Skill** — an agent customization skill config (`skill.json`), a production-ready Python SDK client (`shipping_generator.py`), and executable verification tests. It is designed to validate delivery addresses, compute volumetric package weights, estimate shipping rates, and compile carrier payloads.

---

## 🚀 Capabilities

* **Volumetric Rate Scaling:** Dynamically estimates billable weight thresholds using international dimensional formulas.
* **Zip Code Checks:** Matches and audits delivery postal formats.
* **Carrier Payload Drafting:** Assembles structured packages ready for submission to EasyPost and FedEx APIs.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 SDK Usage Reference

```python
from shipping_generator import ShippingLabelGeneratorClient

client = ShippingLabelGeneratorClient()

label = client.generate_label_draft(
    sender={"street": "123 Main St", "city": "SF", "postal_code": "94103", "country": "US"},
    recipient={"street": "456 Wall St", "city": "NY", "postal_code": "10005", "country": "US"},
    parcel={"length_in": 12, "width_in": 12, "height_in": 12, "weight_oz": 16}
)

print(f"Postage estimate: ${label['postage_rate_est']:.2f}")
```

---

## 📜 License
This project is licensed under the MIT License.