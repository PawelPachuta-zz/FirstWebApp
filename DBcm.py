import mysql.connector

class ConnectionError(Exception):  #importuje pustą klasę ConnectionError, gdzie stworzyłem własny WYJATEK CZASU WYKONANIA
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass


class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config


    def __enter__(self) -> 'cursor':
        try:  #intrukcja try-except zabezpieczy odpowiedzialny za połączenie z bazą danych
            self.conn = mysql.connector.connect(**self.configuartion)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterFaceError as err:  #odwołuje się do błędu specyficznego dla bazy danych
            raise ConnectionError(err)  # zgłaszam do niego własny wyjątek
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)
        
    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:  # jesli wystąpi błąd ProgrammingError zgłoś wyjątek SQLError
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value) # ta instrukcja elif zgłasza inny wyjątek, który mógłby wystąpić


