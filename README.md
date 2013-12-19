Optistatus
==========

What is it for?

Optistatus is a little applet for the taskbar
that shows if the NVIDIA-Optimus-Card is running.

Does it work with primusrun?

Yes, because it checks the status of /proc/acpi/bbswitch, which
shows if the cards is on or not, regardless if you use
optirun or primusrun for launching your app

Bugs

There shouldn't be any...at least i hope so.
Right now I still have the small problem,
that wxwidget uses the system-theme-panel-background as icon background
on my lxpanel. So if you turn on panel transparency, it will look
rather weird.
