import cv2


def create_window(w=900, h=500):
    cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('settings', w, h)


# Затычка для cv2.createTrackbar
def nothing(n: int) -> None:
    pass


def create_setting(name, value, count, minimum=None):
    cv2.createTrackbar(name, 'settings', value, count, nothing)
    if minimum is None:
        minimum = -count
    cv2.setTrackbarMin(name, 'settings', minimum)


def get_setting(field):
    return cv2.getTrackbarPos(field, 'settings')


def gather(*args):
    result = []
    for field in args:
        result.append(get_setting(field))

    return result


def create_multiple_settings(settings: list[tuple]):
    for setting in settings:
        create_setting(*setting)
