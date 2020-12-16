import mysql.connector as mysql


class Connexion:

    @classmethod    
    #Première commande pour créer la base de donnée
    def create_database(cls):
        cls.link = mysql.connect(user='root', password='root', host='localhost', port="8081")
        cls.cursor = cls.link.cursor()
        cls.cursor.execute("CREATE DATABASE IF NOT EXISTS `911`")
        cls.close_connexion()

    @classmethod
    #Permet d'ouvrir la connexion
    def open_connexion(cls):
        cls.link = mysql.connect(user='root', password='root', host='localhost', port="8081", database='911')
        cls.cursor = cls.link.cursor()

    @classmethod
    #Permet de fermer la connexion
    def close_connexion(cls):
        cls.cursor.close()
        cls.link.close()

    @classmethod
    def create_tables(cls):
        cls.open_connexion()
        #Créer la table emergencies
        cls.cursor.execute("CREATE TABLE `911`.`emergencies` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `lat` FLOAT(10) NOT NULL , `long` FLOAT(10) NOT NULL , `town` INT(7) NOT NULL , `address` VARCHAR(255) NOT NULL , `time` DATETIME NOT NULL , `type` INT(7) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB")
        #Créer la table towns
        cls.cursor.execute("CREATE TABLE `911`.`towns` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NOT NULL , `zip` INT(5) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB")
        #Créer la table types
        cls.cursor.execute("CREATE TABLE `911`.`types` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        #Créer la table intermédiaire
        cls.cursor.execute("CREATE TABLE `911`.`emergency_type` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `id_type` INT NOT NULL , `name` VARCHAR(255) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        #Ajouter les relations de emergencies
        cls.cursor.execute("ALTER TABLE `emergencies` ADD FOREIGN KEY (`town`) REFERENCES `towns`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT")
        cls.cursor.execute("ALTER TABLE `emergencies` ADD FOREIGN KEY (`type`) REFERENCES `emergency_type`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;")
        #Ajouter les relations de emergency_type
        cls.cursor.execute("ALTER TABLE `emergency_type` ADD FOREIGN KEY (`id_emergency`) REFERENCES `emergencies`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT")
        cls.cursor.execute("ALTER TABLE `emergency_type` ADD FOREIGN KEY (`id_emergency`) REFERENCES `types`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT")
        cls.close_connexion()

    @classmethod
    #Remplir la table towns
    def load_towns(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO towns VALUES (NULL, %s, %s)", data)
        cls.link.commit()
        cls.close_connexion()

    @classmethod
    #Remplir la table types
    def load_types(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO types VALUES (NULL, %s)", data)
        cls.link.commit()
        cls.close_connexion()

    @classmethod
    #Remplir la table emergency_types
    def load_emergency_types(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO emergency_type VALUES (NULL, (SELECT id from types WHERE name = %s), %s)", data)
        cls.link.commit()
        cls.close_connexion()

    @classmethod
    #Remplir la table principale emergencies
    def load_emergencies(cls, data):
        cls.open_connexion()
        cls.cursor.execute("INSERT INTO emergencies VALUES (NULL, %s, %s, (SELECT id from towns WHERE zip = %s AND name = %s), %s, %s, (SELECT id from emergency_type WHERE name = %s AND id_type = (SELECT id FROM types WHERE name = %s)))", data)
        cls.link.commit()
        cls.close_connexion()