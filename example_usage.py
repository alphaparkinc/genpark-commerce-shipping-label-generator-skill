import sys
import json
from shipping_generator import ShippingLabelGeneratorClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== Commerce Shipping Label Generator Verification ===")
    client = ShippingLabelGeneratorClient()

    # Address inputs
    sender = {
        "street": "100 Pine St",
        "city": "San Francisco",
        "postal_code": "94111",
        "country": "US"
    }

    recipient = {
        "street": "500 Broadway",
        "city": "New York",
        "postal_code": "10012",
        "country": "US"
    }

    # Volumetric package (Large box, light weight)
    parcel = {
        "length_in": 24.0,
        "width_in": 12.0,
        "height_in": 12.0,
        "weight_oz": 32.0 # 2 lbs
    }

    result = client.generate_label_draft(sender, recipient, parcel)
    
    print(f"\nCalculated Volumetric Weight: {result['volumetric_weight_lbs']} lbs")
    print(f"Postage Cost Estimate: ${result['postage_rate_est']:.2f}")
    
    print("\n[EasyPost / Carrier API Request Payload Draft]:")
    print(json.dumps(result["carrier_payload"], indent=2))

if __name__ == "__main__":
    main()
