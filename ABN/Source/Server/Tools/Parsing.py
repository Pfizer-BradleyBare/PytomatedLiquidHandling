import json


def JsonPrettyString(JsonData: dict) -> str:
    return json.dumps(JsonData, indent=4, sort_keys=True)


def ParseHTTPResponse(JSONResponse: dict, ExpectedKeys: tuple):

    if not all(key in JSONResponse for key in ExpectedKeys):
        print(
            "Incorrect JSON object received. Please try again... Expected Keys:",
            str(ExpectedKeys),
        )
        return None
    # Confirm Response keys are present before proceeding.

    return json.dumps(JSONResponse)


def ParsePOST(PostData: bytes, ExpectedKeys: tuple) -> dict:

    print("Parsing POST data into JSON: ", PostData)

    try:
        PostData = json.loads(PostData.decode().replace("'", ""))

        print(JsonPrettyString(PostData))

        ReturnData = ParseHTTPResponse(PostData, ExpectedKeys)

    except Exception:
        print("Error Parsing Data! Bad format.")
        ReturnData = None

    # We will always return the data we receive as a logging event
    return ReturnData
