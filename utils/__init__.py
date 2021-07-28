from rest_framework.request import Request

def middle_data_transfer(value):
    """Transfer value in request to correct data type in python"""
    if value == 'true':
        return True
    elif value == 'false':
        return False
    return value

def data_from_method_post_put_delete(request: Request, *args) -> tuple:
    """
    :param request: request từ client
    :param args: Danh sách các key trong request
    :return tuple: (data1, data2, ...) or (data1,) if only take one key from request
    """

    def get_data():
        for key in args:
            if request.data.get(key) is not None:
                yield middle_data_transfer(request.data.get(key))
            else:
                # Cho phương thức delete
                yield middle_data_transfer(request.query_params.get(key))

    return tuple(get_data())