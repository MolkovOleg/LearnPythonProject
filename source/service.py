from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main_page():
    apt_image = "https://a0.muscache.com/im/pictures/miso/Hosting-947630235219886078/original/56cfe3a5-79b9-4ba7-a3f6-5fdf6d62dbdf.jpeg?im_w=1440"
    apt_address = ["улица Никольская, д.10", "Варшавский проспект, д.34", "Ленинский проспект, д.20", "улица Марата, д.54","проспект Фрунзе, д.54"]
    apt_rooms = ["1-комнатная", "2-комнатная", "3-комнатная", "4-комнатная"]
    apt_area = ["Академическая", "Московский", "Аэропорт"]
    apt_city = ['Москва', "Сочи", "Санкт-Петербург"]
    return render_template("index.html", apt_image=apt_image, apt_address=apt_address, apt_rooms=apt_rooms,
                           apt_area=apt_area, apt_city=apt_city)

if __name__ == "__main__":
    app.run(debug=True)
