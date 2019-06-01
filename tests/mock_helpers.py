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


def controller_mocked_for_run(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.prepare_view")
    mocker.patch("arrangeit.base.BaseController.next")
    mocker.patch("arrangeit.base.get_mouse_listener")
    mocker.patch("arrangeit.base.click_left")
    return base.BaseController(mocker.MagicMock())


def controller_mocked_for_next(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.set_screenshot")
    mocker.patch("arrangeit.base.BaseController.set_default_geometry")
    mocker.patch("arrangeit.base.BaseController.place_on_top_left")
    controller = base.BaseController(mocker.MagicMock())
    controller.model = base.WindowModel(workspace=1)
    controller.generator = mocker.MagicMock(side_effect=[0, 1, 2])
    return controller


def controller_mocked_next(mocker):
    mocked_setup(mocker)
    mocker.patch("arrangeit.base.BaseController.next")
    mocker.patch("arrangeit.base.WindowModel")
    mocker.patch("arrangeit.base.move_cursor")
    controller = base.BaseController(mocker.MagicMock())
    controller.model = base.WindowModel(rect=(50, 50, 100, 100), workspace=1)
    return controller
