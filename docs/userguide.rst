User guide
==========

Basic principles
----------------

**arrangeit** collects all the available open windows and puts them in a queue for
operation. Ending operation on the current window is followed by starting operation
on the next window in the queue. **arrangeit v0.3alpha** ends its execution after all
the windows are exhausted and it should be started again for additional operations.


User interface
--------------

A box with the title of currently operating window occupies the top-left position of
the main window. That window's application name and icon are placed at the top-right.

The other windows in the queue are placed below the title box, in the order in which
**arrangeit** will operate on them.

Workspaces boxes are placed on the right side of the listed windows, with the
emphasized color for the current window workspace.

The status bar for displaying software messages is placed at the bottom of the
main window.

Quit button and the button bringing options dialog (some basic program settings may
be changed from there) are at the bottom-right of the main window.


Main operations
---------------

The default state of the program is its operational state. It means that moving the
mouse cursor automatically moves the main window. That is the positioning phase of the
software in which you're choosing the future position on the screen for the current
window.

You switch to resizing phase by pressing the left button of the mouse. There will be
no resizing phase for a fixed size window, so a left click in such a case will switch
to the positioning phase of the next window in the queue.

Click the middle mouse button or press **Shift** key on your keyboard to release the
mouse. That will stop the positioning/resizing phase and the other functionalities
of the software will be allowed instead.


Positioning phase
^^^^^^^^^^^^^^^^^

As you move your mouse you also move the arrangeit main window. You may set the future
position of the window by pressing the left mouse button or by **Enter** key on your
keyboard. The starting corner of the resizing phase can be picked either by pressing
**Ctrl** key or it can be set automatically by the snapping process.

The main window will snap next to the other windows if it is moved close enough to
them. From the options dialog you may choose a snap distance or you may completely
turn off the snap functionality.

Press the right mouse button or **Space** on keyboard to skip the current window and
start to operate on the next window in the queue.

You may reposition listed windows starting from the desired window by releasing the
mouse and clicking its title in the listed window collection. If you don't want to
release the mouse for the action, you may activate a window by its ordinal number
from the corresponding **F** key (**F1** for the first window in the queue, **F2**
for the second, etc.).

To move current window to another workspace/desktop, click that workspace in the
workspace list after releasing the mouse. Press a related number on your keyboard to
switch to a workspace without releasing the mouse.

When you confirm the position by pressing the left mouse button (or by pressing the
**Enter** key on your keyboard), the resizing phase starts for non-fixed size window.


Resizing phase
^^^^^^^^^^^^^^

Your cursor is positioned at the opposite corner of staring point set in positioning
phase. You are setting the ending corner of the window in resizing phase - just press
the left mouse button when you are ready. You'll be switched to the next window in
the queue afterward, while the previous window will be positioned and resized
based on the actions you did.

Target window background image is shown as the main window background during the
resizing phase. From the options dialog you may set should that image be in
grayscale. you may set the size for the *blur* filter, or you may completely turn off
the background image and set the background to be made from the main background color
instead.

If you release mouse (mouse middle button click or **Shift** on keyboard) then the
resizing phase will be canceled and recapturing the mouse starts from the positioning
phase.


Other operations
----------------

You access other operations either by keyboard shortcuts or by releasing the mouse
cursor and use it to select some other functionality beside positioning/resizing.


Changing window properties
^^^^^^^^^^^^^^^^^^^^^^^^^^

If the current window is a fixed size window, then there would be no resizing phase
after left click - it will be immediately placed and the positioning phase for the
next window in the queue will start afterward.

You may change that default behavior by clicking |resizable| in the window title
box. It works the other way around too: if you click |fixed| for resizable window,
then it will be just placed after positioning phase like it was a fixed size window.

Similar behavior is applicable for restored/minimized windows too: currently
minimized window will be restored after resizing phase if you click |restore|, and
currently restored window will be minimized if you click |minimize|.

.. note::
   In GNU/Linux if a window is pinned (visible in all workspaces) then if you change
   a workspace during the window operation, you will unpin that window and so make it
   visible in the selected workspace only.


Keyboard shortcuts
------------------

======  ===================  =============
 Key    Mouse                Action
        counterpart
======  ===================  =============
Enter   left-click           confirm position
Esc     Quit button          quit program
Space   right-click          skip window
Ctrl    *by snapping*        cycle corner
Shift   middle-click         release mouse
R       resizable icon       turn on/off resizing phase
M       minimize icon        make window minimized/restored
1-9     click workspace      change workspace
F1-F12  click listed window  restart from selected window
======  ===================  =============


Options
-------

You may change some program settings from the options dialog started after you release
the mouse and click the *Options* button at the bottom-right of the main window.

A setting value would be changed and saved immediately after selecting, but some
settings changing require program restart in order to take effect.

.. |resizable| image:: ./_static/resize.png
.. |fixed| image:: ./_static/move.png
.. |restore| image:: ./_static/restore.png
.. |minimize| image:: ./_static/minimize.png
