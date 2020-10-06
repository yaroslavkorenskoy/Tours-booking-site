from flask import Flask, render_template

from data import tours, departures, title, subtitle, description

tours_dict = tours.copy()
for id_Number, tour in tours_dict.items():
    tour['id'] = id_Number

app = Flask(__name__)

#Рендер главной
@app.route("/")
def template():
    return render_template('index.html', tours=list(tours_dict.values()), departures=departures,
                           title=title, subtitle=subtitle, description=description, tour=False)

#Рендер отправлений
@app.route('/departures/<departure>/')
def departure_title(departure):
    request_tours = [tour for tour in tours_dict.values() if tour['departure'] == departure]

    return render_template('departure.html', tours=request_tours, departures=departures,
                           departure=departures[departure], tour=False)

#Рендер туров
@app.route('/tours/<int:id>/')
def render_tour(id):
    return render_template('tour.html', tour=tours_dict[id], departures=departures)

#Рендер и форматирование цены
@app.template_filter('format_price')
def format_price(value):
    if value is None or not isinstance(value, int):
        return value
    return '{:,d} ₽'.format(value).replace(',', ' ')

#Рендер ошибок
@app.errorhandler(404)
def render_not_found(error):
    return "Увы, ошибка 404. Ничего не нашлось! Вот неудача, отправляйтесь на главную!"

@app.errorhandler(500)
def render_server_error(error):
    return "Жаль, ошибка 500. Что-то не так, но мы все починим"

#Запускаем сервер
if __name__ == '__main__':
    app.run()