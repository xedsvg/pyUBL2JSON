import json
import logging

class InvoiceParser:
    @staticmethod
    def parse_invoice(invoice_data):
        try:
            # Handle both string and dict input
            data = json.loads(invoice_data) if isinstance(invoice_data, str) else invoice_data
            invoice_details = data.get('Invoice', {})
            
            # Extract delivery information including delivery party
            delivery_location = None
            delivery_party = None
            if 'cac:Delivery' in invoice_details:
                delivery = invoice_details['cac:Delivery']
                # Extract delivery location
                if 'cac:DeliveryLocation' in delivery:
                    location = delivery['cac:DeliveryLocation']
                    if 'cac:Address' in location:
                        address = location['cac:Address']
                        delivery_location = {
                            'street': address.get('cbc:StreetName', ''),
                            'city': address.get('cbc:CityName', ''),
                            'postal_code': address.get('cbc:PostalZone', ''),
                            'country': address.get('cac:Country', {}).get('cbc:IdentificationCode', '')
                        }

                # Fixed delivery party extraction
                delivery_party = {
                    'name': delivery.get('cac:DeliveryParty', {})
                            .get('cac:PartyName', {})
                            .get('cbc:Name', 'N/A'),
                    'delivery_date': delivery.get('cbc:ActualDeliveryDate', 'N/A'),
                    'location_id': delivery.get('cac:DeliveryLocation', {})
                            .get('cbc:ID', {})
                            .get('#text', 'N/A'),
                    'location_scheme': delivery.get('cac:DeliveryLocation', {})
                            .get('cbc:ID', {})
                            .get('@schemeID', 'N/A')
                }

            # Extract prices
            def extract_amount(amount_field):
                if isinstance(amount_field, dict):
                    return float(amount_field.get('#text', '0'))
                return float(amount_field or '0')

            monetary_total = invoice_details.get('cac:LegalMonetaryTotal', {})
            prices = {
                'tax_exclusive': extract_amount(monetary_total.get('cbc:TaxExclusiveAmount')),
                'tax_inclusive': extract_amount(monetary_total.get('cbc:TaxInclusiveAmount')),
                'payable_amount': extract_amount(monetary_total.get('cbc:PayableAmount')),
                'currency': monetary_total.get('cbc:PayableAmount', {}).get('@currencyID', 'RON')
            }

            # Build invoice information
            invoice_info = {
                "invoice_number": invoice_details.get("cbc:ID", "N/A"),
                "issue_date": invoice_details.get("cbc:IssueDate", "N/A"),
                "due_date": invoice_details.get("cbc:DueDate", "N/A"),
                "currency": invoice_details.get("cbc:DocumentCurrencyCode", "N/A"),
                "seller": invoice_details.get("cac:AccountingSupplierParty", {}).get("cac:Party", {}).get("cac:PartyName", {}).get("cbc:Name", "N/A"),
                "buyer": invoice_details.get("cac:AccountingCustomerParty", {}).get("cac:Party", {}).get("cac:PartyName", {}).get("cbc:Name", "N/A"),
                "delivery_location": delivery_location,
                "delivery_party": delivery_party,
                "prices": prices
            }
            
            # Extract products
            invoice_lines = invoice_details.get("cac:InvoiceLine", [])
            if not isinstance(invoice_lines, list):
                invoice_lines = [invoice_lines]
                
            invoice_info["products"] = []
            for line in invoice_lines:
                product = {
                    "name": line.get("cac:Item", {}).get("cbc:Name", "N/A"),
                    "quantity": float(line.get("cbc:InvoicedQuantity", {}).get("#text", "0")),
                    "price": float(line.get("cac:Price", {}).get("cbc:PriceAmount", {}).get("#text", "0")),
                }
                invoice_info["products"].append(product)
            
            return invoice_info
            
        except Exception as e:
            logging.error(f"Error parsing invoice: {str(e)}")
            raise
