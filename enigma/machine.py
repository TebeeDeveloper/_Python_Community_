import string
import datetime

class Rotor:
    def __init__(self, wiring: str, notch: int, ring_setting: int, name: str):
        self.name = name
        self.ring_setting = ring_setting
        self.notch = notch
        self.position = 0
        
        self.forward_map = [0] * 26
        self.backward_map = [0] * 26
        
        for i, char in enumerate(wiring):
            self.forward_map[i] = ALPHABET.index(char)
            self.backward_map[ALPHABET.index(char)] = i
    def rotate(self):
        self.position = (self.position + 1) % 26
    def set_position(self, pos: str):
        if not pos or not pos in list(string.ascii_letters):
            position_char = 'A'
        else:
            position_char = pos.strip()[0].upper()
        self.position = ALPHABET.index(position_char)
    def forward(self, char_idx: int) -> int:
        wiring_idx = (char_idx - self.position + self.ring_setting) % 26
        wiring_idx_temp = self.forward_map[wiring_idx]
        final_idx = (wiring_idx_temp + self.position - self.ring_setting) % 26
        return final_idx
    def backward(self, char_idx: int) -> int:
        wiring_idx = (char_idx - self.position + self.ring_setting) % 26
        wiring_idx_temp = self.backward_map[wiring_idx]
        final_idx = (wiring_idx_temp + self.position - self.ring_setting) % 26
        return final_idx
class StandingRotor:
    def __init__(self, wiring: str):
        self.position = 0
        self.forward_map = [0] * 26
        self.backward_map = [0] * 26
        
        for i, char in enumerate(wiring):
            self.forward_map[i] = ALPHABET.index(char)
            self.backward_map[ALPHABET.index(char)] = i
    def rotate(self):
        self.position = (self.position + 1) % 26
    def set_position(self, pos_var: str):
        if not pos_var or not pos_var in list(string.ascii_letters):
            position_char = "A"
        else:
            position_char = pos_var.strip()[0].upper()
        self.position = ALPHABET.index(position_char)
    def forward(self, char_idx: int) -> int:
        wiring_idx = (char_idx - self.position) % 26
        wiring_idx_temp = self.forward_map[wiring_idx]
        final_idx = (wiring_idx_temp + self.position) % 26
        return final_idx
    def backward(self, char_idx: int) -> int:
        wiring_idx = (char_idx - self.position) % 26
        wiring_idx_temp = self.backward_map[wiring_idx]
        final_idx = (wiring_idx_temp + self.position) % 26
        return final_idx
class Plugboard:
    def __init__(self):
        pairs = self.get_daily_plugboard()
        self.mapping = self._create_mapping(pairs)
    def _create_mapping(self, pairs: str):
        mapping = {}
        processed_char = set()
        
        pairs_list = pairs.split()
        
        for pair in pairs_list:
            if len(pair) != 2:
                raise ValueError("Pair phai co hai ky tu")
            c1, c2 = pair[0], pair[1]
            if c1 in processed_char or c2 in processed_char:
                raise ValueError("Da co trong xu ly")
            mapping[c1] = c2
            mapping[c2] = c1

            processed_char.add(c1)
            processed_char.add(c2)
        return mapping
    def get_daily_plugboard(self) -> str:
        today = datetime.date.today().day
        daily_plugboard = plugboard_config[today]
        return "".join(daily_plugboard)
    def process(self, char_idx: int) -> int:
        input_char = ALPHABET[char_idx]
        
        if input_char in self.mapping:
            output_char = self.mapping[input_char]
            return ALPHABET.index(output_char)
        else:
            return char_idx
class Reflector:
    def __init__(self, wiring: str):
        self.map = [ALPHABET.index(c) for c in wiring]
    def reflect(self, char_idx):
        return self.map[char_idx]
