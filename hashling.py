import random
import string


def hashling(input_data: str = "test_data", salt: str = "salt%here*", hash_char_len: int = 64, infolds: int = 10,
             character_mask: bool = False, enforce_phrasing: bool = False, enforce_max_char_repeat: bool = False, hash_profile: dict = None):

    if hash_profile is None:
        input_data = input_data
        salt = salt
        hash_char_len = hash_char_len
        infolds = infolds
        character_mask = character_mask
        enforce_phrasing = enforce_phrasing
        enforce_max_char_repeat = enforce_max_char_repeat

    elif hash_profile is not None:
        input_data = hash_profile["input_data"]
        if type(input_data) != str:
            raise Exception("input_data must be passed in as an string")
        salt = hash_profile["salt"]
        if type(salt) != str:
            raise Exception("salt must be passed in as an string")
        hash_char_len = hash_profile["hash_char_len"]
        if type(hash_char_len) != int:
            raise Exception("hash_char_len must be passed in as an integer")
        infolds = hash_profile["infolds"]
        if type(infolds) != int:
            raise Exception("infolds must be passed in as an integer")
        character_mask = hash_profile["character_mask"]
        if type(character_mask) != bool:
            raise Exception("character_mask must be passed in as an bool")
        enforce_phrasing = hash_profile["enforce_phrasing"]
        if type(enforce_phrasing) != bool:
            raise Exception("enforce_phrasing must be passed in as an bool")
        enforce_max_char_repeat = hash_profile["enforce_max_char_repeat"]
        if type(enforce_max_char_repeat) != bool:
            raise Exception("enforce_max_char_repeat must be passed in as an bool")

    if len(input_data) < 10:
        raise Exception("input_data must have a minimum length of 10")

    if hash_char_len < 64:
        raise Exception("hash_char_len must be 64 or greater")

    if infolds > 6:
        raise Exception("infolds must be 0 and 6")

    if enforce_phrasing:
        spaces = 0
        for i in input_data:
            if i == " ":
                spaces += 1
        if spaces < 2:
            raise Exception("input must contain spaces between words 2 spaces minimum")

    if len(salt) < 10:
        raise Exception("salt must be at least 10 characters long")

    if enforce_max_char_repeat:
        repeat = 0
        last_char = ""
        for i in input_data:
            if i == last_char:
                repeat += 1
                if repeat >= 3:
                    raise Exception(f"character '{i}' exceeds sequential repeating characters of 3 for input_data")
            if i != last_char:
                repeat = 0
                last_char = i

    input_data2 = input_data[::-1]
    new_input = []
    for i in range(len(input_data)):
        new_input.append(input_data[i])
        new_input.append(input_data2[i])
    input_data = "".join(new_input)

    mutation = hash_char_len // 2

    salted_string = f"{salt}{input_data}"
    to_ord = [ord(i) for i in salted_string]

    ord_to_power = [str(i**mutation) for i in to_ord]
    ord_to_power2 = [i**mutation for i in to_ord]
    ord_to_power2.sort(reverse=True)
    ord_to_power2 = [str(i) for i in ord_to_power2]

    ord_to_power = "".join(ord_to_power)
    ord_to_power2 = "".join(ord_to_power2)

    org_length = len(ord_to_power)
    zip_add = [str(int(i) + int(ord_to_power2[ord_to_power.index(i)])) for i in ord_to_power]
    zip_add = "".join(zip_add)

    while len(zip_add) != org_length:
        zip_add = zip_add[:-1]

    seg_zip = [zip_add[i:i + 20] for i in range(0, len(zip_add), 20)]
    if len(seg_zip[0]) != len(seg_zip[-1]):
        seg_zip.pop()

    seg_zip = "".join(seg_zip)

    def infold(data: str):
        seg_length = len(data)
        front_half = data[:seg_length//2]
        back_half = data[seg_length//2:]

        while len(front_half) != hash_char_len//2:
            front_half = front_half[:-1]

        while len(back_half) != hash_char_len//2:
            back_half = back_half[:-1]

        zipped_list = []
        for x in range(len(front_half)):
            zipped_list.append(front_half[x])
            zipped_list.append(back_half[x])

        return "".join(zipped_list)

    zipped_list = infold(seg_zip)

    for i in range(infolds):
        zipped_list = infold(zipped_list)

    length_of_zipped = len(zipped_list)
    symbols = ["q", "w", "e", "r", "t", "y", "$", "#", "@", "!"]
    if character_mask:
        altered_list = []
        for i in zipped_list:

            if i == zipped_list[-1]:
                altered_list.append(symbols[int(i)])
            elif i == zipped_list[0]:
                altered_list.append(symbols[int(i)])
            elif i == zipped_list[0]:
                altered_list.append(symbols[int(i)])
            elif i == zipped_list[length_of_zipped//2]:
                altered_list.append(symbols[int(i)])
            else:
                altered_list.append(i)

        return "".join(altered_list)
    else:
        return zipped_list


# combines two lists into one string in alternating order
def zip_list(list1: list, list2: list):
    zipped_list = []
    for x in range(len(list1)):
        zipped_list.append(list1[x])
        zipped_list.append(list2[x])

    return "".join(zipped_list)


# generates a random salt string of a given length
def generate_salt(length: int):
    characters = string.ascii_letters + string.digits + string.punctuation
    salt = ""
    for i in range(length):
        salt += random.choice(characters + " ")
    return salt


# profile example

# profile = {
#     "input_data": "password111",
#     "salt": "salt%4321!",
#     "hash_char_len": 64,
#     "infolds": 4,
#     "character_mask": False,
#     "enforce_phrasing": False,
#     "enforce_max_char_repeat": True
# }



