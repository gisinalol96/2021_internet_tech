from db import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/customers', methods=['GET'])
async def get_all():
    response = await select_all()
    return response


@app.route('/customers', methods=['POST'])
async def add_customer():
    customer_dict = {
        'id': request.json['customerID'],
        'name': request.json['customerName']
    }
    await insert_customer(customer_dict)
    return jsonify({"Info": "added"})


@app.route('/customers/<customerID>/billboards', methods=['POST'])
async def add_billboard(customerID):
    billboard_dict = {
        'id': request.json['billboardID'],
        'info': request.json['info'],
        'address': request.json['address'],
        'customer_id': customerID
    }
    await insert_billboard(billboard_dict)
    response = jsonify({'info': f'Billboard {billboard_dict} was successfully added'})
    return response


@app.route('/customers/<customerID>/billboards/<billboardID>', methods=['DELETE'])
async def remove_billboard(customerID, billboardID):
    await delete_billboard({'customerID': customerID,
                            'billboardID': billboardID})
    response = jsonify({'info': f"Task was successfully deleted"})
    return response


@app.route('/customers/<customerID>/billboards/<billboardID>', methods=['PATCH'])
async def modify_billboard(customerID, billboardID):
    params = request.json
    await update_billboard(params, customerID, billboardID)
    response = jsonify({'info': f"Task was successfully updated"})
    return response


@app.route('/customers/<from_customerID>', methods=['PATCH'])
async def move_billboard(from_customerID):
    await update_billboard({'customer_id': request.json['to_customerID']}, from_customerID, request.json['billboardID'])
    response = jsonify({'info': f"Billboard was successfully moved"})
    return response


if __name__ == '__main__':
    app.run()
