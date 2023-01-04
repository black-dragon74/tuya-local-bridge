def validate_device(dev_id, dev_dict):
    return dev_dict.get(dev_id, "") != ""


def resp_success(resp):
    return {
        "STATUS": "OK",
        **resp
    }


def resp_err(resp):
    return {
        "STATUS": "ERR",
        **resp
    }
