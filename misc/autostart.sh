#!/bin/bash
# -------------------------------------
# Bootsrap the start of a qtile session
# >> This get's run on restart as well!
# -------------------------------------

# pgrep -x doesn't seem to work for this. No idea why...
# This is used to make sure that things only get executed once
is_running() {
    ps -aux | awk "!/grep/ && /$1/" 
}

# Set screen resolutions (add additional screens here)
xrandr --output eDP1 --mode 1920x1080 &

# Set the background image
feh --bg-fill /home/innes/Pictures/Wallpapers/river-boat.jpg &
# feh --bg-fill /home/innes/Pictures/Wallpapers/dunstanburgh.jpg &
# feh --bg-fill /home/innes/Pictures/Wallpapers/turtle.jpg &
# feh --bg-fill /home/innes/Pictures/Wallpapers/cookies.jpg &
# feh --bg-fill /home/innes/Pictures/Wallpapers/mbridge-fields.jpg &
# feh --bg-fill /home/innes/Pictures/Wallpapers/elephant.png &

# Wait to let the X-Session start up correctly
sleep 1

# Bring in mate utils for managing the session
[[ $(is_running 'mate-settings-daemon') ]] || mate-settings-daemon &
[[ $(is_running 'mintupdate-launcher') ]] || mintupdate-launcher &
[[ $(is_running 'mate-power-manager') ]] || mate-power-manager &

# Compton visual compositing but not for qtile as it messes things up
if ! [[ $RUNNING_QTILE ]]; then
  [[ $(is_running 'compton') ]] || compton -CG &
fi;

# Network manager
[[ $(is_running 'nm-applet') ]] || nm-applet &

# Auto-mount external drives
[[ $(is_running 'udiskie') ]] || udiskie -a -n -t &

# Start the keyring daemon for managing ssh keys
[[ $(is_running 'gnome-keyring-daemon') ]] || gnome-keyring-daemon -s &

# Start xautolock using my wrapper around i3lock
# NOTE :: lock-screen is my custom screen lock script in ~/bin
# [[ $(is_running 'xautolock') ]] || xautolock -detectsleep -time 3 -locker "lock-screen"  -notify 30 -notifier "notify-send -u critical -t 10000 -- 'LOCKING screen in 30 seconds...'" &

# Notification daemon : first kill the default mate daemon if it has spun up
# [[ $(is_running 'mate-notification-daemon') ]] || killall mate-notification-daemon 
[[ $(is_running 'dunst') ]] || dunst &

# Music server
[[ $(is_running 'mopidy') ]] || python2 -m mopidy &

# polybar for i3
# [[ $(is_running 'polybar') ]] || polybar top
