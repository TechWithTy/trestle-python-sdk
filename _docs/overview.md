Trestle API Documentation (2.0.0)

Download OpenAPI specification:Download
Trestle Support: support@trestleiq.com URL: https://trestleiq.com/contact Terms of Service
Overview

Trestle provides identity data for businesses. This identity data is key for building and maintaining great customer relationships.
Base URL

https://api.trestleiq.com/ - US West (Default)
Authentication

Trestle controls access to the API and data via an API key. The API key is the primary data authentication method for your account. Your usage is recorded and reported via the API key. You may use a single API key for multiple Trestle APIs.
FAQ
How do I get an API Key?

Sign up for a Developer Portal account. Once verified, you can request access to any of Trestle’s Identity APIs or start using Real Contact API or Phone Validation API immediately. Here’s a brief overview of Trestle’s APIs:

    Reverse Phone API: Identify owner names and their demographics, phone metadata, current addresses, and email addresses.

    Caller Identification API: Access comprehensive phone metadata such as carrier, line type, and prepaid status, alongside crucial details including name, demographics, email addresses, and current address.

    Smart CNAM API: Validate phone numbers and identify the name or business to which the phone number belongs.

    Phone Validation API: Validate phone numbers, obtain phone metadata details, like carrier, line type, and prepaid status, and access a phone activity score to identify disconnected phone numbers.

    Reverse Address API: Discover detailed demographic information, historical addresses, email addresses, and phone numbers.

    Find Person API: Access comprehensive person details, including demographics, current and historical addresses, email addresses, and phone numbers.

    Real Contact API: Validate whether a lead is real by verifying the phone, email, and address and delivering essential insights, including a phone activity score, line types, name matches for phone, email, and address, and phone and email contact grades.

    Phone Feedback API: Offers a method of providing feedback to Treslte about dialed numbers for their connected/disconnected status and confirmation of right party contact.

Do you have a Postman Collection?

Yes, we do, and you can find it here. You will need to fork the collection to use it and an API key, for which you can sign up here.
Where can I check the status of the service?

You can find the API status on the Trestle Status Page.
Can I submit a request using POST method?

We recommend using GET for simplicity. POST is also supported; in this case, api_key must be in the request body and not part of the URL.
I have more questions. Who can I contact?

Please email us at support@trestleiq.com.
