"""API for partner service"""

from flask import Blueprint, jsonify, request
from dao.models import Partner
from data import partner_data

partner_bp = Blueprint('partners', __name__, url_prefix='/partner')


@partner_bp.route('/list', methods=["POST"])
def get_list():
    """retrieve the list of partners based on the filter conditions"""

    err = validate_get_list_request(request.args, request.get_json())
    if err is not None:
        return err

    args = request.args
    name = args.get("name")
    filter_list = request.get_json()

    print("args: ", args)
    print("filter list: ", filter_list)
    
    partners = partner_data.get_list(name, filter_list)
    response = jsonify(partners)

    return response


def validate_get_list_request(args, body):
    """validate the filters for the /list endpoint"""

    if args.get("name") is not None and args.get("name") == "":
        return jsonify({"error": "name should not be empty string"})

    if body:
        if not isinstance(body, list):
            return jsonify({"error": "body should be list"})


@partner_bp.route('', methods=["POST"])
def add():
    """add a partner to the database
    return sucess message if added successfully,
    return error message if failed to add with 500 status code
    """

    body = request.get_json()
    print("body: ", body)

    partner = Partner(body.get("name"), body.get("email"),
                      body.get("organization"),
                      body.get("type_of_organization"))

    val = partner_data.add(partner)

    if val == 1:
        return jsonify({"message": "successfully added"})
    else:
        return jsonify({"error": "failed to add"}), 500


@partner_bp.route('/report', methods=["POST"])
def report():
    """return the report of the partners in json format"""

    type_groups = partner_data.group_by_type("type_of_organization")
    organization_groups = partner_data.group_by_type("organization")

    return jsonify({
        "type_groups": type_groups,
        "organization_groups": organization_groups
    })
