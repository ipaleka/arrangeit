import json
import logging
import os
import queue
import sys

import pynput

from arrangeit.data import WindowModel, WindowsCollection
from arrangeit.settings import MESSAGES, Settings
from arrangeit.utils import (
    Rectangle,
    check_intersections,
    get_component_class,
    get_snapping_sources_for_rect,
    offset_for_intersections,
    platform_user_data_path,
    quarter_by_smaller,
)
from arrangeit.view import ViewApplication, get_screenshot_widget, get_tkinter_root


class BaseApp(object):
    """Base App class holding common code for all the platforms.

    :var BaseApp.controller: object that connects data and presentation
    :type BaseApp.controller: type(:class:`BaseController`) instance (platform specific)
    :var BaseApp.collector: object responsible for collecting windows data
    :type BaseApp.collector: type(:class:`BaseCollector`) instance (platform specific)
    """

    controller = None
    collector = None

    def __init__(self, *args, **kwargs):
        """Instantiates platform specific Controller and Collector classes."""
        self.controller = self.setup_controller()(self)
        self.collector = self.setup_collector()()

    ## SETUP
    def setup_controller(self):
        """Returns platform specific Controller class."""
        return get_component_class("Controller")

    def setup_collector(self):
        """Returns platform specific Collector class."""
        return get_component_class("Collector")

    ## DOMAIN LOGIC
    def run(self):
        """Collects data, prepare them for view and finally shows view application."""
        self.collector.run()
        self.controller.run(self.collector.collection.generator())

    def run_task(self, task, *args):
        """Runs provided task with provided args

        :param task: task name
        :type task: str
        """
        return getattr(self, task)(*args)

    ## TASKS
    def activate_root(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def change_setting(self, name="", value=None):
        """Changes provided setting name to provided value

        and saves it to user settings file.

        If name startswith _ it means we want to change theme part,
        so it calls and returns `change_settings_color_group`.

        :param name: setting name to save
        :type name: str
        :param value: setting value to save
        :type value: int/float/str
        """
        if name.startswith("_"):
            return self.change_settings_color_group(name, value)

        if not Settings.is_setting(name, value):
            return True

        setattr(Settings, name, value)
        logging.info("Settings {} changed.".format(name))
        return self._save_setting([name], value)

    def change_settings_color_group(self, group="", value=None):
        """Changes values for all settings ending with provided `group`

        and saves them to user settings file.

        :param group: settings group to save
        :type group: str
        :param value: setting value to save
        :type value: int/float/str
        """
        group = Settings.color_group(group)
        for name in group:
            setattr(Settings, name, value)
        return self._save_setting(group, value)

    def move(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def move_and_resize(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def move_to_workspace(self, *args):
        """Method must be overridden."""
        raise NotImplementedError

    def rerun_from_window(self, wid, remove_before):
        """Restart positioning routine from the window with provided wid

        without already positioned/skipped windows.

        :param wid: windows identifier
        :type wid: int
        """
        self.collector.collection.repopulate_for_wid(wid, remove_before)

    def save_default(self, *args):
        """Saves collection to default filename in user's directory.

        Creates application's user data directory if it not exists.
        """
        logging.info(MESSAGES["default_saved"])
        directory = platform_user_data_path()
        if not os.path.exists(directory):
            os.mkdir(directory)

        with open(os.path.join(directory, "default.json"), "w") as default:
            json.dump(self.collector.collection.export(), default)

    ## COMMANDS
    def _save_setting(self, names, value):
        """Saves user settings with provided names with provided value
        into user settings file.

        :param names: collection of settings names
        :type names: list
        :param value: setting value to save
        :type name: int/float/str
        """
        directory = platform_user_data_path()
        if not os.path.exists(directory):
            os.mkdir(directory)

        settings_file = os.path.join(directory, "user_settings.json")
        data = {}
        if os.path.exists(settings_file):
            with open(settings_file, "r") as json_settings:
                try:
                    data = json.load(json_settings)
                except json.JSONDecodeError:
                    pass

        data.update(**{name: value for name in names})

        with open(settings_file, "w") as json_settings:
            json.dump(data, json_settings)

        return False

    def _initialize_snapping_sources(self):
        """Creates and returns dictionary with all workspaces numbers as keys

        and all monitors snapping rects as values.

        :returns: dict
        """
        monitors_snapping_rects = [
            get_snapping_sources_for_rect(rect, Settings.SNAP_PIXELS)
            for rect in self.collector.get_monitors_rects()
        ]
        return {
            workspace[0]: monitors_snapping_rects
            for workspace in self.collector.get_available_workspaces()
        }

    def create_snapping_sources(self, for_model):
        """Returns collection of snapping rectangless grouped by workspace.

        Snapping rectangle is created around window connected edge points pair with
        height (or width) of 2*SNAP_PIXELS and width (or height) of related window side.
        Snapping rects for all available monitors are created for each workspace.

        :param for_model: current model
        :type for_model: :class:`WindowModel`
        :returns: dict (int: list of four-tuples)
        """
        sources = self._initialize_snapping_sources()

        for model in list(self.collector.collection.generator()):
            if model == for_model and not Settings.SNAP_INCLUDE_SELF:
                continue

            ws = model.changed_ws if model.is_ws_changed else model.ws
            sources[ws].append(
                get_snapping_sources_for_rect(
                    (
                        model.changed_x,
                        model.changed_y,
                        model.changed_w,
                        model.changed_h,
                    ),
                    Settings.SNAP_PIXELS,
                )
            )
        return sources

    def grab_window_screen(self, model):
        """Method must be overridden."""
        raise NotImplementedError


class BaseController(object):
    """Base Controller class holding common code for all the platforms.

    :var BaseController.app: platform specific parent app
    :type BaseController.app: type(:class:`BaseApp`) instance
    :var model: model holding window data
    :type model: :class:`WindowModel` instance
    :var BaseController.generator: generator for retrieving model instances from collection
    :type BaseController.generator: Generator[WindowModel, None, None]
    :var BaseController.view: Tkinter application showing main window
    :type BaseController.view: :class:`ViewApplication` instance
    :var BaseController.mouse: class responsible for mouse events and queuw
    :type BaseController.mouse: :class:`BaseMouse`
    :var state: controller's state (LOCATE+0..3, RESIZE+0..3 or OTHER)
    :type state: int
    :var default_size: available screen size (width, height)
    :type default_size: (int, int)
    :var screenshot_widget: widget holding background image
    :type screenshot_widget: :class:`tk.Label`
    :var screenshot: screenshot image of the window model
    :type screenshot: :class:`tk.PhotoImage`
    :var snapping_targets: dictionary of snapping rectangles grouped by workspace number
    :type snapping_targets: dict
    """

    app = None
    model = None
    generator = None
    view = None
    mouse = None
    state = None
    default_size = None
    screenshot_widget = None
    screenshot = None
    snapping_targets = None

    def __init__(self, app):
        """Sets app attribute to provided argument, model attribute to new empty model

        and calls :func:`BaseController.setup`.
        """
        self.app = app
        self.model = WindowModel()
        self.mouse = BaseMouse()
        self.setup()

    ## CONFIGURATION
    def setup(self):
        """Initializes Tkinter ViewApplication with root window and self as arguments.

        Creates and place screenshot widget below view frame, used to hold window image.
        Sets view attribute to newly created Tkinter application.
        Temporary hides root window.
        Tkinter root window from now may be accessed by `[self].view.master` attribute.
        """
        root = get_tkinter_root()
        self.setup_root_window(root)
        self.screenshot_widget = get_screenshot_widget(root)
        self.view = ViewApplication(master=root, controller=self)
        self.view.hide_root()

    def setup_root_window(self, root):
        """Sets provided root window appearance common for all platforms.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        """
        if Settings.TRANSPARENCY_IS_ON:
            root.wm_attributes("-alpha", Settings.ROOT_ALPHA)

        root.wm_attributes("-topmost", True)
        root.config(background=Settings.MAIN_BG)

    def set_default_geometry(self, root):
        """Sets provided root window width and height

        calculated from available width and height for screen as quarter of
        the smaller element. Returned width and height have 16:9 aspect ratio.

        :param root: root tkinter window
        :type root: :class:`tkinter.Tk` instance
        :var width: root width in pixels
        :type width: int
        :var height: root height in pixels
        :type height: int
        """
        if self.default_size is None:
            width, height = quarter_by_smaller(
                *self.app.collector.get_smallest_monitor_size()
            )
            self.default_size = (width, height)
        root.geometry("{}x{}".format(*self.default_size))

    def prepare_view(self):
        """Populates view's workspaces and windows list widgets.

        Very first window is our main window so we skip it in listing.
        """
        self.view.workspaces.add_workspaces(
            self.app.collector.get_available_workspaces()
        )
        self.view.windows.add_windows(
            self.app.collector.collection.get_windows_list()[1:]
        )

    def set_screenshot(self):
        """Creates and places screenshot of model window as background image.

        If we can't include window decoration in image then offset is returned
        and we place image shifted by offset amount of pixels to related axis.

        :var offset: offset (x, y)
        :type offset: (int, int)
        """
        self.screenshot, offset = self.app.grab_window_screen(self.model)
        self.screenshot_widget.config(image=self.screenshot)
        self.screenshot_widget.place(
            x=offset[0] + Settings.SCREENSHOT_SHIFT_PIXELS,
            y=offset[1] + Settings.SCREENSHOT_SHIFT_PIXELS,
        )

    ## PROPERTIES
    @property
    def resizing_state_counterpart(self):
        """Returns resizing state counterpart of current positioning state."""
        return Settings.RESIZE + (self.state + 2) % 4

    ## DOMAIN LOGIC
    def apply_snapping(self, new_x, new_y, sources, intersections):
        """Moves cursor and sets new state and corner if snapping occured on new side.

        State and corner can change only for positioning phase, so for resizing phase
        this function calls and returns `move_cursor` at the very beginning.

        :param new_x: new cursor position on x-axis
        :type new_x: int
        :param new_y: new cursor position on y-axis
        :type new_y: int
        :param sources: four-tuple of root window snapping rectangles
        :type sources: tuple of :class:`Rectangle`
        :param intersections: one or two pairs of snapping rectangles that intersect
        :type intersections: tuple
        :var new_state: positioning state
        :type new_state: int
        :var index0: position of root's first intersected snapping rectangle in sources
        :type index0: int
        :var index1: position of root's second intersected snapping rectangle in sources
        :type index1: int
        """
        if not self.state < Settings.RESIZE:
            return self.mouse.move_cursor(new_x, new_y)

        new_state = self.state

        if isinstance(intersections[0], Rectangle):  # single axis snap
            index0 = sources.index(intersections[0])
            if not index0 in Settings.CORNER_RECT_INDEXES[self.state]:
                new_state = Settings.CORNER_RECT_INDEXES.index(
                    (Settings.CORNER_RECT_INDEXES[self.state][0], index0)
                    if index0 % 2
                    else (index0, Settings.CORNER_RECT_INDEXES[self.state][1])
                )

        else:  # both axes snapped
            index0 = sources.index(intersections[0][0])
            index1 = sources.index(intersections[1][0])
            if Settings.CORNER_RECT_INDEXES[self.state] != (index0, index1):
                new_state = Settings.CORNER_RECT_INDEXES.index((index0, index1))

        if new_state != self.state:
            if new_state in (1, 2) and self.state in (0, 3):
                new_x += self.view.master.winfo_width() - 2 * Settings.SHIFT_CURSOR
            elif new_state in (0, 3) and self.state in (1, 2):
                new_x -= self.view.master.winfo_width() - 2 * Settings.SHIFT_CURSOR

            if new_state in (2, 3) and self.state in (0, 1):
                new_y += self.view.master.winfo_height() - 2 * Settings.SHIFT_CURSOR
            elif new_state in (0, 1) and self.state in (2, 3):
                new_y -= self.view.master.winfo_height() - 2 * Settings.SHIFT_CURSOR
            self.state = new_state
            self.setup_corner()

        self.mouse.move_cursor(new_x, new_y)

    def check_snapping(self, x, y):
        """Snaps root window and returns True if root window intersects

        with any collection window according to snapping rects in current workspace
        or returns False if no snapping has occurred.

        Calls `apply_snapping` to change state and corner if snapping occurs on
        different corner that current state/corner.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        :var sources: four-tuple of root window snapping rectangles
        :type sources: tuple of :class:`Rectangle`
        :var intersections: one or two pairs of snapping rectangles that intersect
        :type intersections: tuple
        :var offset: offset for axes
        :type offset: tuple
        :returns: Boolean
        """
        if Settings.SNAPPING_IS_ON:

            sources = get_snapping_sources_for_rect(
                self.get_root_rect(x, y),
                Settings.SNAP_PIXELS,
                corner=None if self.state < Settings.RESIZE else self.state % 10,
            )
            intersections = check_intersections(
                sources, self.snapping_targets[self.view.workspaces.active]
            )
            offset = offset_for_intersections(intersections, Settings.SNAP_PIXELS)

            if offset and offset != (0, 0):
                self.apply_snapping(
                    x + offset[0], y + offset[1], sources, intersections
                )
                return True

        return False

    def listed_window_activated(self, wid):
        """Calls task that restarts positioning routine from provided window id

        not including windows prior to current model.

        :param wid: windows identifier
        :type wid: int
        """
        self.app.run_task("rerun_from_window", wid, self.model.wid)
        self.view.windows.clear_list()
        self.view.windows.add_windows(
            self.app.collector.collection.get_windows_list()[1:]
        )
        if self.state == Settings.OTHER:
            self.recapture_mouse()
        self.generator = self.app.collector.collection.generator()
        self.next(first_time=True)

    def next(self, first_time=False):
        """Sets controller ``model`` attribute from the value yielded from ``generator``

        and populates view widgets with new model data.

        Sets program to be in positioning phase by setting LOCATE state.
        Also changes and moves cursor and root window to model's window position.
        Grabs and sets screenshot image of the model's window.
        If there are no values left in collection then saves and exits app.
        Switches workspace if it's changed.

        :var old_workspace: old model's workspace number
        :type old_workspace: ind
        :var first_time: is method called for the very first time
        :type first_time: Boolean
        :returns: Boolean
        """
        self.state = Settings.LOCATE

        old_workspace = self.model.changed_ws or self.model.workspace
        try:
            self.model = next(self.generator)
        except StopIteration:
            if Settings.SAVE_ON_EXIT:
                self.save()
            self.shutdown()
            return True

        if not first_time:
            self.remove_listed_window(self.model.wid)
            if self.model.workspace != old_workspace:
                self.switch_workspace()

        self.set_screenshot()
        self.snapping_targets = self.app.create_snapping_sources(self.model)
        self.set_default_geometry(self.view.master)
        self.view.update_widgets(self.model)
        self.place_on_top_left()
        if first_time:
            self.view.master.geometry(
                "+{}+{}".format(
                    *self.get_root_rect(
                        self.model.x + Settings.SHIFT_CURSOR,
                        self.model.y + Settings.SHIFT_CURSOR,
                    )[:2]
                )
            )
        return False

    def run(self, generator):
        """Prepares view, syncs data, starts mouse listener and enters main loop.

        Calls `prepare_view` to create workspaces and windows list widgets.
        Sets generator attribute to provided generator and sets window data
        by calling :func:`BaseController.next` for the first time.
        Calls view application startup routine to show root and calculate
        visible parameters.
        Also brings global focus to root window.
        """
        self.prepare_view()

        self.generator = generator
        self.next(first_time=True)

        self.mouse.start()

        self.view.startup()

        self.app.run_task("activate_root", self.view.master.winfo_id())

        self.mainloop()

    def update(self, x, y):
        """Calls corresponding state related update method.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        """
        if self.state < Settings.RESIZE:  # implies LOCATE
            return self.update_positioning(x, y)

        elif self.state < Settings.OTHER:  # implies RESIZE
            return self.update_resizing(x, y)

    def update_positioning(self, x, y):
        """Updates model with provided cursor position in LOCATE state

        and takes action in regard to model type.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        """
        self.model.set_changed(
            x=x + (1 if self.state % 3 else -1) * Settings.SHIFT_CURSOR,
            y=y + (1 if self.state // 2 else -1) * Settings.SHIFT_CURSOR,
        )
        if not self.model.resizable:
            if self.model.changed or self.model.is_ws_changed:
                self.app.run_task("move", self.model.wid)
            self.next()
        else:
            self.state = self.resizing_state_counterpart
            self.place_on_opposite_corner()

    def update_resizing(self, x, y):
        """Updates model related to provided cursor position and current root size

        and calls move and resize task if window has changed.

        Switches to next model anyway.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        :var params: rect attributes we're going to change
        :type params: dict
        """
        params = {
            "w": self.view.master.winfo_width(),
            "h": self.view.master.winfo_height(),
            "x": x - Settings.SHIFT_CURSOR,
            "y": y - Settings.SHIFT_CURSOR,
        }

        if (self.state % 10) % 3:
            del params["x"]
        if (self.state % 10) // 2:
            del params["y"]

        self.model.set_changed(**params)

        if self.model.changed or self.model.is_ws_changed:
            self.app.run_task("move_and_resize", self.model.wid)
        self.next()

    def workspace_activated(self, number):
        """Activates workspace with number equal to provided number.

        :param number: our custom workspace number (screen*1000 + workspace)
        :type number: int
        """
        self.app.run_task("move_to_workspace", self.view.master.winfo_id(), number)
        self.model.set_changed(ws=number)
        if self.state == Settings.OTHER:
            self.recapture_mouse()

    ## COMMANDS
    def change_position(self, x, y):
        """Changes root window position to provided x and y

        if snapping criteria is not satisfied.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if self.check_snapping(x, y):
            return True

        self.view.master.geometry("+{}+{}".format(*self.get_root_rect(x, y)[:2]))

    def change_size(self, x, y):
        """Changes root window size in regard to provided current x and y

        related to model's changed x and y if calculated size won't be smaller
        than minimum and if snapping criteria isn't satisfied.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        :var position: eventual position of minimum sized root
        :type position: tuple (int, int)
        :var width: root window calculated width
        :type width: int
        :var height: root window calculated height
        :type height: int
        :var left: root window calculated position on x-axis
        :type left: int
        :var top: root window calculated position on y-axis
        :type top: int
        """
        position = self.check_current_size(x, y)
        if position:
            return self.set_minimum_size(*position)

        if self.check_snapping(x, y):
            return True

        width = min(
            self.model.changed_x - x + Settings.SHIFT_CURSOR, self.model.changed_x
        )
        height = min(
            self.model.changed_y - y + Settings.SHIFT_CURSOR, self.model.changed_y
        )
        left = x - Settings.SHIFT_CURSOR
        top = y - Settings.SHIFT_CURSOR

        if (self.state % 10) // 2:
            height = min(
                y - self.model.changed_y + Settings.SHIFT_CURSOR,
                self.view.master.winfo_screenheight() - self.model.changed_y,
            )
            top = self.model.changed_y

        if (self.state % 10) % 3:
            width = min(
                x - self.model.changed_x + Settings.SHIFT_CURSOR,
                self.view.master.winfo_screenwidth() - self.model.changed_x,
            )
            left = self.model.changed_x

        self.view.master.geometry("{}x{}+{}+{}".format(width, height, left, top))

    def change_setting(self, name, value):
        """Calls task for changing provided settings name to provided value.

        :param name: setting name
        :type name: str
        :param value: value to change the setting to
        :type name: str/int/float
        """
        return self.app.run_task("change_setting", name, value)

    def check_current_size(self, x, y):
        """Returns True if current size in resizing phase is greater than minimum size

        defined in settings.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        :returns: tuple position (int, int) or False
        """
        check_x = x < self.model.changed_x - Settings.MIN_WIDTH + Settings.SHIFT_CURSOR
        check_y = y < self.model.changed_y - Settings.MIN_HEIGHT + Settings.SHIFT_CURSOR
        left = self.model.changed_x - Settings.MIN_WIDTH
        top = self.model.changed_y - Settings.MIN_HEIGHT

        if (self.state % 10) % 3:
            check_x = (
                x > self.model.changed_x + Settings.MIN_WIDTH - Settings.SHIFT_CURSOR
            )
            left = self.model.changed_x

        if (self.state % 10) // 2:
            check_y = (
                y > self.model.changed_y + Settings.MIN_HEIGHT - Settings.SHIFT_CURSOR
            )
            top = self.model.changed_y

        return False if check_x and check_y else (left, top)

    def cycle_corners(self, counter=False):
        """Cycle through corners in positioning phase by changing state."""
        if self.state < Settings.RESIZE:  # implies LOCATE
            if not counter:
                self.state = self.state + 1 if (self.state + 1) % 4 != 0 else 0
            else:
                self.state = self.state - 1 if self.state > 0 else 3
            self.move_to_corner()

    def get_root_rect(self, x, y):
        """Returns current root position and size calculated from provided x, y.

        :param x: current horizontal axis mouse position in pixels
        :type x: int
        :param y: current vertical axis mouse position in pixels
        :type y: int
        :returns: (int, int, int, int)
        """
        left, top, width, height = (
            x - Settings.SHIFT_CURSOR,
            y - Settings.SHIFT_CURSOR,
            self.view.master.winfo_width(),
            self.view.master.winfo_height(),
        )
        if (self.state % 10) % 3:  # 1 and 2 have different new_x
            left -= width - 2 * Settings.SHIFT_CURSOR
        if (self.state % 10) // 2:  # 2 and 3 have different new_y
            top -= height - 2 * Settings.SHIFT_CURSOR

        return (left, top, width, height)

    def listed_window_activated_by_digit(self, number):
        """Activates listed window by its ordinal in list presented by provided number.

        :param number: number of 1 to 16 representing ordinal in list
        :type number: int
        :var windows: available workspaces in view
        :type windows: :class:`WorkspacesCollection`
        """
        windows = self.view.windows.winfo_children()
        if len(windows) >= number:
            self.listed_window_activated(windows[number - 1].wid)

    def mouse_move(self, x, y):
        """Moves root Tkinter window to provided mouse coordinates.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        if self.state < Settings.RESIZE:
            self.change_position(x, y)

        elif self.state < Settings.OTHER:
            self.change_size(x, y)

    def mouse_scroll(self, counter=False):
        """Cycles through window corners in both directions.

        :param counter: is scroll in counter direction
        :type counter: Boolean
        """
        self.cycle_corners(counter=counter)

    def move_to_corner(self):
        """Configures mouse pointer and moves cursor to calculated corner position.

        :var x: absolute horizontal axis mouse position in pixels
        :type x: int
        :var y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        x = self.view.master.winfo_x() + Settings.SHIFT_CURSOR
        y = self.view.master.winfo_y() + Settings.SHIFT_CURSOR

        if self.state % 3:
            x += self.view.master.winfo_width() - 2 * Settings.SHIFT_CURSOR

        if self.state // 2:
            y += self.view.master.winfo_height() - 2 * Settings.SHIFT_CURSOR

        self.mouse.move_cursor(x, y)
        self.setup_corner()

    def place_on_top_left(self):
        """Moves cursor to model's top left position and setups that corner

        widget and cursor.
        """
        self.mouse.move_cursor(
            self.model.x + Settings.SHIFT_CURSOR, self.model.y + Settings.SHIFT_CURSOR
        )
        self.setup_corner()

    def place_on_opposite_corner(self):
        """Changes and moves cursor to model windows corner opposite to positioning phase

        and so triggers master resizing.

        :var left: x-axis part of the cursor position
        :type left: int
        :var top: y-axis part of the cursor position
        :type top: int
        """
        left = max(self.model.changed_x - self.model.w, 0) + Settings.SHIFT_CURSOR
        top = max(self.model.changed_y - self.model.h, 0) + Settings.SHIFT_CURSOR

        if (self.state % 10) // 2:
            top = (
                min(
                    self.model.changed_y + self.model.h,
                    self.view.master.winfo_screenheight(),
                )
                - Settings.SHIFT_CURSOR
            )
        if (self.state % 10) % 3:
            left = (
                min(
                    self.model.changed_x + self.model.w,
                    self.view.master.winfo_screenwidth(),
                )
                - Settings.SHIFT_CURSOR
            )

        self.mouse.move_cursor(left, top)
        self.setup_corner()

    def remove_listed_window(self, wid):
        """Destroys window widget from windows list and refreshes the list afterward.

        :param wid: id of window that will be destroyed
        :type wid: int
        """
        try:
            next(
                widget
                for widget in self.view.windows.winfo_children()
                if widget.wid == wid
            ).destroy()
        except StopIteration:
            pass
        self.view.windows.place_children()

    def release_mouse(self):
        """Stops positioning/resizing routine and releases mouse."""
        self.view.reset_bindings()
        self.view.master.config(cursor="left_ptr")
        self.view.corner.hide_corner()
        self.state = Settings.OTHER
        self.mouse.stop()

    def recapture_mouse(self):
        """Starts mouse listener and positioning/resizing routine."""
        self.view.setup_bindings()
        self.state = Settings.LOCATE
        self.set_default_geometry(self.view.master)
        self.mouse.move_cursor(
            self.view.master.winfo_x() + Settings.SHIFT_CURSOR,
            self.view.master.winfo_y() + Settings.SHIFT_CURSOR,
        )
        self.setup_corner()
        self.mouse.start()

    def save(self):
        """Runs task for saving windows collection data to default file."""
        self.app.run_task("save_default")

    def shutdown(self):
        """Stops mouse listener, destroys Tkinter root window and exits."""
        self.mouse.stop()
        self.view.master.destroy()
        sys.exit(0)

    def setup_corner(self):
        """Configures mouse pointer and background to current corner."""
        self.view.master.config(cursor=Settings.CORNER_CURSOR[self.state % 10])
        self.view.corner.set_corner(self.state % 10)

    def set_minimum_size(self, x, y):
        """Sets root window size to minimum size defined in settings

        and places root's top left position to (x, y).

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        self.view.master.geometry(
            "{}x{}+{}+{}".format(Settings.MIN_WIDTH, Settings.MIN_HEIGHT, x, y)
        )

    def skip_current_window(self):
        """Calls `next` and then destroys that new window from the windows list."""
        self.model.clear_changed()
        self.next()

    def switch_workspace(self):
        """Activates workspace and moves root window onto it."""
        self.app.run_task(
            "move_to_workspace", self.view.master.winfo_id(), self.model.workspace
        )

    def switch_resizable(self):
        """Changes current model resizable Boolean value and updates view."""
        self.model.resizable = not self.model.resizable
        self.view.resizable.set_value(self.model.resizable)

    def switch_restored(self):
        """Changes current model restored Boolean value and updates view."""
        self.model.restored = not self.model.restored
        self.view.restored.set_value(self.model.restored)

    def workspace_activated_by_digit(self, number):
        """Activates workspace with humanized number equal to provided number.

        :param number: number of 1 to 9 representing workspace
        :type number: int
        :var workspaces: available workspaces in view
        :type workspaces: :class:`WorkspacesCollection`
        """
        workspaces = self.view.workspaces.winfo_children()
        if len(workspaces) >= number:
            self.workspace_activated(workspaces[number - 1].number)

    ## EVENTS CALLBACKS
    def on_key_pressed(self, event):
        """Calls method related to pressed key.

        :param event: catched event
        :type event: Tkinter event
        """
        if event.keysym in ("Escape",):
            self.shutdown()

        elif event.keysym in ("Return", "KP_Enter"):
            self.update(*self.mouse.cursor_position())

        elif event.keysym in ("space", "Tab"):
            self.skip_current_window()

        elif event.keysym in ("R", "r"):
            self.switch_resizable()

        elif event.keysym in ("M", "m"):
            self.switch_restored()

        elif event.keysym in ("Alt_L", "Alt_R", "Shift_L", "Shift_R"):
            self.release_mouse()

        elif event.keysym in ("Control_L", "Control_R"):
            self.cycle_corners()

        elif event.keysym in [str(i) for i in range(1, 10)]:
            self.workspace_activated_by_digit(int(event.keysym))

        elif event.keysym in ["KP_{}".format(i) for i in range(1, 10)]:
            self.workspace_activated_by_digit(int(event.keysym[-1]))

        elif event.keysym in ["F{}".format(i) for i in range(1, 17)]:
            self.listed_window_activated_by_digit(int(event.keysym[1:]))

        return "break"

    def on_mouse_left_down(self, event):
        """Calls :class:`BaseController.update` with current cursor position

        :param event: catched event
        :type event: Tkinter event
        """
        self.update(*self.mouse.cursor_position())
        return "break"

    def on_mouse_middle_down(self, event):
        """Switches to third state.

        :param event: catched event
        :type event: Tkinter event
        """
        self.release_mouse()
        return "break"

    def on_mouse_right_down(self, event):
        """Skips the current model.

        :param event: catched event
        :type event: Tkinter event
        """
        self.skip_current_window()
        return "break"

    def on_continue(self, event):
        """Restarts positioning routine."""
        self.recapture_mouse()
        return "break"

    def on_focus(self, event):
        """Calls task top activate root if Tkinter has lost focus."""
        if self.view.focus_get() is None:
            self.app.run_task("activate_root", self.view.master.winfo_id())
            return "break"

    def on_resizable_change(self, event):
        """Switches model resizable attribute."""
        self.switch_resizable()
        self.recapture_mouse()
        return "break"

    def on_restored_change(self, event):
        """Switches model restored attribute."""
        self.switch_restored()
        self.recapture_mouse()
        return "break"

    ## MAIN LOOPS
    def check_mouse(self):
        """Runs method that corresponds to retrieved item from mouse queue.

        There are only two possibilities for item type: Boolean (scroll direction)
        or tuple (mouse position).

        Method calls itself in regular interval defined in settings.
        """
        while True:
            item = self.mouse.get_item()
            if item is None:
                break
            elif isinstance(item, bool):
                self.view.master.after_idle(self.mouse_scroll, item)
            else:
                self.view.master.after_idle(self.mouse_move, *item)

        self.view.master.after(Settings.MOUSE_CHECK_INTERVAL, self.check_mouse)

    def mainloop(self):
        """Tkinter main loop."""
        self.view.master.after(Settings.MOUSE_CHECK_INTERVAL, self.check_mouse)
        self.view.mainloop()


class BaseCollector(object):
    """Base Collector class holding common code for all the platforms.

    :var collection: collection of :class:`WindowModel` instances
    :type collection: :class:`WindowsCollection` instance
    """

    collection = None

    def __init__(self):
        """Initiates ``collection`` as empty :class:`WindowsCollection` instance."""
        self.collection = WindowsCollection()

    def is_applicable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def is_valid_state(self, window_type, window_state):
        """Method must be overridden."""
        raise NotImplementedError

    def is_resizable(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def is_restored(self, window_type):
        """Method must be overridden."""
        raise NotImplementedError

    def get_windows(self):
        """Method must be overridden."""
        raise NotImplementedError

    def check_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def add_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def get_workspace_number(self, workspace):
        """Method must be overridden."""
        raise NotImplementedError

    def get_workspace_number_for_window(self, win):
        """Method must be overridden."""
        raise NotImplementedError

    def get_available_workspaces(self):
        """Method must be overridden."""
        raise NotImplementedError

    def get_monitors_rects(self):
        """Method must be overridden."""
        raise NotImplementedError

    def get_smallest_monitor_size(self):
        """Returns size of the smallest monitor.

        :returns: tuple (w,h)
        """
        return min((rect[2], rect[3]) for rect in self.get_monitors_rects())

    def run(self):
        """Populates ``collection`` with WindowModel instances

        created from the windows list provided by :func:`get_windows`
        after they are checked for compliance with :func:`check_window`
        by calling :func:`add_window`.


        :var win: current window instance/handle in the loop
        :type win: platform specific window object or handle (Wnck.Window, hwnd, ...)
        """
        for win in self.get_windows():
            if self.check_window(win):
                self.add_window(win)
        win = None
        self.collection.sort()


class BaseMouse(object):
    """Class responsible for listening and controlling system-wide mouse events.

    :var queue: mouse events queue
    :type queue: :class:`queue.Queue`
    :var listener: class as separate thread listening for mouse events
    :type listener: :class:`pynput.mouse.Listener`
    :var control: class for retrieving and setting cursor position
    :type control: :class:`pynput.mouse.Controller`
    """

    queue = None
    listener = None
    control = None

    def __init__(self):
        """Instatiates and sets queue."""
        self.queue = queue.Queue()
        self.control = pynput.mouse.Controller()

    def cursor_position(self):
        """Returns current cursor position.

        :returns: (int, int)
        """
        return self.control.position

    def get_item(self):
        """Gets next item in queue and returns it.

        :returns: (x,y) or bool or None
        """
        try:
            return self.queue.get(block=False)
        except queue.Empty:
            return None

    def move_cursor(self, x, y):
        """Moves cursor position to a point defined by provided x and y."""
        self.control.position = (x, y)

    def on_move(self, x, y):
        """Puts provided x and y in queue as position tuple.

        NOTE: int(x) and int(y) are needed for Darwin - making a specific
        platform mouse module just for that is avoided.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        """
        self.queue.put((int(x), int(y)))

    def on_scroll(self, x, y, dx, dy):
        """Puts scroll direction as Boolean value in queue.

        We are interested only in in dy that holds either +1 or -1 value, so we
        converted that to Boolean value.

        :param x: absolute horizontal axis mouse position in pixels
        :type x: int
        :param y: absolute vertical axis mouse position in pixels
        :type y: int
        :param dx: scroll vector on x axis
        :type dx: int
        :param dy: scroll vector on y axis
        :type dy: int
        """
        self.queue.put(dy > 0)

    def start(self):
        """Initializes and starts listener for move and scroll events."""
        self.listener = pynput.mouse.Listener(
            on_move=self.on_move, on_scroll=self.on_scroll
        )
        self.listener.start()

    def stop(self):
        """Stops listener by raising an exception."""
        try:
            raise pynput.mouse.Listener.StopException
        except pynput.mouse.Listener.StopException:
            return
