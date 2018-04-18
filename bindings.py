'''
My mouse and key bindings.

String names for non-alpha-numeric keys can be found here:
>>> https://github.com/qtile/qtile/blob/develop/libqtile/xkeysyms.py

It is possible to bind keys to multiple actions (see the swap panes bindings).
When this is done, all actions are sent and the layout/window/group acts on
those that it knows about and ignores those that it doesn't.
- I've used this to group logical behaviour between layouts where they use
  different method names (in the case of moving windows) and to chain
  actions together (move group to screen and follow with focus).

I'm not being 100% consistent but in general:
    M-...  :: qtile / environment commands
    M-S... :: qtile window/group management commands (movement of windows etc)
    M-C... :: program launching
    M-A... :: utility launching

Anything bound to arrow keys is movement based. I'm having problems binding
`M-C={h,j,k,l}` which is preventing me using that for movement. (Though this
may be something to do with my own ez_keys function...!)
'''
from libqtile.config import Click, Drag, EzKey
from libqtile.command import lazy

from settings import MOD, TERMINAL
from helpers import script
from groups import groups


def switch_screens(target_screen):
    '''Send the current group to the other screen.'''
    @lazy.function
    def _inner(qtile):
        current_group = qtile.screens[1 - target_screen].group
        qtile.screens[target_screen].setGroup(current_group)

    return _inner


def focus_or_switch(group_name):
    '''
    Focus the selected group on the current screen or switch to the other
    screen if the group is currently active there
    '''
    @lazy.function
    def _inner(qtile):
        # Check what groups are currently active
        groups = [s.group.name for s in qtile.screens]

        try:
            # Jump to that screen if we are active
            qtile.toScreen(groups.index(group_name))
        except ValueError:
            # We're not active so pull the group to the current screen
            qtile.currentScreen.setGroup(qtile.groupMap[group_name])

    return _inner


# qtile actually has an emacs style `EzKey` helper that makes specifying
# key bindings a lot nicer than the default.
keys = [EzKey(k[0], *k[1:]) for k in [
    # .: Movement :.
    # Swtich focus between panes
    ("M-<Up>", lazy.layout.up()),
    ("M-<Down>", lazy.layout.down()),
    ("M-<Left>", lazy.layout.left()),
    ("M-<Right>", lazy.layout.right()),

    # Swap panes: target relative to active.
    # NOTE :: The `swap` commands are for XMonad
    ("M-S-<Up>", lazy.layout.shuffle_up()),
    ("M-S-<Down>", lazy.layout.shuffle_down()),
    ("M-S-<Left>", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    ("M-S-<Right>", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    # Grow/shrink the main the focused window
    # NOTE :: grow/shrink for XMonadTall, grow_X for Wmii/BSP
    ("M-C-<Up>", lazy.layout.grow_up()),
    ("M-C-<Down>", lazy.layout.grow_down()),
    ("M-C-<Left>", lazy.layout.grow_left()),
    ("M-C-<Right>", lazy.layout.grow_right()),

    # .: Xmonad :. #
    ("M-<slash>", lazy.layout.maximize()),
    ("M-S-<slash>", lazy.layout.normalize()),
    # Swap the position of the master/child panes
    ("M-<backslash>", lazy.layout.flip()),
    ("M-<minus>", lazy.layout.shrink()),
    ("M-<equal>", lazy.layout.grow()),

    # .: BSP :. #
    ("M-<period>", lazy.layout.toggle_split()),
    ("M-A-<Up>", lazy.layout.flip_up()),
    ("M-A-<Down>", lazy.layout.flip_down()),
    ("M-A-<Left>", lazy.layout.flip_left()),
    ("M-A-<Right>", lazy.layout.flip_right()),

    # .: Program Launchers :. #
    ("M-<Return>", lazy.spawn(TERMINAL + " -e zsh")),
    ("M-<semicolon>", lazy.spawn('rofi -show run -i')),
    ("M-c", lazy.spawn(script("calendar.sh"))),
    ("M-n", lazy.spawn('rofi-wifi-menu')),
    ("M-r", lazy.spawncmd()),  # Quick execution of shell commands
    ("M-t", lazy.spawn(script("show-todo.sh"))),
    ("M-w", lazy.spawn('rofi -show window')),
    ("M-C-c", lazy.spawn("google-chrome")),
    ("M-C-e", lazy.spawn("emacs")),
    ("M-C-f", lazy.spawn("firefox")),
    ("M-C-i", lazy.spawn("python3 -m qtconsole")),
    ("M-C-S-i", lazy.spawn("python3.6 -m qtconsole")),
    ("M-C-p", lazy.spawn("peek")),
    ("M-C-r", lazy.spawn(TERMINAL + ' -e "ranger"')),
    ("M-C-v", lazy.spawn(TERMINAL + ' -e "vim"')),
    ("M-C-h", lazy.spawn(TERMINAL + ' -e "htop"')),
    ("M-C-w", lazy.spawn(TERMINAL + ' -e "weechat"')),
    ("M-C-t", lazy.spawn("thunar")),

    # .: Layout / Focus Manipulation :. #
    ("M-f", lazy.window.toggle_fullscreen()),
    # Toggle between the available layouts.
    ("M-<grave>", lazy.next_layout()),
    ("A-<grave>", lazy.prev_layout()),
    # Switch focus between two screens
    ("M-<bracketleft>", lazy.to_screen(0)),
    ("M-<bracketright>", lazy.to_screen(1)),
    # Move the focused group to one of the screens and follow it
    ("M-S-<bracketleft>", switch_screens(0), lazy.to_screen(0)),
    ("M-S-<bracketright>", switch_screens(1), lazy.to_screen(1)),
    # Toggle between the two most recently used groups
    # TODO :: Write my own version of this that has the same
    #         screen preserving behaviour
    ("M-<Tab>", lazy.screen.toggle_group()),
    # Close the current window: NO WARNING!
    ("M-S-q", lazy.window.kill()),
    ("M-S-<BackSpace>", lazy.window.kill()),

    # .: Sys + Utils :. #
    # Restart qtile in place and pull in config changes (check config before
    # doing this with `check-qtile-conf` script to avoid crashes)
    ("M-A-r", lazy.restart()),
    # Shut down qtile.
    ("M-A-<Escape>", lazy.shutdown()),
    ("M-A-l", lazy.spawn("lock-screen")),
    ("M-A-s", lazy.spawn("screenshot")),
    ("M-A-<Delete>", lazy.spawn(script("power-menu.sh"))),
]]

# .: Jump between groups and also throw windows to groups :. #
for _ix, group in enumerate(groups):
    # Index from 1-0 instead of 0-9
    ix = 0 if _ix == 9 else _ix + 1

    keys.extend([EzKey(k[0], *k[1:]) for k in [
        # M-ix = switch to that group
        # ("M-%d" % ix, lazy.group[group.name].toscreen()),
        ("M-%d" % ix, focus_or_switch(group.name)),
        # M-S-ix = switch to & move focused window to that group
        ("M-S-%d" % ix, lazy.window.togroup(group.name)),
    ]])

# .: Use the mouse to drag floating layouts :. #
# XXX :: This can mess up layouts by having a perminant floating window...
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front())
]
