from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", defaults={'path': ''}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def entry_point(path):
    ops = {
        "add": add,
        "subtract": sub,
        "multiply": mult,
        "divide": div
    }
    if request.method in ["GET", "HEAD"]  and path == "":
        return "Hello Ian, welcome to my HTTP server - I trust you know how to use it", 200, {'Content-Type': 'text/plain'}
    try:

        try: 
            operation, num1, num2 = parse_vars(ops, path)
        except Exception as e:
            return str(e), 400, {'Content-Type': 'text/plain'}

        result = ops[operation](num1, num2)
        if request.method in ["GET", "HEAD"]:
            return str(result), 200, {'Content-Type': 'text/plain'}
        else:
            return jsonify({"result": result}), 200, {'Content-Type': 'application/json'}
    
    except ZeroDivisionError as e:
        return str(e), 422, {'Content-Type': 'text/plain'}
    except Exception as e:
        print(e)
        return "Internal Server Error, something went wrong, oops", 500, {'Content-Type': 'text/plain'}

def parse_vars(ops, path):
    if request.method in ["GET", "HEAD"]:
        vars = [var for var in path.split("/") if var]
        if len(vars) > 0:
            if vars[0] in ops:
                if len(vars) == 3:
                    if validate_number(vars[1]) and validate_number(vars[2]):
                        return vars[0], float(vars[1]), float(vars[2])
                    else:
                        raise TypeError("Incorrect operand types, 2 NUMBERS must be supplied. Usage: /<operation>/<num1>/<num2>")
                else:
                    raise ValueError("Incorrect number of operands, 2 must be supplied. Usage: /<operation>/<num1>/<num2>")
            else:
                raise Exception("Invalid operation type, valid operations are add, subtract, multiply and divide. Usage: /<operation>/<num1>/<num2>")
        else:
            raise Exception("No arguments supplied to GET operation. Usage: /<operation>/<num1>/<num2>")
    else:
        json_data = request.get_json()
        if json_data:
            if "operation" in json_data and json_data["operation"] in ops:
                operation = json_data["operation"]
                if "arguments" in json_data and isinstance(json_data["arguments"], list) and len(json_data["arguments"]) == 2:
                    if validate_number(json_data["arguments"][0]) and validate_number(json_data["arguments"][1]):
                        return operation, float(json_data["arguments"][0]), float(json_data["arguments"][1])
                    else:
                        raise TypeError('Incorrect argument types, 2 NUMBERS must be supplied. Usage: {"operation": "<operation>", "arguments": [ <num1>, <num2> ]}')
                else:
                    raise ValueError('Invalid arguments, 2 must be supplied in a list. Usage: {"operation": "<operation>", "arguments": [ <num1>, <num2> ]}')
            else:
                raise Exception('Invalid operation type, valid operations are add, subtract, multiply and divide. Usage: {"operation": "<operation>", "arguments": [ <num1>, <num2> ]}')
        else:
            raise Exception('No json data received in POST request. Usage: {"operation": "<operation>", "arguments": [ <num1>, <num2> ]}')

def validate_number(num):
    try: 
        float(num)
        return True
    except ValueError:
        return False

def add(num1, num2):
    return num1 + num2


def sub(num1, num2):
    return num1 - num2


def mult(num1, num2):
    return num1 * num2


def div(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        raise ZeroDivisionError("Division by 0")
