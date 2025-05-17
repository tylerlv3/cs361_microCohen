

# Metadata Microservice Communication Contract

Outline for how to use/interact with the metadata microservice.

**Base URL:** `https://cs361.tylerlv.me/metadata`

---

## Endpoints

### 1. Manage File Metadata

This endpoint allows you to add, update, or retrieve metadata associated with a specific file ID.

* **URL:** `/metadata/<fileID>`
* **`fileID` (Path Parameter):** An integer representing the unique identifier for the file.

---

## How to Programmatically REQUEST Data

You will interact with the microservice using standard HTTP requests.

### A. Adding or Updating Metadata (POST Request)

To add new metadata for a file or update existing metadata, send a `POST` request.

* **Method:** `POST`
* **URL:** `https://cs361.tylerlv.me/metadata/metadata/<fileID>`
    * Example: `https://cs361.tylerlv.me/metadata/metadata/123`
* **Headers:**
    * `Content-Type: application/json`
* **Body (JSON):**
    The request body must be a JSON object containing a single key `metadata`, whose value is another JSON object representing the custom metadata.
    ```json
    {
        "metadata": {
            "author": "Jane Doe",
            "version": "1.2",
            "tags": ["important", "draft"]
        }
    }
    ```
* **Example Call (using Python `requests` library):**
    ```python
    import requests
    import json

    file_id = 789
    metadata_payload = {
        "metadata": {
            "author": "John Smith",
            "status": "final"
        }
    }
    url = f"https://cs361.tylerlv.me/metadata/{file_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(metadata_payload), headers=headers)
        response.raise_for_status() # Raises an HTTPError for bad responses (e.g. 404)
        print(f"Success: {response.json()}")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
        print(f"Response body: {response.text if 'response' in locals() else 'No response'}")
    ```

### B. Retrieving Metadata (GET Request)

To retrieve existing metadata for a file, send a `GET` request.

* **Method:** `GET`
* **URL:** `https://cs361.tylerlv.me/metadata/<fileID>`
    * Example: `https://cs361.tylerlv.me/metadata/123`
* **Headers:** None required beyond standard HTTP headers.
* **Body:** None.

* **Example Call (using Python `requests` library):**
    ```python
    import requests

    file_id = 123
    url = f"https://cs361.tylerlv.me/metadata/{file_id}"

    try:
        response = requests.get(url)
        response.raise_for_status() # Raises an HTTPError for bad responses (e.g. 404)
        print(f"Success: {response.json()}") # The metadata itself is the JSON response
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
        print(f"Response body: {response.text if 'response' in locals() else 'No response'}")
    ```

---

## How to Programmatically RECEIVE Data

The microservice will respond with standard HTTP status codes and JSON-formatted bodies.

### A. Responses for POST Requests

* **Success - Metadata Added (HTTP 201 Created):**
    If a new file metadata record is created.
    ```json
    {
        "message": "Metadata added successfully",
        "id": <fileID>
    }
    ```
* **Success - Metadata Updated (HTTP 200 OK):**
    If existing metadata for the file is updated.
    ```json
    {
        "message": "Metadata updated successfully",
        "id": <fileID>
    }
    ```
* **Error - Bad Request (HTTP 400 Bad Request):**
    If the request JSON is malformed or the `metadata` field is missing.
    ```json
    {
        "error": "Data or metadata Missing"
    }
    ```

### B. Responses for GET Requests

* **Success - Metadata Found (HTTP 200 OK):**
    The body will be the JSON object representing the custom metadata.
    ```json
    {
        "author": "Jane Doe",
        "version": "1.2",
        "tags": ["important", "draft"]
    }
    ```
* **Error - File Not Found (HTTP 404 Not Found):**
    If no metadata exists for the given `fileID`.
    ```json
    {
        "error": "File not found"
    }
    ```

### C. General Error Response

* **Error - Method Not Allowed (HTTP 405 Method Not Allowed):**
    If an HTTP method other than `POST` or `GET` is used on the `/metadata/<fileID>` endpoint.
    ```json
    {
        "error": "Method not allowed"
    }
    ```
    
## UML Diagram
[UML Diagram](/umlDiagram.png)
