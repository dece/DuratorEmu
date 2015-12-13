

class CharEnumHandler(object):

    # public ulong GUID;
    # public string Name;
    # public WoWRace Race;
    # public WoWClass Class;
    # public WoWGender Gender;

    # public byte Skin;
    # public byte Face;
    # public byte HairStyle;
    # public byte HairColor;
    # public byte FacialHair;

    # public byte Level;

    # public uint Zone;
    # public uint Map;
    # public float X, Y, Z;

    # public uint GuildId;
    # public uint CharacterFlags;
    # public byte FirstLogin;

    # public uint PetDisplayId;
    # public uint PetLevel;
    # public uint PetFamily;

    # public CharEnumEquipmentEntry[] Equipment;
    # public uint FirstBagDisplayId;
    # public byte FirstBagInventoryType;

    def __init__(self, connection, packet):
        self.conn = connection
        self.packet = packet

    def process(self):
        pass
