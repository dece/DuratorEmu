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

- - -

```
ERROR #0 (0x85100000)
Program:  F:\Jeux\World of Warcraft\1.1.2.4125 (Vanilla EU release)\WoW.exe
File: ..\WowServices/BitField.h
Line: 90
Expr: bitNum < m_numBits


WoWBuild: 4125
------------------------------------------------------------------------------

----------------------------------------
    Stack Trace (Manual)
----------------------------------------

Address  Frame    Logical addr  Module

004B9AE1 0019FC08 0001:000B8AE1 F:\Jeux\World of Warcraft\1.1.2.4125 ...
004999F6 0019FC20 0001:000989F6 F:\Jeux\World of Warcraft\1.1.2.4125 ...
005D864F 0019FC3C 0001:001D764F F:\Jeux\World of Warcraft\1.1.2.4125 ...
005D878D 0019FC50 0001:001D778D F:\Jeux\World of Warcraft\1.1.2.4125 ...
0046D460 0019FD6C 0001:0006C460 F:\Jeux\World of Warcraft\1.1.2.4125 ...
0046C708 0019FD90 0001:0006B708 F:\Jeux\World of Warcraft\1.1.2.4125 ...
00534534 0019FDB8 0001:00133534 F:\Jeux\World of Warcraft\1.1.2.4125 ...
00534829 0019FDE8 0001:00133829 F:\Jeux\World of Warcraft\1.1.2.4125 ...
00535180 0019FE14 0001:00134180 F:\Jeux\World of Warcraft\1.1.2.4125 ...
0040372F 0019FE54 0001:0000272F F:\Jeux\World of Warcraft\1.1.2.4125 ...
00418662 0019FECC 0001:00017662 F:\Jeux\World of Warcraft\1.1.2.4125 ...
00417E91 0019FEE0 0001:00016E91 F:\Jeux\World of Warcraft\1.1.2.4125 ...
004041FB 0019FF80 0001:000031FB F:\Jeux\World of Warcraft\1.1.2.4125 ...
76B53744 0019FF94 0001:00003744 C:\WINDOWS\SYSTEM32\KERNEL32.DLL
77319CD4 0019FFDC 0001:00058CD4 C:\WINDOWS\SYSTEM32\ntdll.dll
77319C9F 0019FFEC 0001:00058C9F C:\WINDOWS\SYSTEM32\ntdll.dll
```

- - -

03:03:36 WARNING  Unknown opcode 211
00000000 ce 01 00 00                                     ....
03:03:36 WARNING  Unknown opcode 1CE
00000000 ff 01 00 00                                     ....
03:03:36 WARNING  Unknown opcode 1FF
00000000 56 00 00 00 e4 1f 00 00 00 00 00 00 00 00 00 00 V...............
03:03:36 WARNING  Unknown opcode 56
00000000 56 00 00 00 5f 24 00 00 00 00 00 00 00 00 00 00 V..._$..........
03:03:36 WARNING  Unknown opcode 56
