import pytest

from arrangeit.mouse import Mouse


class TestMouse(object):
    """Testing class for base Controller class' domain logic methods."""


    ## Mouse
    @pytest.mark.parametrize(
        "attr",
        [
            "queue",
            "listener",
        ],
    )
    def test_Mouse_inits_attr_as_None(self, attr):
        assert getattr(Mouse, attr) is None

    ## Mouse.__init__
    def test_Mouse_init_instantiates_Queue(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue")
        Mouse()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Mouse_init_sets_queue_attribute(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue")
        assert Mouse().queue == mocked.return_value

    ## Mouse.cursor_position
    def test_Mouse_cursor_position_initializes_Controller(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Controller")
        Mouse().cursor_position()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Mouse_cursor_position_returns_position(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Controller")
        returned = Mouse().cursor_position()
        assert returned == mocked.return_value.position

    ## Mouse.get_item
    def test_Mouse_get_item_calls_queue_get(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue.get")
        Mouse().get_item()
        mocked.assert_called_once()
        mocked.assert_called_with(block=False)

    def test_Mouse_get_item_returns_item(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue.get")
        returned = Mouse().get_item()
        assert returned == mocked.return_value

    def test_Mouse_get_item_returns_None_for_Empty(self, mocker):
        assert Mouse().get_item() is None

    ## Mouse.move_cursor
    def test_Mouse_move_cursor_initializes_Controller(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Controller")
        Mouse().move_cursor(0, 0)
        mocked.assert_called_once()

    def test_Mouse_move_cursor_calls_position_with_provided_x_and_y(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Controller")
        xy = (101, 202)
        Mouse().move_cursor(*xy)
        assert mocked.return_value.position == xy


    ## Mouse.on_move
    def test_Mouse_on_move_puts_in_queue(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue.put")
        mouse = Mouse()
        SAMPLE = (10, 20)
        mouse.on_move(*SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    ## Mouse.on_scroll
    @pytest.mark.parametrize("dy,expected", [
        (-1, False), (1, True)
    ])
    def test_Mouse_on_scroll_puts_in_queue(self, mocker, dy, expected):
        mocked = mocker.patch("arrangeit.mouse.queue.Queue.put")
        mouse = Mouse()
        mouse.on_scroll(0, 0, 0, dy)
        mocked.assert_called_once()
        mocked.assert_called_with(expected)

    ## Mouse.start
    def test_Mouse_start_calls_mouse_Listener(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Listener")
        mouse = Mouse()
        mouse.start()
        mocked.assert_called_once()
        mocked.assert_called_with(on_move=mouse.on_move, on_scroll=mouse.on_scroll)

    def test_Mouse_start_sets_listener_attribute(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Listener")
        mouse = Mouse()
        mouse.start()
        assert mouse.listener == mocked.return_value

    def test_Mouse_start_starts_listener(self, mocker):
        mocked = mocker.patch("arrangeit.mouse.Listener")
        mouse = Mouse()
        mouse.start()
        mocked.return_value.start.assert_called_once()
        mocked.return_value.start.assert_called_with()

    ## Mouse.stop
    def test_Mouse_stop_stops_listener(self, mocker):
        mouse = Mouse()
        mouse.listener = mocker.MagicMock()
        mouse.stop()
        mouse.listener.stop.assert_called_once()
        mouse.listener.stop.assert_called_with()
