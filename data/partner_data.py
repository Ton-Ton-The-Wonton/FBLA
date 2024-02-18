"""partner data mapping"""

from sqlalchemy import exc
from sqlalchemy.sql import func
from app.__init__ import db_session, logger
from dao.models import Partner, partner_columns, TypeOfOrganizationEnum, get_enum_member_by_value


def init():
    """init

    init data
    """

    partners = [
        Partner('admin', 'admin@localhost', "Google"),
        Partner('John Doe', 'john.doe@example.com', "Amazon")
    ]

    db_session.add_all(partners)
    db_session.commit()


def get_list(name="", filter_list=None):
    """get_by_name

    Args:
        name: name

    Returns:
        list of partners filtered by name
    """

    if name and name != "":
        filter_list.append({
            "name": "name",
            "operation": "like",
            "value": name
        })

    query = db_session.query(Partner)

    if filter_list:
        for f in filter_list:
            name = f["name"]
            operation = f["operation"]
            value = f["value"]

            if name not in partner_columns:
                continue
            if operation == '=':
                expr = getattr(Partner, name) == value
            elif operation == 'like':
                expr = getattr(Partner, name).like(f'%{value}%')
            else:
                logger.warning("Unsupported operation: %s", operation)
            query = query.where(expr)

    partners = query.all()
    partners = [p.as_dict() for p in partners]

    for p in partners:
        p["type_of_organization"] = get_enum_member_by_value(
            TypeOfOrganizationEnum, p["type_of_organization"]).name

    return partners


def add(partner) -> int:
    """add
    Args:
        partner: a partner 
    Returns:
        number of rows successfully added
    """

    try:
        db_session.add(partner)
        db_session.commit()

        return 1
    except exc.IntegrityError as exception:
        logger.warning("data: partner_data: add error: %s", exception)
        
        return 0


def group_by_type(name):
    """showing the amount of each type_of_organization"""

    attr = getattr(Partner, name)
    query = db_session.query(attr, func.count(Partner.id)).group_by(attr)
    groups = query.all()

    if name == "type_of_organization":
        groups = [{
            "type_of_organization":
            get_enum_member_by_value(TypeOfOrganizationEnum,
                                     group.type_of_organization).name,
            "count":
            group[1]
        } for group in groups]
    else:
        groups = [{
            "organization": group[0],
            "count": group[1]
        } for group in groups]

    return groups
