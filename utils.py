import asymmetric_encryption as ae
import bcrypt

def format_words_for_db(ordered_dict, public_key):
    dicts = []
    for key, val in ordered_dict.items():
        new_dict = {}
        try:
            new_dict["encryptedword"] = bcrypt.hashpw(
                key.encode('utf-8'), bcrypt.gensalt())
            new_dict["word"] = ae.encrypt_message(str(key), public_key)
            new_dict['countedword'] = val
            dicts.append(new_dict)
        except UnicodeEncodeError:
            pass

    return dicts
