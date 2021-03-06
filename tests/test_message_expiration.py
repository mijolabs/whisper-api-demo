from test_config import Configuration
import json
import time

import httpx


config = Configuration()


def test_message_expiration():
    """
    Test for message expiration.
    """
    expiration_seconds = 3
    
    params = {
        "test_expiry": expiration_seconds
    }
    request_body = {
        "message":
            "Let us make the world a more empathetic and creative place "\
            "with great stories to be shared and enjoyed by anyone, anywhere and anytime."
    }
    
    # Create a message with defined expiration time
    post_message_response = httpx.post(config.base_url, params=params, json=request_body, auth=(config.username, config.password))
    post_message_response_json = post_message_response.json()
    assert post_message_response.status_code == 201

    # Check that message exists
    get_message_response = httpx.get(post_message_response_json["url"])
    assert get_message_response.status_code == 200
    
    # Wait until it has expired
    time.sleep(expiration_seconds + 2)

    #  Assert that it is no longer available
    second_get_message_response = httpx.get(post_message_response_json["url"])
    print(second_get_message_response.status_code)
    assert second_get_message_response.status_code == 404
