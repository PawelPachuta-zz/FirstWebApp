from flask import session  # dekorator importujemy ze slownika session

from functools import wraps  #przy tworzeniu dekoratorów musze wykonac tą czynność

def check_logged_in(func):  #check_logged- dekorator/func-obiekt dekorowanej funkcji/fcja dekorowana
    @wraps(func)  
    def wrapper(*args, **kwargs):  #fcja zagnieżdżona
        if 'logged_in' in session:  #Jeśli użytkownik jest zalogowany...
            return func(*args, **kwargs)  #wywołuje dekorowaną funkcję
        return('Nie jesteś zalogowany')  # jeśli nie zwracam komunikat
    return wrapper  #zwracam zagnieżdżoną funkcję(obiekt funkcji)
    