class Machine:
    def __init__(self, plugboard, reflector, main_rotors, standing_rotor):
        self.plugboard = plugboard
        self.reflector = reflector
        self.main_rotors = main_rotors
        self.standing_rotor = standing_rotor
    def rotate_rotors(self):
        is_R0_at_notch = ALPHABET[self.main_rotors[0].position] == self.main_rotors[0].notch
        is_R1_at_notch = ALPHABET[self.main_rotors[1].position] == self.main_rotors[1].notch
        
        if is_R1_at_notch:
            self.main_rotors[2].rotate()
            self.main_rotors[1].rotate()
        if is_R0_at_notch and not is_R1_at_notch:
            self.main_rotors[1].rotate()
        
        self.main_rotors[0].rotate()
        
        for i in range(2, len(self.main_rotors)):
            if ALPHABET[self.main_rotors[i].position] == self.main_rotors[i].notch:
                if i < len(main_rotors) - 1:
                    self.main_rotors[i+1].rotate()
        self.standing_rotor.rotate()
    def set_positions(self, position):
        for rotor, pos in zip(rotors, position):
            rotor.set_position(pos)
    def process_char(self, char: str, decrypt_mode: bool):
        if len(char) != 1 or char not in string.ascii_letters:
            return char

        is_lower = char.islower()
        char = char.upper()
        self.rotate_rotors()

        index = ALPHABET.index(char)
        index = self.plugboard.process(index)
        if not decrypt_mode:
            index = self.standing_rotor.forward(index)
            
            for rotor in self.main_rotors:
                index = rotor.forward(index)
        else:
            for rotor in self.main_rotors:
                index = rotor.forward(index)

        index = self.reflector.reflect(index)
        if not decrypt_mode:
            for rotor in reversed(self.main_rotors):
                index = rotor.backward(index)
        else:
            for rotor in reversed(self.main_rotors):
                index = rotor.backward(index)
            index = self.standing_rotor.backward(index)
            
        index = self.plugboard.process(index)
        result_char = ALPHABET[index]
        return result_char.lower() if is_lower else result_char
    def encrypt_text(self, text: str):
        encoded_text = [
            self.process_char(c,False) if c in string.ascii_letters else c
            for c in text
        ]
        return "".join(encoded_text)
    def decrypt_text(self, text: str):
        decoded_text = [
            self.process_char(c,True) if c in string.ascii_letters else c
            for c in text
        ]
        return "".join(decoded_text)
def create_rotors():
    rotor_created = []
    while len(rotor_created) != 1000:
        for i in range(10):
            rt = Rotor(
                wiring=rotor_data[i]['wiring'],
                notch=rotor_data[i]['notch'],
                ring_setting=ALPHABET.index(rotor_data[i]['ring_setting']),
                name= str(i)
            )
            rotor_created.append(rt)
    return rotor_created
def EnigmaMachine():
    return Machine(
        plugboard=plugboard,
        reflector=reflector,
        main_rotors=main_rotors,
        standing_rotor=standing_rotor
    )
filepath = "enigma_license.txt"
ALPHABET = string.ascii_uppercase
rotor_data = {
    0: {'wiring': 'CGIOQFBVEKAJURDNHYWZMTXLSP', 'notch': 'G', 'ring_setting': 'U'},
    1: {'wiring': 'KWAXCGJYEQMULZVBSDNTPIOFRH', 'notch': 'K', 'ring_setting': 'H'},
    2: {'wiring': 'CMAIZFKHBGQEJOLTWUXPDYRVNS', 'notch': 'L', 'ring_setting': 'K'},
    3: {'wiring': 'NUHQTKVIMEOARDBGZXPFSCLWJY', 'notch': 'Q', 'ring_setting': 'Y'},
    4: {'wiring': 'FDVPLOBMGWQKRCSAENZTXUIYJH', 'notch': 'P', 'ring_setting': 'O'},
    5: {'wiring': 'BZEJDHYPLRFNKSQTWCIXUOMVGA', 'notch': 'T', 'ring_setting': 'H'},
    6: {'wiring': 'DGBIXFACJEHTMKUPLSOZVRYNQW', 'notch': 'M', 'ring_setting': 'F'},
    7: {'wiring': 'CEHKGPBJDQANILSFMRZWYTOXUV', 'notch': 'Y', 'ring_setting': 'S'},
    8: {'wiring': 'DJFILGAKNECHTPVOWQBMRYUSZX', 'notch': 'H', 'ring_setting': 'G'},
    9: {'wiring': 'YSQXJOWIZURATHNKGMFCELDPBV', 'notch': 'J', 'ring_setting': 'S'}
}
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
# A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
plugboard_config = {
    1: "AB CD EF",
    2: "OP XC BT",
    3: "MN JK HG",
    4: "ST UV WX",
    5: "BV AS TX",
    6: "KH GL IJ",
    7: "KL MN OP",
    8: "NF PB TU",
    9: "WX YZ AB",
    10: "CD EF GH",
    11: "IJ UT MN",
    12: "OP QR ST",
    13: "SA WX HT",
    14: "AB QO PK",
    15: "CD BF PS",
    16: "EF QU BT",
    17: "GH KS DV",
    18: "IJ PZ LK",
    19: "KL PT GI",
    20: "MN XB HU",
    21: "BT YU HJ",
    22: "LK YU QW",
    23: "ST UY OP",
    24: "BH YU EW",
    25: "SD GH BC",
    26: "PO UI WR",
    27: "KJ LM OI",
    28: "QW AS ZX",
    29: "LK GH TR",
    30: "KJ UI ZX",
    31: "GT BV WS",
}
standing_rotor_wiring = 'XZLJVTBHUFDWSAYMRGNICKPEOQ'
reflector_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

