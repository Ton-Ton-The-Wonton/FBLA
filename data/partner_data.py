"""interact with the partner table in the database"""

from sqlalchemy import exc, func
from app.__init__ import db_session
from dao.models import Partner, partner_columns

ENUM_TO_TYPE = [
    "Unknown", "Governmental Organization", "Non-Governmental Organization",
    "Educational/Research Institution", "Healthcare Organization",
    "Community Center/Library", "For-Profit Business",
    "Arts/Cultural Organization", "Sports/Recreational Organization", "Other"
]


def get_list(name="", filter_list=None):
    """given the filter conditions, return the matching partners"""

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
            value = f["value"]

            if name not in partner_columns:
                continue

            expr = getattr(Partner, name).like(f'%{value}%')
            query = query.where(expr)

    partners = query.all()
    print("partners1: ", partners)
    partners = [p.as_dict() for p in partners]
    print("partners2: ", partners)

    for partner in partners:
        partner["type_of_organization"] = ENUM_TO_TYPE[
            partner["type_of_organization"]]

    return partners


def add(partner):
    """add a partner to the database

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
        print("Exception: ", exception)

        return 0


def group_by_type(grouping_attr):
    """showing the amount of each type of organization"""

    attr = getattr(Partner, grouping_attr)
    query = db_session.query(attr, func.count(Partner.id)).group_by(attr)
    groups = query.all()

    if grouping_attr == "type_of_organization":
        groups = [{
            "type_of_organization":
            ENUM_TO_TYPE[group.type_of_organization],
            "count":
            group[1]
        } for group in groups]
    else:
        groups = [{
            "organization": group[0],
            "count": group[1]
        } for group in groups]

    return groups
