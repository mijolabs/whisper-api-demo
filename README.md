# Whisper API [DEMO/PoC]

This demo proof of concept was developed over a weekend as part of a coding challenge assignment. It works as expected but isn't maintained in any way and is just here for archiving purposes. The project was developed according to the following given instructions:

> The goal is to design and build a RESTful API to serve as the backend for a message sharing system.
> It should support the following features:
> - [x] A client should be able to create a message, and get the URL to the message
> - [x] A client should be able to view any message, if the URL is known to the client
> - [x] It should be infeasible to guess the URL to a message
> - [x] Messages should only be stored and available on the server for 7 days, and deleted automatically thereafter.
> - [x] Use an in-memory solution for storing any data for this service.
> - [x] Consider the appropriate HTTP verbs, headers and responses to use.
> - [x] You should also include tests to assert the correctness of your solution.
> - [x] Please document significant security risks/assumptions.
> - [x] The complete solution should include a README that describes how to build and run the solution.
> - [x] Please choose between Python, Java or Go, and your own choice of frameworks/libraries to help implement the web layer and testing.
> - [x] Ensure the project is easily built with a common build system for the chosen ecosystem.
> - [x] Consider including a Dockerfile if you wish to demonstrate your knowledge of image building.

## Main Components
- **FastAPI** is a modern, fast (high-performance), web framework for building APIs.
- **Redis** is an in-memory data structure store, used as a database, cache, and message broker.

## Requirements
- Python >= 3.8
- Installed dependencies (as according to `requirements.txt`)
- Redis

The provided `Dockerfile` will greatly simplify the setup process.

## Running it with Docker
0. ***Clone it:*** `git clone https://github.com/mijolabs/whisper-demo && cd whisper-demo`
1. ***Build it:*** `docker build -t whisper-demo .`
2. ***Start it:*** `docker run -d --rm --name whisper -p 8000:8000 whisper-demo` (or omit the `-d` flag to view the live access logs)
3. ***Try it:*** Browse to http://127.0.0.1:8000/docs (you may need to replace the ip with your docker server address)

If you see Swagger UI docs it means we're in business.

## Usage
The Swagger UI can be used to test the API functionality, or if you prefer using a proper client you can use e.g. Postman or whip something up in Python code (examples below). The API root accepts a POST request for creating a new message, and the response provides a URL where a client can GET it from.

HTTP Basic Auth is enabled for POST requests to create new messages.

| Default Username | Default Password |
| ---------------- | ---------------- |
| `whisper`      | `demo`           |

Let's start by creating a new message by sending a POST request with the message string in the request body. 

Python [httpx](https://github.com/encode/httpx) example of creating a new message:
```python
import httpx

endpoint = "http://127.0.0.1:8000"
auth = ( "whisper", "demo" )

request_body = {
    "message": "Whisper words of wisdom, let it be."
    }

r = httpx.post(endpoint, auth=auth, json=request_body)
print(r.text)
```
Browse to the message URL in the response and take a look. You should see the same JSON contents as you received in the POST reply earlier.

For this demo project, there is a URL parameter `test_expiry=n` provided that can be used to test the message expiration function. It enables setting the number of seconds for message expiry, overriding the 7 day default expiration time.

Python [httpx](https://github.com/encode/httpx) example using the `test_expiry` parameter:
```python
import httpx

expiration_seconds = 45

endpoint = "http://127.0.0.1:8000"
auth = ( "whisper", "demo" )

params = { "test_expiry": expiration_seconds }
request_body = { "message": f"This message will self-destruct in {expiration_seconds} seconds." }

r = httpx.post(endpoint, auth=auth, params=params, json=request_body)
print(r.text)
```
You can GET the message at its URL to verify it exists and reload the URL after it should have expired to confirm that it is gone.

## Limitations, Possible Bugs, and Vulnerabilities
- The lack of TLS opens up for the possibility of MITM attacks. HTTPS can be easily enabled by utilizing certificates but usually HTTPS is handled by an external tool, e.g. load balancer or cloud service.
- It is theoretically possible to launch a bruteforce attack and eventually stumble upon a valid message ID and access its contents. Although unfeasible for most, asynchronous requests or other methods could be used to speed up the attack. By default, this demo application uses the same length and character set used by Google Docs for sharing links to documents, which should be sufficient for our purpose considering the automatic deletion of messages after 7 days. Further mitigation could be performed by increasing the length of generated message IDs, request rate limiting, adding some form of authentication mechanism for this endpoint, or restricting access to allow requests only from specific client IPs or subnets.
- The message ID could leak in other ways, e.g. the web application may log a request and the URL could be retrievable from the log file.
- It may be possible to inject harmful code in message contents to exploit Redis or a web application displaying the message. This demo app has implemented basic HTML escaping but further input validation may be required.
- Authentication credentials are exposed in cleartext in the configuration file. It is assumed to be protected by other means.

## TODO
- Better error handling.
- Logging.
- More tests.
- Much refactoring.

## Testing
Various assertion tests are available under `tests/` for use with Pytest.

0. Enter `tests/` and create a virtual environment, e.g.: `python -m venv .venv`
1. Activate the venv: `source .venv/bin/activate`
2. Install dependencies: `pip install -r test_requirements.txt`
3. Run `pytest`
