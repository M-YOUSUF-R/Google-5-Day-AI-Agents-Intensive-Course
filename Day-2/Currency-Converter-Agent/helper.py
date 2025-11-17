def get_fee_for_payment_method(method:str)->dict:
    fee_database:dict = {
        "platinum credit card": 0.02,  # 2%
        "gold debit card": 0.035,  # 3.5%
        "bank transfer": 0.01,  # 1%
    }

    fee:int = fee_database.get(method.lower())

    if fee is not None:
        return {"status":"success","fee_percentage":fee}
    else:
        return {
            'status':"error",
            'error_message':f"Payment method '{method}' not found",
        }

def get_exchange_rate(base_currency:str,target_currency:str)->dict:
    rate_database = {
        "usd":{
            "eur":0.93,
            "jpy":157.0,
            "inr": 83.58,
        }
    }

    base = base_currency.lower()
    target = target_currency.lower()

    rate = rate_database.get(base,{}).get(target)

    if rate is not None:
        return {"status":"success","rate":rate}
    else:
        return {
            "status":"error",
            "error_message":f"Unsupported currency pair: {base_currency}/{target_currency}",
        }

def show_python_code_and_result(response):
    for i in range(len(response)):
        # Check if the response contains a valid function call result from the code executor
        if (
            (response[i].content.parts)
            and (response[i].content.parts[0])
            and (response[i].content.parts[0].function_response)
            and (response[i].content.parts[0].function_response.response)
        ):
            response_code = response[i].content.parts[0].function_response.response
            if "result" in response_code and response_code["result"] != "```":
                if "tool_code" in response_code["result"]:
                    print(
                        "Generated Python Code >> ",
                        response_code["result"].replace("tool_code", ""),
                    )
                else:
                    print("Generated Python Response >> ", response_code["result"])
