import mysql.connector as mysql


class Connexion:

    @classmethod    
    def create_database(cls):
        cls.link = mysql.connect(user='root', password='root', host='localhost', port="8081")
        cls.cursor = cls.link.cursor()
        cls.cursor.execute("CREATE DATABASE IF NOT EXISTS `911`")
        cls.close_connexion()

    @classmethod
    def open_connexion(cls):
        cls.link = mysql.connect(user='root', password='root', host='localhost', port="8081", database='911')
        cls.cursor = cls.link.cursor()

    @classmethod
    def close_connexion(cls):
        cls.cursor.close()
        cls.link.close()

    @classmethod
    def create_tables(cls):
        cls.open_connexion()
        #Créer la table emergencies
        cls.cursor.execute("CREATE TABLE `911`.`emergencies` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `lat` FLOAT(10) NOT NULL , `long` FLOAT(10) NOT NULL , `desc` VARCHAR(255) NOT NULL , `town` INT(1) NOT NULL , `address` VARCHAR(255) NOT NULL , `time` DATETIME NOT NULL , `type` INT(1) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB")
        #Créer la table towns
        cls.cursor.execute("CREATE TABLE `911`.`towns` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NOT NULL , `zip` INT(5) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB")
        #Créer la table types
        cls.cursor.execute("CREATE TABLE `911`.`types` ( `id` INT(7) NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        #Ajouter les relations
        cls.cursor.execute("ALTER TABLE `emergencies` ADD FOREIGN KEY (`town`) REFERENCES `towns`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT")
        cls.cursor.execute("ALTER TABLE `emergencies` ADD FOREIGN KEY (`type`) REFERENCES `types`(`id`) ON DELETE RESTRICT ON UPDATE RESTRICT")
        
        cls.close_connexion()

    @classmethod
    def load_towns(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO towns VALUES (NULL, %s, %s)", data)
        cls.link.commit()
        cls.close_connexion()

    @classmethod
    def load_types(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO types VALUES (NULL, %s)", data)
        cls.link.commit()
        cls.close_connexion()

    @classmethod
    def load_emergencies(cls, data):
        cls.open_connexion()
        cls.cursor.executemany("INSERT INTO emergencies VALUES (NULL, %s, %s, %s, (SELECT id from towns WHERE name = %s), %s, (SELECT id from types WHERE name = %s))", data)
        cls.link.commit()
        cls.close_connexion()