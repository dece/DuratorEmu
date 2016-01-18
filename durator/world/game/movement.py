from enum import Enum
import io
from struct import Struct

from durator.world.game.position import Position
from pyshgck.bin import read_struct


class MovementFlags(Enum):
    """ Flags defining the MovementBlock structure. Need double checking. """

    FORWARD      = 1 << 0
    BACKWARD     = 1 << 1
    STRAFE_LEFT  = 1 << 2
    STRAFE_RIGHT = 1 << 3
    TURN_LEFT    = 1 << 4
    TURN_RIGHT   = 1 << 5
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


class JumpData(object):

    BIN = Struct("<I4f")

    def __init__(self):
        self.time = 0
        self.velocity = 0.0
        self.sin = 0.0
        self.cos = 0.0
        self.xy_speed = 0.0

    @staticmethod
    def from_io(bytes_io):
        jump = JumpData()
        data = read_struct(bytes_io, JumpData.BIN)
        jump.time, jump.velocity, jump.sin, jump.cos, jump.xy_speed = data
        return jump

    def to_bytes(self):
        return self.BIN.pack(
            self.time,
            self.velocity,
            self.sin,
            self.cos,
            self.xy_speed
        )


class Movement(object):

    HEADER_BIN           = Struct("<2I")
    TRANSPORT_HEADER_BIN = Struct("<Q")
    SWIMMING_BIN         = Struct("<f")
    SPLINE_ELEVATION_BIN = Struct("<f")

    def __init__(self):
        self.flags = 0
        self.time = 0
        self.position = Position()
        self.transport_guid = 0
        self.transport_position = Position()
        self.swim_pitch = 0.0
        self.jump_data = JumpData()
        self.spline_elevation_unk = 0.0

    @staticmethod
    def from_bytes(data):
        movement = Movement()
        data_io = io.BytesIO(data)

        header_data = read_struct(data_io, Movement.HEADER_BIN)
        movement.flags, movement.time = header_data
        movement.position = Position.from_io(data_io)

        if movement.flags & MovementFlags.ON_TRANSPORT.value:
            transport_data = read_struct(data_io, Movement.TRANSPORT_HEADER_BIN)
            movement.transport_guid = transport_data[0]
            movement.transport_position = Position.from_io(data_io)

        if movement.flags & MovementFlags.IS_SWIMMING.value:
            swimming_data = read_struct(data_io, Movement.SWIMMING_BIN)
            movement.swim_pitch = swimming_data[0]

        if movement.flags & MovementFlags.IS_FALLING.value:
            movement.jump_data = JumpData.from_io(data_io)

        if movement.flags & MovementFlags.SPLINE_ELEVATION.value:
            elevation_data = read_struct(data_io, Movement.SPLINE_ELEVATION_BIN)
            movement.spline_elevation_unk = elevation_data[0]

        return movement

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
            data += self.jump_data.to_bytes()

        if self.flags & MovementFlags.SPLINE_ELEVATION.value:
            data += self.SPLINE_ELEVATION_BIN.pack(self.spline_elevation_unk)

        return data
