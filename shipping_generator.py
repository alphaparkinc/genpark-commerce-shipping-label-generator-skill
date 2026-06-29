import os
from typing import Dict, Any, Optional

class ShippingLabelGeneratorClient:
    """
    Production-grade shipping utility that parses package details, computes volumetric weight,
    runs postal code format audits, and constructs EasyPost/FedEx standard API payloads.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SHIPPING_API_KEY")

    def validate_postal_code(self, code: str, country: str) -> bool:
        """
        Validates basic postal code formats for US and general international rules.
        """
        code_clean = code.strip()
        if country.upper() == "US":
            # Must be 5 digit zip code
            return len(code_clean) == 5 and code_clean.isdigit()
        return len(code_clean) >= 3

    def generate_label_draft(
        self,
        sender: Dict[str, Any],
        recipient: Dict[str, Any],
        parcel: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimates shipping parameters and outputs a clean payload draft for shipping carriers.
        """
        # Validate postal codes
        if not self.validate_postal_code(sender.get("postal_code", ""), sender.get("country", "US")):
            raise ValueError("Invalid sender postal code format.")
        if not self.validate_postal_code(recipient.get("postal_code", ""), recipient.get("country", "US")):
            raise ValueError("Invalid recipient postal code format.")

        length = float(parcel.get("length_in", 1.0))
        width = float(parcel.get("width_in", 1.0))
        height = float(parcel.get("height_in", 1.0))
        weight_oz = float(parcel.get("weight_oz", 1.0))

        # Volumetric Weight Formula (US Domestic / DHL / FedEx standard: L*W*H / 166)
        vol_weight = round((length * width * height) / 166.0, 2)
        
        # Standard weight in lbs
        actual_weight_lbs = round(weight_oz / 16.0, 2)
        billable_weight = max(actual_weight_lbs, vol_weight)

        # Rate estimation rules (base $5.00 + $0.50 per billable lb)
        rate = round(5.00 + (billable_weight * 0.50), 2)

        # EasyPost payload structure format
        carrier_payload = {
            "shipment": {
                "to_address": {
                    "street1": recipient.get("street"),
                    "city": recipient.get("city"),
                    "zip": recipient.get("postal_code"),
                    "country": recipient.get("country")
                },
                "from_address": {
                    "street1": sender.get("street"),
                    "city": sender.get("city"),
                    "zip": sender.get("postal_code"),
                    "country": sender.get("country")
                },
                "parcel": {
                    "length": length,
                    "width": width,
                    "height": height,
                    "weight": weight_oz
                },
                "carrier_accounts": ["ca_fedex_123"],
                "options": {"bill_weight": billable_weight}
            }
        }

        return {
            "volumetric_weight_lbs": vol_weight,
            "postage_rate_est": rate,
            "carrier_payload": carrier_payload
        }
