import cv2


class Window:
    def __init__(self, winname, w=900, h=500):
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(winname, w, h)

        self.winname = winname

    def create_setting(self, name, value, count, minimum=None):
        cv2.createTrackbar(name, self.winname, value, count, nothing)
        if minimum is None:
            minimum = -count
        cv2.setTrackbarMin(name, self.winname, minimum)

    def get_setting(self, field):
        return cv2.getTrackbarPos(field, self.winname)

    def gather(self, *args):
        result = []
        for field in args:
            result.append(self.get_setting(field))

        return result

    def create_multiple_settings(self, settings: list[tuple]):
        for setting in settings:
            self.create_setting(*setting)


# Затычка для cv2.createTrackbar
def nothing(n: int) -> None:
    pass
