def create_new_word(db, encryptedword, word, countedword):
    sql_command = """INSERT INTO words (encryptedword, word, countedword) VALUES ("%s", "%s", %s)""" % (
        encryptedword, word, countedword)
    db.execute(sql_command)
