from tkinter import *
import requests

token = 'TOKEN'
root = Tk()
root.geometry('550x125')
root.title('Air quality index')


def main():
    global f_town
    global f_town_label
    global f_button
    global query_label

    f_town = Entry(root, width=30)
    f_town.grid(row=0, column=1, pady=(20, 0))

    f_town_label = Label(root, text='Choose the town')
    f_town_label.grid(row=0, column=2, pady=(20, 0))

    f_button = Button(root, text='OK', command=get_town)
    f_button.grid(row=0, column=3, pady=(20, 0))

    query_label = Label(root, font=('Helvetica bold', 26), text='00')
    query_label.grid(row=0, column=0, pady=(20, 0), padx=(10, 0))


def response():
    town = f_town.get()
    global url
    global err_label
    try:
        url = f'https://api.waqi.info/feed/{town}/?token={token}'
        aqi = requests.get(url).json()['data']['aqi']
        return aqi
    except TypeError:
        err_label = Label(root, font=('Helvetica bold', 14), text='Unknown station')
        err_label.grid(row=2, column=0, columnspan=2)


def air_color(aqi):
    if aqi <= 50:
        return '#0C0'
    elif 51 < aqi <= 100:
        return '#FFFF00'
    elif 101 < aqi <= 150:
        return '#FFA600'
    elif 151 < aqi <= 200:
        return '#FF0000'
    elif 201 < aqi <= 300:
        return '#AA00FF'
    elif 301 < aqi:
        return '#964B00'


def aq_name(air_color):
    if air_color == '#0C0':
        return 'Good' + '\n' + 'quality'
    elif air_color == '#FFFF00':
        return 'Moderate' + '\n' + ' quality'
    elif air_color == '#FFA600':
        return 'Unhealthy for' + '\n' + ' sensitive groups'
    elif air_color == '#FF0000':
        return 'Unhealthy'
    elif air_color == '#AA00FF':
        return 'Very ' + '\n' + 'unhealthy'
    elif air_color == '#964B00':
        return 'Hazardous'


def get_town():
    x = air_color(response())
    aq = aq_name(air_color(response()))
    query_label.configure(font=('Helvetica bold', 26), background=x, text=response())
    root.configure(background=x)

    f_town.destroy()
    f_town_label.destroy()
    f_button.destroy()
    err_label.destroy()

    response_label = Label(root, font=('Helvetica bold', 14), text=requests.get(url).json()['data']['city']['name'],
                           background=x)
    response_label.grid(row=0, column=1, pady=(20, 0), padx=(30, 0))

    aq_label = Label(root, font=('Helvetica bold', 14), text=aq,
                     background=x)
    aq_label.grid(row=2, column=0)

    clear_button = Button(root, text='Clear', command=clear)
    clear_button.grid(row=3, column=0, columnspan=3)


def clear():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(background='white')

    main()


if __name__ == '__main__':
    main()

root.mainloop()