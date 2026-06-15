import os
import asyncio
from app.services.ai_service import interpret_prescription
from dotenv import load_dotenv
import json
from unittest.mock import AsyncMock, patch

load_dotenv()

# Mock objects to simulate OpenAI/Nvidia client response structure
class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

mock_json = """{
    "doctor_name": "Dr. Smith",
    "patient_name": "John Doe",
    "hospital_name": "Clinic",
    "date": "05/08/2026",
    "diagnosis": "Infection",
    "medicines": [
        {"name": "Advil", "dosage": "200mg", "timing": "every 4 hours", "duration": "3 days", "instructions": "Take for pain"},
        {"name": "Amoxicillin", "dosage": "500mg", "timing": "three times a day", "duration": "7 days", "instructions": "Finish course"}
    ],
    "summary": "Sample prescription details.",
    "disclaimer": "Contact the doctor or hospital for prescription information.",
    "extracted_text": "Advil and Amoxicillin prescription details."
}"""

async def run_test():
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = MockResponse(mock_json)
    with patch('app.services.ai_service.get_client', return_value=mock_client):
        # Pass dummy bytes as the image content
        result_json = await interpret_prescription(b"dummy_image_content")
        return result_json

print("Interpreting prescription and verifying with OpenFDA...")
result_json = asyncio.run(run_test())
result = json.loads(result_json)

print("\n--- RESULTS ---")
print(f"Summary: {result.get('summary')}")
print("\nMedicines Found:")
for med in result.get("medicines", []):
    print(f"- {med['name']} ({med['dosage']})")
    print(f"  Verified: {med.get('verified')}")
    if med.get('verified'):
        print(f"  Generic Name: {med.get('generic_name')}")
        print(f"  Official Purpose: {med.get('official_purpose')[:100]}...")
    print(f"  Timing: {med.get('timing')}")

print(f"\nDisclaimer: {result.get('disclaimer')}")

