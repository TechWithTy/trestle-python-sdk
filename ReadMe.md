# Trestle Python SDK

A comprehensive Python client for the Trestle API, providing seamless integration with Trestle's OSINT and data enrichment services. Built with async/await support, type safety, and production-grade error handling.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

- **Complete API Coverage**: Full support for all Trestle API endpoints
  - Phone Validation & Lookup
  - Reverse Phone Lookup
  - Smart CNAM Lookup
  - Reverse Address Lookup
  - Real Contact Verification
- **Modern Python**: Async/await support with `httpx`
- **Type Safety**: Pydantic models for all requests/responses
- **Production Ready**:
  - Automatic retries with exponential backoff
  - Comprehensive error handling
  - Environment-based configuration
  - Full test coverage
  - Pre-commit hooks
  - CI/CD ready

## 📦 Installation

```bash
# Using pip
pip install trestle-python-sdk

# Using poetry
poetry add trestle-python-sdk
```

## ⚙️ Configuration

Configure using environment variables or directly in your code:

```env
# Required
TRESTLE_API_KEY=your_api_key_here

# Optional
TRESTLE_BASE_URL=https://api.trestleiq.com/3.2
TRESTLE_TIMEOUT=30.0  # seconds
TRESTLE_MAX_RETRIES=3
```

## 🚀 Quick Start

### Phone Validation

```python
import asyncio
from trestle import TrestleClient

async def validate_phone():
    async with TrestleClient() as client:
        result = await client.phone_validation.validate(
            phone="+12069735100",
            country_hint="US"
        )
        print(f"Is valid: {result.is_valid}")
        print(f"Carrier: {result.carrier}")
        print(f"Line type: {result.line_type}")

asyncio.run(validate_phone())
```

### Reverse Phone Lookup

```python
async def reverse_phone_lookup():
    async with TrestleClient() as client:
        result = await client.reverse_phone.lookup(
            phone="2069735100",
            country_hint="US"
        )
        if result.owners:
            for owner in result.owners:
                print(f"Owner: {owner.name}")
                print(f"Type: {owner.type}")
```python
# Smart CNAM Lookup

async def cnam_lookup():
    async with TrestleClient() as client:
        result = await client.smart_cnam.lookup(
            phone="2069735100",
            country_hint="US"
        )
        if result.belongs_to:
            print(f"Name: {result.belongs_to.name}")
            print(f"Type: {result.belongs_to.type}")
```

### Reverse Address Lookup

```python
async def reverse_address_lookup():
    async with TrestleClient() as client:
        result = await client.reverse_address.lookup(
            address="1600 Amphitheatre Parkway",
            city="Mountain View",
            state="CA",
            postal_code="94043"
        )
        if result.results:
            for match in result.results:
                print(f"Formatted Address: {match.formatted_address}")
                print(f"Coordinates: {match.location.lat}, {match.location.lng}")
```

## 📚 Documentation

For detailed documentation, including all available endpoints and models, please see our [documentation](https://techwithty.github.io/trestle-python-sdk/).

## 🤝 Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For support or questions, please open an issue on our [GitHub repository](https://github.com/techwithty/trestle-python-sdk).
```

## API Reference

### `TrestleAPIClient`

Main client class for interacting with the Trestle API.

#### Methods

- `reverse_phone`: Access the Reverse Phone API
- `is_healthy()`: Check if the Trestle API is healthy
- `close()`: Close the client and release resources

### `ReversePhoneAPI`

Client for the Reverse Phone Lookup API.

#### Methods

- `lookup_phone(phone: str, country_hint: Optional[str] = None, name_hint: Optional[str] = None, postal_code_hint: Optional[str] = None) -> ReversePhoneResponse`
  
  Look up information about a phone number.
  
  **Parameters:**
  - `phone`: The phone number to look up (E.164 or local format)
  - `country_hint`: ISO-3166 alpha-2 country code hint
  - `name_hint`: Name associated with the phone number
  - `postal_code_hint`: Postal code of the subscriber address
  
  **Returns:**
  - `ReversePhoneResponse`: The response from the API
  
  **Raises:**
  - `InvalidPhoneNumberError`: If the phone number is invalid
  - `AuthenticationError`: If authentication fails
  - `RateLimitExceededError`: If rate limit is exceeded
  - `ServerError`: If there's a server-side error
  - `APIError`: For other API errors
  - `ValidationError`: If request validation fails

## Error Handling

The client defines several custom exceptions for different error scenarios:

- `ReversePhoneAPIError`: Base exception for all Reverse Phone API errors
- `InvalidPhoneNumberError`: Raised when the provided phone number is invalid
- `RateLimitExceededError`: Raised when the rate limit is exceeded
- `AuthenticationError`: Raised when authentication fails
- `ServerError`: Raised for server-side errors (5xx)
- `APIError`: Generic API error with status code and details
- `ValidationError`: Raised when request validation fails

## Testing

To run the tests, create a `tests/conftest.py` file with your test configuration:

```python
import pytest
from app.core.third_party_integrations.trestle import TrestleAPIClient

@pytest.fixture
def test_api_key():
    return "your_test_api_key"

@pytest.fixture
async def trestle_client(test_api_key):
    async with TrestleAPIClient(api_key=test_api_key) as client:
        yield client
```

Then create your test files in the `tests/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.