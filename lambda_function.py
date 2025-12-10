import json
import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')  # Make sure this matches your table name

# Helper to format HTTP responses
def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    # 1) Read HTTP method (GET, POST, etc.)
    http_method = event.get("httpMethod")
    
    # 2) Read path (like /Dev/items or /Dev/items/1)
    path = event.get("path", "")
    
    # 3) Read path parameters (like { "id": "1" } for /items/1)
    path_params = event.get("pathParameters") or {}
    
    # 4) Read body (for POST/PUT). It will be a JSON string.
    raw_body = event.get("body")
    body = None
    if raw_body:
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return response(400, {"message": "Invalid JSON body"})
    
    # CREATE: POST /items
    if http_method == "POST" and path.endswith("/items"):
        if not body or "id" not in body:
            return response(400, {"message": "Field 'id' is required in body"})
        
        table.put_item(Item=body)
        
        return response(201, {
            "message": "Item created successfully",
            "item": body
        })

    # READ: GET /items/{id}
    if http_method == "GET" and path_params.get("id"):
        item_id = path_params["id"]  # example: "1"

        result = table.get_item(Key={"id": item_id})
        item = result.get("Item")

        if not item:
            return response(404, {"message": "Item not found"})

        return response(200, item)

    # UPDATE: PUT /items/{id}
    if http_method == "PUT" and path_params.get("id"):
        item_id = path_params["id"]

        if not body:
            return response(400, {"message": "Request body is required for update"})

        body["id"] = item_id  # force id from path

        table.put_item(Item=body)

        return response(200, {
            "message": "Item updated successfully",
            "item": body
        })

    # DELETE: DELETE /items/{id}
    if http_method == "DELETE" and path_params.get("id"):
        item_id = path_params["id"]

        table.delete_item(Key={"id": item_id})

        return response(200, {
            "message": f"Item with id {item_id} deleted successfully"
        })
    
    # other methods/paths not handled
    return response(400, {
        "message": "No handler for this method/path",
        "http_method": http_method,
        "path": path,
        "path_params": path_params,
        "body": body
    })


