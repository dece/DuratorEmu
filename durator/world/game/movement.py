from enum import Enum
from struct import Struct

from durator.world.game.position import Position


class MovementFlags(Enum):
    """ Flags defining the MovementBlock structure. Need double checking. """

    # FORWARD      = 1 << 0
    # BACKWARD     = 1 << 1
    # STRAFE_LEFT  = 1 << 2
    # STRAFE_RIGHT = 1 << 3
    # TURN_LEFT    = 1 << 4
    # TURN_RIGHT   = 1 << 5
    # PITCH_UP     = 1 << 6
    # PITCH_DOWN   = 1 << 7
    # WALK_MODE    = 1 << 8

    # IS_LEVITATING  = 1 << 10
    # IS_FLYING      = 1 << 11
    IS_FALLING     = 1 << 13
    # IS_FALLING_FAR = 1 << 14
    IS_SWIMMING    = 1 << 21

    # SPLINE_ENABLED = 1 << 22
    # CAN_FLY        = 1 << 23
    # FLYING_OLD     = 1 << 24

    ON_TRANSPORT     = 1 << 25
    SPLINE_ELEVATION = 1 << 26
    # ROOT             = 1 << 27
    # IS_WATERWALKING  = 1 << 28
    # SAFE_FALL        = 1 << 29
    # HOVER            = 1 << 30


class MovementBlock(object):

    HEADER_BIN           = Struct("<2I")
    TRANSPORT_HEADER_BIN = Struct("<Q")
    SWIMMING_BIN         = Struct("<f")
    FALLING_BIN          = Struct("<I4f")
    SPLINE_ELEVATION_BIN = Struct("<f")

    def __init__(self):
        self.flags = 0
        self.time = 0
        self.position = Position()
        self.transport_guid = 0
        self.transport_position = Position()
        self.swim_pitch = 0.0
        self.fall_time = 0
        self.jump_velocity = 0.0
        self.jump_sin = 0.0
        self.jump_cos = 0.0
        self.jump_xy_speed = 0.0
        self.spline_elevation_unk = 0.0

    def to_bytes(self):
        data = b""
        data += self.HEADER_BIN(self.flags, self.time)
        data += self.position.to_bytes()

        if self.flags & MovementFlags.ON_TRANSPORT.value:
            data += self.TRANSPORT_HEADER_BIN.pack(self.transport_guid)
            data += self.transport_position.to_bytes()

        if self.flags & MovementFlags.IS_SWIMMING.value:
            data += self.SWIMMING_BIN.pack(self.swim_pitch)

        if self.flags & MovementFlags.IS_FALLING.value:
            data += self.FALLING_BIN.pack(
                self.fall_time,
                self.jump_velocity,
                self.jump_sin,
                self.jump_cos,
                self.jump_xy_speed
            )

        if self.flags & MovementFlags.SPLINE_ELEVATION.value:
            data += self.SPLINE_ELEVATION_BIN.pack(self.spline_elevation_unk)

        return data
