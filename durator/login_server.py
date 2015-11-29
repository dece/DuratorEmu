import socket
from struct import Struct
import threading

from shgck_tools.bin import dump_data

from durator.network import netstr_to_str
from durator.srp import Srp


class LoginServer(object):
    """ Listen for clients and start a new thread for each connection. """

    HOST = "0.0.0.0"
    PORT = 3724
    BACKLOG_SIZE = 64

    def __init__(self):
        self.socket = None
        # self.clients = []

    def is_running(self):
        return self.socket is None

    def start(self):
        self._start_listening()
        self._accept_connections()
        self._stop_listening()

    def _start_listening(self):
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self.socket.bind( (LoginServer.HOST, LoginServer.PORT) )
        self.socket.listen(LoginServer.BACKLOG_SIZE)
        print("Login server running.")

    def _accept_connections(self):
        try:
            while True:
                self._try_accept_connection()
        except KeyboardInterrupt:
            print("KeyboardInterrupt received, stopping server.")

    def _try_accept_connection(self):
        try:
            connection, address = self.socket.accept()
            self._handle_connection(connection, address)
        except socket.timeout:
            pass

    def _handle_connection(self, connection, address):
        print("Accepting connection from", address)
        client = LoginConnection(self, connection, address)
        client.threaded_handle()
        # self.clients.append(client)

    def _stop_listening(self):
        self.socket.close()
        self.socket = None
        print("Login server stopped.")

    def get_pass_entry(self, account_name):
        pass_entry = Srp.gen_pass_entry(account_name, account_name)
        return pass_entry


class LoginConnection(object):
    """ Handle the login process of a client with a SRP challenge. """

    def __init__(self, server, socket, address):
        self.server = server
        self.socket = socket
        self.address = address
        self.srp = Srp()

    def __del__(self):
        self.socket.close()

    def threaded_handle(self):
        connection_thread = threading.Thread(target = self._handle)
        connection_thread.daemon = True
        connection_thread.start()

    def _handle(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            self._handle_packet(data)
        print("Connection closed.")

    def _handle_packet(self, data):
        print(dump_data(data), end = "")
        opcode = data[0]
        if opcode == LoginOpCodes.CHALLENGE:
            print("Received challenge.")
            self._handle_challenge(data[1:])
        else:
            print("Unknown operation:", opcode)

    def _handle_challenge(self, data):
        challenge = LoginChallenge(data)
        pass_entry = self.server.get_pass_entry(challenge.account_name)
        answer = challenge.get_answer(self.srp, pass_entry)
        print("Answering challenge:")
        print(dump_data(answer), end = "")
        self.socket.sendall(answer)


class LoginOpCodes(object):
    """ Opcodes used during the login process. """

    CHALLENGE = 0x00
    PROOF     = 0x01
    REALMLIST = 0x10


class LoginChallenge(object):
    """ Process a challenge request and answer with the challenge data. """

    CHALL_HEADER_BIN = Struct("<BH")
    CHALL_CONTENT_BIN = Struct("<4s3BH4s4s4sI4BB")
    REPR_FORMAT = ( "Error={}, Size={}, Game='{}', Version={}.{}.{}.{}, "
                    "Arch='{}', Platform='{}', Locale='{}', TZ={}, "
                    "IP={}.{}.{}.{}, Account='{}'" )

    CHALL_ANSWER_BIN = Struct("<3B32sB1sB32s32s16sB")

    def __init__(self, packet):
        self.unk_code = 0
        self.size = 0
        self.game_name = ""
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.version_build = 0
        self.arch = ""
        self.platform = ""
        self.locale = ""
        self.timezone = 0
        self.ip = (0, 0, 0, 0)
        self.account_name_size = 0
        self.account_name = ""
        self.parse_packet(packet)

    def __repr__(self):
        return LoginChallenge.REPR_FORMAT.format(
            self.unk_code, self.size, self.game_name,
            self.version_major, self.version_minor,
            self.version_patch, self.version_build,
            self.arch, self.platform, self.locale, self.timezone,
            self.ip[0], self.ip[1], self.ip[2], self.ip[3],
            self.account_name
        )

    def parse_packet(self, packet):
        offset = 0
        self._parse_packet_header(offset, packet)
        offset += LoginChallenge.CHALL_HEADER_BIN.size
        self._parse_packet_content(offset, packet)
        print(self)

    def _parse_packet_header(self, offset, packet):
        end_offset = offset + LoginChallenge.CHALL_HEADER_BIN.size
        header = packet[ offset : end_offset ]
        header_data = LoginChallenge.CHALL_HEADER_BIN.unpack(header)
        self.unk_code = header_data[0]
        self.size = header_data[1]

    def _parse_packet_content(self, offset, packet):
        end_offset = offset + LoginChallenge.CHALL_CONTENT_BIN.size
        content = packet[ offset : end_offset ]
        content_data = LoginChallenge.CHALL_CONTENT_BIN.unpack(content)

        self.game_name = netstr_to_str(content_data[0])
        self.version_major = content_data[1]
        self.version_minor = content_data[2]
        self.version_patch = content_data[3]
        self.version_build = content_data[4]
        self.arch = netstr_to_str(content_data[5])
        self.platform = netstr_to_str(content_data[6])
        self.locale = netstr_to_str(content_data[7])
        self.timezone = content_data[8]
        self.ip = content_data[9:13]
        self.account_name_size = content_data[13]

        account_name = packet[ end_offset : end_offset+self.account_name_size ]
        self.account_name = account_name.decode("ascii")

    def get_answer(self, srp, pass_entry):
        srp.gen_server_ephemeral(pass_entry.verifier)
        server_ephemeral = int.to_bytes(srp.server_ephemeral, 32, "little")
        generator = int.to_bytes(Srp.GENERATOR, 1, "little")
        modulus = int.to_bytes(Srp.MODULUS, 32, "little")
        salt = pass_entry.salt

        answer = LoginChallenge.CHALL_ANSWER_BIN.pack(
            LoginOpCodes.CHALLENGE,
            LoginChallengeResults.SUCCESS,
            0,
            server_ephemeral,
            1,
            generator,
            32,
            modulus,
            salt,
            b"\x00" * 16,
            0
        )
        return answer


class LoginChallengeResults(object):

    SUCCESS = 0x00
