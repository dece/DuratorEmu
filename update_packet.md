Update packet
=============

- uint32        count
- uint8         bool hasTransport (?)
- uint8         UPDATE_TYPE (should it be 2 or 3 for player spawn?)
- uint64        guid
- uint8         OBJECT_TYPE (4 for player)
- MovementBlocks
        - uint32        flags
        - uint32        unk
        - float[4]      position+ori
        - (maybe stuff due to flags)
        - float[6]      speeds (walk, run, bw, swim, swim bw, turn)
        - (maybe stuff due to flags)
- uint32        isPlayer ? 1 : 0
- uint32        attack cycle
- uint32        timer ID
- uint64        victim guid 
- uint8         mask block count
- UpdateBlocks

Notes from Deamon, valid for late Vanilla, maybe not for early!

GUID can be packed, it works like this:

> "packed guid" goes like this: first uint8 bit mask and then the actual data
> lets say the mask will be 1101001
> then the "data" will contain 0-th, 3-rd, 5-th and 6-th bytes of int64
> this is "blizz" way of ommiting useless zeros in packet payload :D

About the whole packet:

> 1) Update only "update fields"
> 2) spawn a new "world object"
> 3) destroy object
> 1 - is update packet type 1
> 2 - is update packet 2 and 3
> 3 - is type 4 and 5
> type 1 include only "update fields", type 2 and 3 include movement information
> block + update fields, 4 and 5 are just list of guids

> There are 6 types of world objects in WoW: world_object, world_unit,
> world_player, world_gameobject, world_corpse, world_dynamicobject pktLen+1 is
> mostly internal stuff there. Buf array starts with packet length, then 2 bytes
> of opcode, and then goes the actual packet payload. That's just how this
> sandbox organizes it's memory
