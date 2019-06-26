from flask import Flask, render_template, request, escape, session
from flask import copy_current_request_context  #dekorator ten zapewnia, że żadanie HTTP, które jest aktywne gdy f-cja jest wywoływana, poztstaje aktywne gdy f-cja ta jest w późniejszym czasie wykonywana w wątku

from vsearch import search4letters
from threading import Thread

from checker import check_logged_in

from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
"""importuje klasę ConnectionError z modułu Dbcm"""

from time import sleep

app = Flask(__name__)


app.config['dbconfig'] = {'host': '127.0.0.1',  #słownik poza funkcją by inne funkcje mogły z niego korzystać
                'user': 'vsearch',
                'password': 'vsearchpasswd',
                'database': 'vsearchlogDB',}

@app.route('/login')  # URL login
def do_login() ->str:  # kod funkcji login
    session['logged_in'] = True  # wartość True dla klucza 'logged in' znajdującego się w słowniku session(powoduje zalogowanie)
    return 'Teraz jesteś zalogowany.'  # zwraca komunikat do przeglądarki


@app.route('/logout')  # URL wylogowania
def log_out():  # kod funkcji log_out
    session.pop('logged_in')  # usuwam za pomocą metody pop klucz'logged_in' ze słownika session(w ten sposób usuwa się klucze słownika(>>>dir(dict)))(( powoduje nie zalogowanie)
    return 'Jesteś wylogowany'  # zwracam komunikat do przeglądrki
    


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':

    @copy_current_request_context  # log_request loguje żadanie sieciowe i jego wyniki
    def log_request(req: 'Flask_request', res: str) -> None:  # musze umieścić f-cjie log_request w do_search w innych wypadku interpreter nie widzi zmiennych, które zostału użyte w wątku.
        sleep(15)  # to sprawia że funkcja log_request działa z 15 sekunodwym opóźnieniem
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:  #menedzer kontekstu(zawiera __init__,__enter__,__exit__).Auto. zamyka funkcje
                _SQL = """insert into log
                        (phrase, letters, ip, browser_string, results)
                        values
                        (%s, %s, %s, %s, %s)"""  # %s-arg do zmiennej. Tworze zapytanie
                cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,  #wydobywa jedynie nazwe
                                  res, ))  # wykonuje zapytanie
        except Exception as err:
            print('Coś poszło źle:', str(err))
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Oto Twoje wyniki'
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target= log_request, args=(request, results))  # kod WYKONANIA WĄTKU f-cji loq_request. Args to argumenty w postaci krotki.
        t.start()  # kod uruchamiający wątek
    except Exception as err:  # klauzula przechwytuje wszystkie wyjątki i wyświetlam komunikat poniżej gdy nastąpi BŁĄD CZASU WYKONANIA
        print('***** Logowanie się nie powiodło, wystąpił błąd:', str(err))
    return render_template('results.html',
                            the_phrase=phrase,  #the_ znajdują się w szablonie i = zmiennym w kodzie
                            the_letters=letters,
                            the_title=title,
                            the_results=results, )


"""@app.route jest dekoratorem funkcji poniżej. Funkcja do search wywoluje
funkcje search4letters i zwraca jako wynik lanuch znakowy"""


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                            the_title='Witamy na stronie internetowej search4letters!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
       with UseDatabase(app.config['dbconfig']) as cursor:
           _SQL = """select phrase, letters, ip, browser_string, results from log""" 
           cursor.execute(_SQL)  # Przesyłam zapytanie do serwera MySQL
           contents = cursor.fetchall()  # odbieram wyniki i przypisuje je do zmiennej CONTENTS
           raise Exception('Jakiś nieznany wyjątek.')
       titles = ('Fraza', 'Litery', 'Adres klienta', 'Agent użytkownika', 'Wyniki')
       return render_template('viewlog.html',
                           the_title = 'Widok logu',
                           the_row_titles = titles,
                           the_data = contents,)
    except ConnectionError as err:  # to niestandardowy wyjątek, zgłaszany gdy połączenie z bazą danych po stronie back-endu się nie powiedzie
        print('Czy twoja baza danych jest włączona? Błąd:', str(err))
    except CredentialsError as err:
        print('Problemy z identyfikatorem użytkonika lub hasłem dostępu. Błąd:', str(err))
    except SQLError as err:
        print('Czy twoje zapytania jest poprawne? Błąd:', str(err))
    except Exception as err:
        print('Coś poszło źle:', str(err))
    return 'Błąd'


app.secret_key = 'NigdyNieZgadnieszMojegoTajnegoKlucza'


if __name__ == '__main__':
    app.run(debug=True)


