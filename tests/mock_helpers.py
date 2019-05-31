from arrangeit import base


def mocked_setup(mocker):
    mocker.patch("arrangeit.base.get_tkinter_root")
    mocker.patch("arrangeit.base.get_screenshot_widget")
    mocker.patch("arrangeit.base.ViewApplication")


def mocked_setup_root(mocker):
    mocked_setup(mocker)
    return mocker.patch("arrangeit.base.get_tkinter_root")


def mocked_setup_view(mocker):
    mocked_setup(mocker)
    return mocker.patch("arrangeit.base.ViewApplication")


def controller_mocked_app(mocker):
    app = mocker.MagicMock()
    app.grab_window_screen.return_value = (mocker.MagicMock(), (0, 0))
    return base.BaseController(app)


def controller_mocked_key_press(mocker, key):
    event = mocker.MagicMock()
    type(event).keysym = mocker.PropertyMock(return_value=key)
    base.BaseController(mocker.MagicMock()).on_key_pressed(event)