sr = StandingRotor(
    wiring=standing_rotor_wiring
)
rotors = []
main_rotors = create_rotors()
for rotor in main_rotors:
    rotors.append(rotor)
rotors.append(sr)
standing_rotor = sr
plugboard = Plugboard()
reflector = Reflector(wiring=reflector_wiring)

INFORMATION = """
===================================================================================================================================================================================
    CUSTOM ENIGMA MACHINISM LICENSE - CEML
    ----          INFORMATION         ----
    Version: 1.0
===================================================================================================================================================================================
I. Vấn đề bản quyền
    [2025]. Mọi quyền được bảo lưu
-   Tác giả: Tebee_Sunaookami - Trần Trung Nghĩa
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-   Sở hữu trí tuệ:
    +   Module này được phát triển độc lập dựa trên kiến thức về mật mã cổ điển.
    +   "Cơ chế Enigma 1000 Rotor" là thiết kế độc quyền của tác giả, không sao chép từ bất kỳ hệ thống Enigma thương mại hoặc học thuật hiện có nào.
    +   Việc sử dụng, sao chép hoặc phân phối lại module này mà không có sự cho phép bằng văn bản đều bị nghiêm cấm.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

II. Giới thiệu Enigma cổ điển (nền tảng của module)
-   Enigma là máy mật mã của Đức Quốc Xã trong Thế chiến 2.

-   Đây là cổ máy có tầm quan trọng nhất, về việc bảo vệ thông tin nội bộ
        Alan Turin & Bletchley Park đã giải mã
        
- Thành phần:
    Bàn phím (Keyboard): Nhập liệu.
    Bảng cắm (Plugboard/Steckerbrett): Trao đổi ký tự ban đầu, là một trong những tầng mã hóa quan trọng.
    Các Rotor (Rotors/Walzen): [Thường 3-5 rotor] Thực hiện phép thế hoán vị. Mỗi lần gõ phím, các rotor quay, thay đổi hoán vị.
    Rotor Phản xạ (Reflector/Umkehrwalze): Đảm bảo tính thuận nghịch của mã hóa (A được mã thành B thì B sẽ được mã thành A), nhưng cũng là
    yếu tố then chốt ngăn chặn việc một ký tự tự mã hóa thành chính nó.
    
-   Nguyên lý hoạt động:
    Bàn phím -> Plugboard -> Rotor 1, 2, 3 -> Reflector -> Rotor 3, 2, 1 -> Plugboard -> Đèn báo
    
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

III. Giới thiệu Enigma Module Made By Tebee
-   Dựa trên nguyên lý Enigma cổ điển, với 1000 rotor làm tăng không gian khoá (space key) và độ phức tạp khi giải mã
-   Không gian khoá lý thuyết là 26^1000
-   Kiến trúc độc quyền:
    -   Cơ chế quay:
        Khi rotor n - 1 chạm notch [Ví dụ: X]
        Rotor n quay 1 nấc [Ví dụ: P 0->1 K]
    -> Đây gọi là Double Stepping
    -   Plugboard động: Thay đổi plugboard theo ngày
    -   Không gian khoá ước tính 26^1000. Có thể nói lớn hơn số nguyên tử trong vũ trụ quan sát được.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

IV. Ý tưởng và Tính năng Bổ sung
-   Tối ưu hoá hiệu suất:
    -   Cơ chế EnigmaGamma
    -   Được xây dựng hoàn toàn bằng Python và thư viện string
    
-   Tính năng đặc biệt:
    -   Hỗ trợ bộ ký tự ALPHABET (A-Z)
    
-   Lĩnh vực và Ứng dụng Tiềm năng:
    -   Công cụ giáo dục về mật mã
    -   Sử dụng trong trò chơi và phòng thử thách
    -   Nghiên cứu về độ phức tạp của mật mã Rotor

-   Ý tưởng phát triển tiếp theo:
    -   Reflector động
    -   Mã hoá số và ký tự bảng chữ cái tiếng Việt
    -   Mã hoá ký tự Unicode

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

V. Liên hệ và Hợp tác
-   Gmail: tebeebmgo@gmail.com
-   Link sử dụng file cho mục đích cá nhân: https://www.mediafire.com/folder/bsypnf174a32y/Enigma+Machinism
-   Link GitHub: https://github.com/TebeeDeveloper/_Python_Community_

===================================================================================================================================================================================
"""