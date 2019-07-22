User guide
==========

Basic principles
----------------

**arrangeit** collects all the available open windows and puts them in queue for
operation. Ending operation on the current window is followed by starting operation
on the next window in queue. **arrangeit v0.3alpha** ends its execution after all
the windows are exhausted and it should be started again for additional operations.


User interface
--------------

A box with the title of currently operating window occupies top-left position of the
main window. That window's application name and icon are placed at the top-right.

The other windows in queue are placed below the title box, in the order in which
**arrangeit** will operate on them.

Workspaces boxes are placed on the right side of the listed windows, with the
emphasized color for the current window workspace.

The status bar for displaying software messages is placed at the bottom of the
main window.

Quit button and the button bringing options dialog (some basic program settings may
be changed from there) are at the bottom-right of the main window.


Main operations
---------------

The default state of the program is its operational state. It means that moving mouse
cursor automatically moves the main window. That is the positioning phase of the
software in which you're choosing the future position on the screen for the current
window.

You switch to resizing phase by pressing the left button of the mouse. There will be
no resizing phase for a fixed size window, so a left click will switch to the
positioning phase of the next window in the queue.

Click the middle mouse button or press **Shift** key on keyboard to release the mouse.
That will stop positioning/resizing phase and the other functionalities of the
software will be allowed instead of the main operations of windows positioning and
resizing.


Positioning phase
^^^^^^^^^^^^^^^^^

snapping, cycle corners, clicking/shift


Resizing phase
^^^^^^^^^^^^^^
snapping, if you are not satisfied, releasing and clicking tjhe titrle/icon resets to the positioning phase



Other operations
----------------

You access other operations either by keyboard shortcuts or by releasing the mouse
cursor and use it to select some other functionality beside positioning/resizing.


Changing window properties
^^^^^^^^^^^^^^^^^^^^^^^^^^

If the current window is a fixed size window, then there would be no resizing phase
after left click - it will be immediately placed and the positioning phase for the
next window in queue will start afterward.

You may change that default behaviour by clicking |resizable| in the window title
box. It works other way around too: if you click |fixed| for resizable window, then
it will be just placed after positioning phase like it was a fixed size window.

A similar behavior is applicable for restored/minimized windows too: currently
minimized window will be restored after resizing phase if you click |restore|, and
currently restored window will be minimized if you click |minimize|.

.. |resizable| image:: ./_static/resize.png
.. |fixed| image:: ./_static/move.png
.. |restore| image:: ./_static/restore.png
.. |minimize| image:: ./_static/minimize.png




Keyboard shortcuts
------------------

Enter
^^^^^

Confirms position or size - acts identically as left mouse click.


Space
^^^^^

Skips current window - just like the right mouse click does.


subheader
"""""""""


If a window is pinned (visible in all workspaces) then if you change workspace
during positioning you will unpin that window and so make it visible in the
selected workspace only.
