"""controller"""
from flask import Blueprint, jsonify, request
from app import logger
from dao.response import Response, RequestErrorResponse
from dao.models import Partner
from service import partner_service

partner_bp = Blueprint('partners', __name__, url_prefix='/partner')


@partner_bp.route('/list', methods=["POST"])
def get_list():
    """get_list

    Args:
        name: name

    Returns:
        json response
    """

    err = validate_get_list_request(request.args, request.get_json())
    if err is not None:
        return err

    args = request.args
    name = args.get("name")
    filter_list = request.get_json()

    logger.info("args: %s", args)
    logger.info("filter list: %s", filter_list)
    partners = partner_service.get_list(name, filter_list)
    response = jsonify(Response(0, partners).as_dict())

    return response


def validate_get_list_request(args, body):
    """validate_get_list_request

    Args:
        args: request args
        body: request body

    Returns:
        json response
    """

    if args.get("name") is not None and args.get("name") == "":
        return jsonify(
            RequestErrorResponse("name shoule not be empty string").as_dict())

    if body:
        if not isinstance(body, list):
            return jsonify(
                RequestErrorResponse("body shoule be list").as_dict())


@partner_bp.route('', methods=["POST"])
def add():
    """add

    Returns:
        json response
    """

    body = request.get_json()
    logger.info("add a partner: %s", body)

    partner = Partner(body.get("name"), body.get("email"),
                      body.get("organization"),
                      body.get("type_of_organization"))

    succ = partner_service.add(partner)
    if succ != 0:
        return jsonify(Response(0, succ).as_dict())

    return jsonify(RequestErrorResponse("name or email exists").as_dict())


@partner_bp.route('/report', methods=["POST"])
def report():
    """report

    some statistics of partners
    """

    groups = partner_service.report()
    return jsonify(Response(0, groups).as_dict())
