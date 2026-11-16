
import json

import allure


def attach_api_response(response):

    metadata = (
        f"Method: {response.request.method}\n"
        f"URL: {response.url}\n"
        f"Status Code: {response.status_code}\n"
        f"Response Time: {response.elapsed.total_seconds():.3f}s"
    )

    allure.attach(
        metadata,
        name="API Response Metadata",
        attachment_type=allure.attachment_type.TEXT
    )

    try:
        response_body = json.dumps(
            response.json(),
            indent=4
        )

        attachment_type = allure.attachment_type.JSON

    except ValueError:

        response_body = response.text

        attachment_type = allure.attachment_type.TEXT

    allure.attach(
        response_body,
        name="API Response Body",
        attachment_type=attachment_type
    )
