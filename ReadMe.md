# Trestle API Integration

This module provides a Python client for interacting with the Trestle API, specifically the Reverse Phone Lookup service. The client is designed to be async-first, type-safe, and production-ready.

## Features

- **Async/Await Support**: Built on top of `httpx` for non-blocking HTTP requests
- **Type Safety**: Uses Pydantic models for request/response validation
- **Retry Logic**: Automatic retries with exponential backoff
- **Error Handling**: Comprehensive error types for different failure scenarios
- **Configuration**: Environment variable based configuration with sensible defaults
- **Documentation**: Full docstrings and type hints for better IDE support

## Installation

Add the following to your `requirements.txt`:

```
httpx>=0.23.0
pydantic>=1.10.0
python-dotenv>=0.21.0
tenacity>=8.1.0
```

## Configuration

Create a `.env` file in your project root with the following variables:

```env
TRESTLE_API_KEY=your_api_key_here
TRESTLE_BASE_URL=https://api.trestleiq.com/3.2  # Optional
TRESTLE_TIMEOUT=30.0  # Optional, in seconds
TRESTLE_MAX_RETRIES=3  # Optional
```

## Usage

### Basic Example

```python
import asyncio
from app.core.third_party_integrations.trestle import get_trestle_client

async def main():
    async with get_trestle_client() as client:
        try:
            # Look up a phone number
            result = await client.reverse_phone.lookup_phone("2069735100")
            print(f"Phone: {result.phone_number}")
            print(f"Carrier: {result.carrier}")
            print(f"Line Type: {result.line_type}")
            
            if result.owners:
                print("\nOwners:")
                for owner in result.owners:
                    print(f"- {getattr(owner, 'name', 'Unknown')}")
                    
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### With Hints

```python
result = await client.reverse_phone.lookup_phone(
    phone="2069735100",
    country_hint="US",
    name_hint="John Doe",
    postal_code_hint="98101"
)
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