import mysql.connector as mysql


class Connexion:

    @classmethod
    def ouvrir_connexion(cls):
        cls.link = mysql.connect(
            user='root', password='root', host='localhost', port="8081", database='911')
        cls.cursor = cls.link.cursor()

    @classmethod
    def fermer_connexion(cls):
        cls.cursor.close()
        cls.link.close()