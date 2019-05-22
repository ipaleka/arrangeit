import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with GNU/Linux specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def move_and_resize(self, wid):
        """Moves and resizes window having provided wid.

        Gravity stays the same (Wnck.WindowGravity.CURRENT) and the other arguments
        are calculated/retrieved from model where `changed` attribute holds needed data.

        :var model: window data
        :type model: :class:`WindowModel` instance
        :var mask: combination of bits holding information what is changed
        :type mask: :class:`Wnck.WindowMoveResizeMask` flag
        :var win: window instance
        :type win: :class:`Wnck.Window` object
        """
        model = await self.collector.collection.get_model_by_wid(wid)
        mask = await self.collector.get_window_move_resize_mask(model)
        win = await self.collector.get_window_by_wid(wid)
        return win.set_geometry(Wnck.WindowGravity.CURRENT, mask, *model.changed)

    async def move(self, wid):
        """Just calls `move_and_resize` as the same method moves and resizes

        in Wnck.Window class under GNU/Linux.
        """
        return await self.move_and_resize(wid)
