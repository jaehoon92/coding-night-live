from channels import route
from .consumers import *

# Websocket command : join => call room_join
custom_routing = [
    route("room.receive", room_join, command="^join$"),
    route("room.receive", room_leave, command="^leave$"),
    route("room.receive", rename_room, command="^rename_room$"),
    route("room.receive", new_slide, command="^new_slide$"),
    route("room.receive", get_slide, command="^get_slide$"),
    route("room.receive", del_slide, command="^del_slide$"),
    route("room.receive", curr_slide, command="^curr_slide$"),
    route("room.receive", change_slide_order, command="^change_slide_order$"),
    route("room.receive", rename_slide, command="^rename_slide_title$"),
    route("room.receive", change_slide, command="^change_slide$"),
    route("room.receive", get_slide_diff, command="^get_slide_diff$"),
]
