#!/usr/bin/env python3

import json
import requests


def get_url(locale, workspace, webservice):
    """Form an absolute Azure ML url and return it as a string.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param webservice: Azure ML webservice id.
    :return: str
    """
    return "https://{}.management.azureml.net/workspaces/{}/webservices/{}/endpoints".format(locale, workspace, webservice)


def get_endpoint(locale, workspace, token, webservice, name):
    """Retrieve specific Azure endpoint data for a webservice and return it as a JSON dict.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :param name: Azure ML webservice endpoint name.
    :return: dict
    """
    url = get_url(locale, workspace, webservice) + "/{}".format(name)
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer {}'.format(token))}
    try:
        req = requests.get(url=url, headers=headers)
        res = json.loads(req.text)
        if req.ok:
            return res
        else:
            print("FAILURE {}: {} - {}".format(req.status_code, res["error"]["code"], res["error"]["message"]))
            raise requests.HTTPError(req.status_code)
    except requests.RequestException as error:
        print(error)


def get_endpoints(locale, workspace, token, webservice):
    """Retrieve all Azure endpoint data for a webservice and return it as a JSON dict.

    :param locale: Azure region
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :return: dict
    """
    url = get_url(locale, workspace, webservice)
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer {}'.format(token))}
    try:
        req = requests.get(url=url, headers=headers)
        res = json.loads(req.text)
        if req.ok:
            return res
        else:
            print("FAILURE {}: {} - {}".format(req.status_code, res["error"]["code"], res["error"]["message"]))
            raise requests.HTTPError(req.status_code)
    except requests.RequestException as error:
        print(error)


def get_endpoints_names(locale, workspace, token, webservice):
    """Retrieve all Azure endpoint names for a webservice and return it as a list.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :return: list
    """
    endpoints = get_endpoints(locale, workspace, token, webservice)
    return [endpoint["Name"] for endpoint in endpoints]


def create_endpoint(locale, workspace, token, webservice, name, desc, tlvl=None):
    """Create a new endpoint for a webservice and return success status as a bool.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :param name: New Azure ML webservice endpoint name.
    :param desc: New Azure ML webservice endpoint description.
    :param tlvl: (Optional) New Azure ML webservice endpoint throttle level.
    :return: bool
    """
    url = get_url(locale, workspace, webservice) + "/{}".format(name)
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer {}'.format(token))}
    data = {
        "Description": desc
    }
    if tlvl:
        data["ThrottleLevel"] = tlvl

    try:
        req = requests.put(url=url, data=json.dumps(data), headers=headers)
        if req.ok:
            print("CREATED ENDPOINT '{}': {}".format(name, req.status_code))
            return True
        else:
            res = json.loads(req.text)
            print("FAILURE {}: {} - {}".format(req.status_code, res["error"]["code"], res["error"]["message"]))
            raise requests.HTTPError(req.status_code)
    except requests.RequestException as error:
        print(error)
        return False


def delete_endpoint(locale, workspace, token, webservice, name):
    """Delete an endpoint for a webservice and return success status as a bool.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :param name: Azure ML webservice endpoint name.
    :return: bool
    """
    if name == "default":
        print("FAILURE 400: UnauthorizedRequest - Cannot delete default endpoint.")
        return False
        # raise requests.HTTPError(400)
    url = get_url(locale, workspace, webservice) + "/{}".format(name)
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer {}'.format(token))}
    try:
        req = requests.delete(url=url, headers=headers)
        if req.ok:
            print("DELETED ENDPOINT '{}': {}".format(name, req.status_code))
            return True
        else:
            res = json.loads(req.text)
            print("FAILURE {}: {} - {}".format(req.status_code, res["error"]["code"], res["error"]["message"]))
            raise requests.HTTPError(req.status_code)
    except requests.RequestException as error:
        print(error)
        return False


def update_endpoint(locale, workspace, token, webservice, endpoint_name, model_name, base_loc, relative_loc, sas_token):
    """Update an endpoint for a webservice and return success status as a bool.

    :param locale: Azure region.
    :param workspace: Azure ML workspace id.
    :param token: Azure ML API token.
    :param webservice: Azure ML webservice id.
    :param endpoint_name: Azure ML webservice endpoint name.
    :param model_name: Azure ML trained model name.
    :param base_loc: New trained model base location.
    :param relative_loc: New trained model relative location.
    :param sas_token: Azure Blob SAS token.
    :return: bool
    """
    data = {
                "Resources": [
                    {
                        "Name": model_name,
                        "Location":
                            {
                                "BaseLocation": base_loc,
                                "RelativeLocation": relative_loc,
                                "SasBlobToken": sas_token
                            }
                    }
                ]
           }

    url = get_url(locale, workspace, webservice) + "/{}".format(endpoint_name)
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer {}'.format(token))}

    try:
        req = requests.patch(url=url, data=json.dumps(data), headers=headers)
        if req.ok:
            print("UPDATED ENDPOINT '{}': {}".format(endpoint_name, req.status_code))
            return True
        else:
            res = json.loads(req.text)
            print("FAILURE {}: {} - {}".format(req.status_code, res["error"]["code"], res["error"]["message"]))
            raise requests.HTTPError(req.status_code)
    except requests.RequestException as error:
        print(error)
        return False
