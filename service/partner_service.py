"""service"""

from data import partner_data


def get_list(name, filter_list):
    """get_list"""

    return partner_data.get_list(name, filter_list)


def add(partner) -> int:
    """add"""

    return partner_data.add(partner)


def report():
    """reports of partners"""

    type_groups = partner_data.group_by_type("type_of_organization")
    organization_groups = partner_data.group_by_type("organization")

    return {
        "type_groups": type_groups,
        "organization_groups": organization_groups
    }
