from typing import Union


def _assert_almost_equel(number_received: Union[float, int], number_expected: Union[float, int], message=None, factor=0.02):
    if message is None:
        message = "Expected {e}, received {r}".format(e=number_expected, r=number_received)
    assert number_expected - factor * number_expected < number_received < number_expected + factor * number_expected, message
    return True