# install pillow, tkcalendar, pyqrcode
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
from tkcalendar import Calendar
from datetime import date, datetime, timedelta
import mysql.connector as con
import random
from pyqrcode import create
import os


# Entry box with default text that disappears when clicked
class PlaceholderEntry(Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder

        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)

    def clear_placeholder(self, e):
        if self.get() == self.placeholder:
            self.delete("0", "end")

    def add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)


geometry = '750x500+500+10'
root = Tk()
root.geometry(geometry)
root.title('Miniplex')
root.iconbitmap('m-logo icon.ico')
root.resizable(False, False)

# get current date
d = date.today().strftime("%d/%m/%Y")
date = [int(d[0:2]), int(d[3:5]), int(d[6:10])]


#  It helps in changing the mainframes, called in next and back
def show_frame(n, s_id=0):
    for widgets in root.winfo_children():
        widgets.destroy()

    if n == 1:
        StartUp()
    elif n == 2:
        AdminPass()
    elif n == 3:
        AdminEdit()
    elif n == 4:
        SelectMovie()
    elif n == 5:
        MovieDetails(s_id)
    elif n == 6:
        PickSeat(s_id)
    elif n == 7:
        Payment(s_id)
    elif n == 8:
        Ticket(s_id)


def exit_program():
    root.destroy()


#  1 Select bw Admin and Book tickets
def StartUp():
    F1 = Frame(root)
    F1.rowconfigure(0, weight=1, minsize=100)
    F1.rowconfigure(1, weight=1, minsize=400)
    F1.columnconfigure(0, weight=1, minsize=750)

    titleFrm = Frame(master=F1, borderwidth=1)
    Label(master=titleFrm, text='MINIPLEX', font=('Georgia', 30)).pack()
    titleFrm.grid(row=0, column=0, sticky='nsew')

    optFrm = Frame(master=F1, borderwidth=10)
    optFrm.rowconfigure(0, weight=1, minsize=400)
    optFrm.columnconfigure([0, 1], weight=1, minsize=325)

    adFrm = Frame(master=optFrm, borderwidth=1)
    Label(master=adFrm, image=admImg).pack()
    Button(master=adFrm, text='Enter Admin', width=20, command=lambda: show_frame(2)).pack()
    adFrm.grid(row=0, column=0, sticky='nsew')

    tktFrm = Frame(master=optFrm, borderwidth=1)
    Label(master=tktFrm, image=tktImg).pack()
    Button(master=tktFrm, text='Buy Ticket', width=20, command=lambda: show_frame(4)).pack()
    tktFrm.grid(row=0, column=1, sticky='nsew')

    optFrm.grid(row=1, column=0, sticky='nsew')

    F1.grid(row=0, column=0)


#  2 Enter correct username and password to gain access to admin controls
def AdminPass():
    F2 = Frame(root)
    F2.rowconfigure(0, weight=1, minsize=100)
    F2.rowconfigure(1, weight=1, minsize=150)
    F2.rowconfigure(2, weight=1, minsize=70)
    F2.rowconfigure(3, weight=1, minsize=180)
    F2.columnconfigure(0, weight=1, minsize=750)

    titleFrm = Frame(master=F2, borderwidth=1)
    Label(master=titleFrm, text='ADMIN', font=('Georgia', 30)).pack()
    titleFrm.grid(row=0, column=0, sticky='nsew')

    passFrm = Frame(master=F2, borderwidth=1)
    Label(master=passFrm, text='Username', width=10).grid(row=0, column=0, sticky='nse', pady=10)
    usernmTxt = Entry(master=passFrm, width=20)
    Label(master=passFrm, text='Password', width=10).grid(row=1, column=0, sticky='nse')
    passwdTxt = Entry(master=passFrm, width=20, show='*')
    usernmTxt.grid(row=0, column=1, sticky='nsw', pady=10)
    passwdTxt.grid(row=1, column=1, sticky='nsw')
    passFrm.grid(row=1, column=0, sticky='s')

    #  Checks if entered username and password are correct
    def checkPass():
        UN = usernmTxt.get()
        PW = passwdTxt.get()
        cur.execute('Select username from passwordinfo')
        adminUsername = cur.fetchone()
        adminUsername = adminUsername[0]
        cur.execute('Select password from passwordinfo')
        adminPass = cur.fetchone()
        adminPass = adminPass[0]

        if UN == adminUsername and PW == adminPass:
            show_frame(3)
        else:
            messagebox.showerror("Error", 'Wrong username and/or password.')

    Button(master=passFrm, text='Enter', width=5, command=checkPass).grid(row=1, column=2, sticky='nsw', padx=2)

    #  Show password checkbox
    chkFrm = Frame(F2, borderwidth=1)
    chkFrm.grid(row=2, column=0, pady=5)

    def show():
        if var.get() == 1:
            passwdTxt.config(show='')
        else:
            passwdTxt.config(show='*')

    var = IntVar()
    Checkbutton(chkFrm, text='Show Password', variable=var, command=show).pack()

    buttonFrm = Frame(master=F2, borderwidth=1)
    Button(master=buttonFrm, text='Back', width=10, command=lambda: show_frame(1)).pack(padx=5, pady=5)
    buttonFrm.grid(row=3, column=0, sticky='sw')

    F2.pack()


#  3 Admin controls: add movie, edit movie, change password and check revenue 
def AdminEdit():
    F3 = Frame(root)
    F3.rowconfigure(0, weight=1, minsize=500)
    F3.columnconfigure(0, weight=1, minsize=100)
    F3.columnconfigure(1, weight=1, minsize=650)

    # Contains buttons: Add movie, edit movie, revenue, change password, menu, exit
    optFrm = Frame(F3, bd=1, relief=RAISED)
    # Activity frame
    actFrm = Frame(F3)

    def clear_actFrm():
        for widgets in actFrm.winfo_children():
            widgets.destroy()

    # Changes bw 1: Add movie, 2: Edit movie in actFrm
    def changeFrm(n):
        clear_actFrm()

        Label(actFrm, text='Movie').grid(row=0, column=0, sticky='w')  
        Label(actFrm, text='Poster Location').grid(row=1, column=0, sticky='w')  
        Label(actFrm, text='Language').grid(row=2, column=0, sticky='w')  
        Label(actFrm, text='Age Rating').grid(row=3, column=0, sticky='w')  
        Label(actFrm, text='Rating').grid(row=4, column=0, sticky='w')  
        Label(actFrm, text='Genre').grid(row=5, column=0, sticky='w')  
        Label(actFrm, text='Description').grid(row=6, column=0, sticky='nw')  
        Label(actFrm, text='Date').grid(row=7, column=0, sticky='nw', pady=10)  
        Label(actFrm, text='Time').grid(row=8, column=0, sticky='w')  
        Label(actFrm, text='Duration').grid(row=9, column=0, sticky='w')  
        cal = Calendar(actFrm, selectmode='day', year=date[2], month=date[1], day=date[0])

        movieTxt = Entry(actFrm, width=40)
        posterTxt = Entry(actFrm, width=40)
        langTxt = Entry(actFrm, width=40)
        ageRatingFrm = Frame(actFrm)
        ratingFrm = Frame(actFrm)
        genreTxt = Entry(actFrm, width=40)
        descpTxt = Text(actFrm, height=2, width=50)

        movieTxt.grid(row=0, column=1, sticky='w')
        posterTxt.grid(row=1, column=1, sticky='w')
        langTxt.grid(row=2, column=1, sticky='w')
        ageRatingFrm.grid(row=3, column=1, sticky='w')
        ratingFrm.grid(row=4, column=1, sticky='w')
        genreTxt.grid(row=5, column=1, sticky='w')
        descpTxt.grid(row=6, column=1, sticky='w')
        cal.grid(row=7, column=1, sticky='w', pady=10)

        timeFrm = Frame(actFrm)
        timeFrm.grid(row=8, column=1, sticky='w')
        hourEntry = Entry(timeFrm, width=3)
        hourEntry.insert(0, '0')
        colonLbl = Label(timeFrm, text=':')
        minEntry = Entry(timeFrm, width=3)
        minEntry.insert(0, '0')
        hourEntry.grid(row=0, column=0, sticky='w')
        colonLbl.grid(row=0, column=1, sticky='w')
        minEntry.grid(row=0, column=2, sticky='w')
        _24Lbl = Label(timeFrm, text='(24 hours)')
        _24Lbl.grid(row=0, column=3, sticky='w')

        durationFrm = Frame(actFrm)
        durationFrm.grid(row=9, column=1, sticky='w')
        d_hourEntry = Entry(durationFrm, width=3)
        d_hourEntry.insert(0, '0')
        colonLbl = Label(durationFrm, text=':')
        d_minEntry = Entry(durationFrm, width=3)
        d_minEntry.insert(0, '0')
        d_hourEntry.grid(row=0, column=0, sticky='w')
        colonLbl.grid(row=0, column=1, sticky='w')
        d_minEntry.grid(row=0, column=2, sticky='w')

        Label(actFrm, text='Trailer link').grid(row=10, column=0, sticky='w')  
        trailerTxt = Entry(actFrm, width=40)
        trailerTxt.grid(row=10, column=1, sticky='w')

        chosenRating = IntVar()
        ratingOptions = [1, 2, 3, 4, 5]
        for rating in ratingOptions:
            Radiobutton(ratingFrm, text=rating, variable=chosenRating, value=rating).grid(row=0, column=rating)

        ageRating = StringVar()
        ageRatingOptions = ['U', 'UA', 'A', 'S']
        for rating in ageRatingOptions:
            Radiobutton(ageRatingFrm, text=rating, variable=ageRating, value=rating).grid(row=0, column=ageRatingOptions.index(rating))

        # To clear all the entry fields and reset calendar
        def clear_fields():
            movieTxt.delete(0, END)
            langTxt.delete(0, END)
            genreTxt.delete(0, END)
            descpTxt.delete(1.0, END)
            posterTxt.delete(0, END)
            hourEntry.delete(0, END)
            minEntry.delete(0, END)
            d_hourEntry.delete(0, END)
            d_minEntry.delete(0, END)
            trailerTxt.delete(0, END)
            cal.selection_set(str(date[1]) + '/' + str(date[0]) + '/' + str(date[2]))

        # To display message after movie is successfully added or edited
        def success_message(message):
            messagebox.showinfo('Success', message)
            clear_fields()

        # Add movie
        if n == 1:
            def save():
                # Get all info from input fields
                movie = movieTxt.get()
                poster_loc = posterTxt.get()
                lang = langTxt.get()
                age_rating = ageRating.get()
                rating = chosenRating.get()
                genre = genreTxt.get()
                descp = descpTxt.get('1.0', "end-1c")
                get_date = cal.selection_get()
                year = int(get_date.strftime("%Y"))
                month = int(get_date.strftime("%m"))
                day = int(get_date.strftime("%d"))
                hour = int(hourEntry.get())
                min = int(minEntry.get())
                d_hour = int(d_hourEntry.get())
                d_min = int(d_minEntry.get())
                startdate_time = datetime(year, month, day, hour, min, 0)
                duration = timedelta(hours=d_hour, minutes=d_min, seconds=0)
                enddate_time = startdate_time + duration + timedelta(minutes=30)
                trailerlink = trailerTxt.get()

                def check_slot():
                    full_slots = 'Select startdate_time, enddate_time from movieinfo'
                    cur.execute(full_slots)
                    get_slots = cur.fetchall()
                    for i in get_slots:
                        # Check if input start date time is in an unavailable slot
                        if startdate_time >= i[0] and startdate_time <= i[1]:
                            messagebox.showerror('Error', 'Slot full.')
                            return False
                        # Check if calculated end time is in unavailable slot
                        elif enddate_time >= i[0] and enddate_time.date() == i[1].date():
                            messagebox.showerror('Error', 'Slot full.')
                            return False

                slot_available = check_slot()

                # If time not written in correct format, show error message
                if int(hour) < 0 or int(hour) > 23 or int(min) < 0 or int(min) > 59:
                    messagebox.showerror("Error", 'Please enter time in 24 hour format only.')

                elif slot_available is False:
                    pass

                # Save the new movie details
                else:
                    # To make a new ShowId for the inputted movie details and enter into the movieinfo table
                    # List of existing showids
                    cur.execute('Select showid from movieinfo')
                    showids = cur.fetchall()
                    showid_list = []
                    for id in showids:
                        showid_list += id

                    # Creating new showid of 00001 type
                    while True:
                        n = random.randint(0, 10000)
                        if n not in showid_list:
                            break
                    new_id = str(n)
                    while len(new_id) < 5:
                        new_id = '0' + new_id

                    new_movie = """Insert into movieinfo values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")""".format(new_id, movie, lang, age_rating, rating, genre, descp, poster_loc, startdate_time, duration, enddate_time, trailerlink)

                    cur.execute(new_movie)
                    mycon.commit()
                    success_message('Movie successfully added.')

            Button(actFrm, text='Save', command=lambda: save(), width=8).grid(row=11, column=0, pady=5, sticky='sw', ipadx=2)

        # Edit movie details
        elif n == 2:
            # Get movie list (showid + moviename)
            def get_movie_list():
                cur.execute('Select showid, moviename from movieinfo order by showid')
                movie_list = cur.fetchall()
                Movies = []
                for i in movie_list:
                    m = i[0] + ' ' + i[1]
                    Movies += [m]

                # Dropdown menu to select movie
                Label(actFrm, text='Select Movie').grid(row=0, column=3, sticky='w')
                OptionMenu(actFrm, varMovie, *Movies, command=old_movie_info).grid(row=1, column=3, sticky='w')

            def old_movie_info(selection):
                # Removing prev selected movie info
                clear_fields()

                # Inserting new selected movie info
                showid = str(selection[0:6])
                movie_det_qry = "Select * from movieinfo where showid = {}".format(showid)
                cur.execute(movie_det_qry)
                movie_details = cur.fetchall()
                movie_details = movie_details[0]
                movieTxt.insert(0, movie_details[1])
                langTxt.insert(0, movie_details[2])
                ageRating.set(movie_details[3])
                chosenRating.set(movie_details[4])
                genreTxt.insert(0, movie_details[5])
                descpTxt.insert('1.0', movie_details[6])
                posterTxt.insert(0, movie_details[7])
                cal.selection_set(movie_details[8])
                hourEntry.insert(0, movie_details[8].strftime('%H'))
                minEntry.insert(0, movie_details[8].strftime('%M'))
                dur_list = str(movie_details[9]).split(':')
                d_hourEntry.insert(0, dur_list[0])
                d_minEntry.insert(0, dur_list[1])
                trailerTxt.insert(0, movie_details[11])

            def confirm():
                # First delete existing record corresponding to showid
                showid = varMovie.get()
                showid = showid[0:5]
                del_rec = 'Delete from movieinfo where showid={}'.format(showid)
                cur.execute(del_rec)

                # Get all info from input fields
                movie = movieTxt.get()
                poster_loc = posterTxt.get()
                lang = langTxt.get()
                age_rating = ageRating.get()
                rating = chosenRating.get()
                genre = genreTxt.get()
                descp = descpTxt.get('1.0', "end-1c")
                get_date = cal.selection_get()
                year = int(get_date.strftime("%Y"))
                month = int(get_date.strftime("%m"))
                day = int(get_date.strftime("%d"))
                hour = int(hourEntry.get())
                min = int(minEntry.get())
                d_hour = int(d_hourEntry.get())
                d_min = int(d_minEntry.get())
                startdate_time = datetime(year, month, day, hour, min, 0)
                duration = timedelta(hours=d_hour, minutes=d_min, seconds=0)
                enddate_time = startdate_time + duration + timedelta(minutes=30)
                trailer_link = trailerTxt.get()

                enter_rec = """Insert into movieinfo values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")""".format(showid, movie, lang, age_rating, rating, genre, descp, poster_loc, startdate_time, duration, enddate_time, trailer_link)
                cur.execute(enter_rec)
                mycon.commit()
                success_message('Movie successfully edited.')
                get_movie_list()

            varMovie = StringVar()
            get_movie_list()

            Button(actFrm, text='Confirm', command=lambda: confirm(), width=8).grid(row=11, column=0, pady=5, sticky='sw', ipadx=2)

   
    def check_revenue():
        def clear_displayFrm():
            for widgets in displayFrm.winfo_children():
                widgets.destroy()

        clear_actFrm()

        actFrm2 = Frame(actFrm)
        actFrm2.rowconfigure(0, weight=1, minsize=50)
        actFrm2.rowconfigure(1, weight=1, minsize=450)
        actFrm2.columnconfigure(0, weight=1, minsize=630)

        buttonFrm = Frame(actFrm2, borderwidth=1, height=100, relief=SOLID)
        displayFrm = Frame(actFrm2, height=400)

        def total_revenue():
            clear_displayFrm()

            cur.execute('Select "Rs"+SUM(cost) from customerinfo')
            total_rev = cur.fetchone()
            total_rev = 'Rs. ' + str(total_rev[0])
            Label(displayFrm, text='Total Revenue: ' + total_rev, font=18).grid(row=0, column=0, pady=10, sticky='nsew')

        def movie_revenue():
            clear_displayFrm()

            def rev_of_movie(selection):
                get_revenue = "Select SUM(cost) from customerinfo as CI, movieinfo as MI where CI.ShowId = MI.ShowId and moviename = '{}'".format(selection)
                cur.execute(get_revenue)
                movie_rev = cur.fetchall()
                movie_rev = 'Rs. ' + str(movie_rev[0][0])
                Label(displayFrm, text='Movie Revenue: ' + movie_rev, font=18).grid(row=1, column=0, pady=10, sticky='nsew')

            cur.execute('Select distinct(moviename) from movieinfo')
            movie_list = cur.fetchall()
            movies = []
            for i in movie_list:
                movies += i
            varMovie = StringVar()
            selMovieFrm = Frame(displayFrm)
            Label(selMovieFrm, text='Select Movie').grid(row=0, column=0, sticky='nsw', padx=10)
            OptionMenu(selMovieFrm, varMovie, *movies, command=rev_of_movie).grid(row=0, column=1, sticky='nsw')
            selMovieFrm.grid(row=0, column=0, sticky='nsew')

        Button(buttonFrm, text='Total Revenue', command=lambda: total_revenue()).grid(row=0, column=0, sticky='ew', pady=5, padx=20)
        Button(buttonFrm, text='Movie Revenue', command=lambda: movie_revenue()).grid(row=0, column=1, sticky='ew', padx=20)

        buttonFrm.grid(row=0, column=0, sticky='nsew')
        displayFrm.grid(row=1, column=0, sticky='nsew', ipady=20)
        actFrm2.grid(row=0, column=0, sticky='nsew')

    def update_password():
        def set_pass():
            cur.execute('Select password from passwordinfo')
            old = cur.fetchone()
            old = old[0]
            if old != oldPass.get():
                messagebox.showerror('Error', 'Please enter correct password.')
            elif newPass.get() != confirmPass.get():
                messagebox.showerror('Error', 'New password does not match confirm password.')
            elif (len(newPass.get()) > 20):
                messagebox.showerror('Error', 'Exceeding limit of 20 characters.')
            elif (len(newPass.get()) == 0):
                messagebox.showerror('Error', 'Enter new password,')
            else:
                update_pass = "Update passwordinfo set password = '{}'".format(newPass.get())
                cur.execute(update_pass)
                mycon.commit()
                messagebox.showinfo('Password', 'Password update is successful')
                clear_actFrm()

        clear_actFrm()

        Label(actFrm, text='Old Password', width=20, justify=LEFT).grid(row=0, column=0, padx=10, pady=10)
        oldPass = Entry(actFrm, width=30, show='*')
        oldPass.grid(row=0, column=1, sticky='nsw', padx=10, pady=10)
        Label(actFrm, text='New Password', width=20, justify=LEFT).grid(row=1, column=0, padx=10, pady=10)
        newPass = Entry(actFrm, width=30, show='*')
        newPass.grid(row=1, column=1, sticky='nsw', padx=10, pady=10)
        Label(actFrm, text='Confirm Password', width=20, justify=LEFT).grid(row=2, column=0, padx=10, pady=10)
        confirmPass = Entry(actFrm, width=30, show='*')
        confirmPass.grid(row=2, column=1, sticky='nsw', padx=10, pady=10)
        Button(actFrm, text='Set Password', width=20, command=lambda: set_pass()).grid(row=3, column=0, padx=10, pady=10)

    actFrm.grid(row=0, column=1, sticky='nws', padx=10, pady=10)

    Button(optFrm, text='Add Movie', command=lambda: changeFrm(1), width=9).grid(row=0, column=0, padx=15, pady=10)
    Button(optFrm, text='Edit Movie', command=lambda: changeFrm(2), width=9).grid(row=1, column=0, pady=10)
    Button(optFrm, text='Revenue', command=lambda: check_revenue(), width=9).grid(row=2, column=0, pady=10)
    Button(optFrm, text='Update password', command=lambda: update_password(), width=9, wraplength=90).grid(row=3, column=0, pady=10)

    bottomFrm = Frame(optFrm)
    Button(bottomFrm, text='Menu', command=lambda: show_frame(1), width=9).grid(row=1, column=0, sticky='s', pady=10)
    Button(bottomFrm, text='Exit', command=lambda: exit_program(), width=9).grid(row=2, column=0, sticky='s', pady=10)

    bottomFrm.grid(row=4, column=0, sticky='s', pady=205)
    optFrm.grid(row=0, column=0, sticky='nsw')

    F3.pack()


#  4 Page for customer to search and select movie
def SelectMovie():
    F4 = Frame(master=root)
    F4.rowconfigure(0, weight=1, minsize=50)
    F4.rowconfigure(1, weight=1, minsize=400)
    F4.columnconfigure(0, weight=1, minsize=750)

    #  Makes the table after retrieving reqd info like moviename, genre, lang, date, time, duration
    def make_table(data):
        for widgets in tableFrm.winfo_children():
            widgets.destroy()

        Label(tableFrm, text='Movie', width=15).grid(row=0, column=0, sticky='w')
        Label(tableFrm, text='Genre', width=15).grid(row=0, column=1, sticky='w')
        Label(tableFrm, text='Language', width=15).grid(row=0, column=2, sticky='w')
        Label(tableFrm, text='Date', width=15).grid(row=0, column=3, sticky='w')
        Label(tableFrm, text='Time', width=15).grid(row=0, column=4, sticky='w')
        Label(tableFrm, text='Duration', width=15).grid(row=0, column=5, sticky='w')

        count = 1
        for row in data:
            row = list(row)
            for i in range(1, len(row)):
                if i == 1:
                    #  num to try referring to specific button even in loop
                    movBtn = Button(tableFrm, text=row[i], width=10, wraplength=100, activebackground='white', command=lambda num=row[0]: show_frame(5, num))
                    movBtn.grid(row=count, column=0, sticky='nsew', padx=4, pady=5)
                else:
                    Label(tableFrm, text=str(row[i]).title(), wraplength=100).grid(row=count, column=(i - 1), sticky='nsew', padx=4, pady=5)
            count += 1
        Label(tableFrm, text='Search for more', fg='grey').grid(row=count, column=0, sticky='w', padx=4, pady=5)

    def search_movie():
        movie = searchBar.get()
        search = "Select showid, moviename, genre, language, cast(Startdate_time as date), cast(startdate_time as time), duration from movieinfo where moviename like '%{}%' and Startdate_time >= current_timestamp".format(movie)
        cur.execute(search)
        data = cur.fetchall()
        make_table(data)

    def default_table():
        getData = 'SELECT showid, moviename, genre, language, cast(Startdate_time as date) as date, cast(startdate_time as time) as time,duration from movieinfo where startdate_time >= current_timestamp order by startdate_time, moviename'
        cur.execute(getData)
        data = cur.fetchmany(8)  # To stick to tableFrm size limit
        make_table(data)
        cur.fetchall()  # To reach end of collected data, otherwise throws error when search_movie is used

    # Search Bar, only search movie name
    searchFrm = Frame(F4)
    searchBar = PlaceholderEntry(searchFrm, 'Search Movie', background='white', width=80, borderwidth=2)
    searchBar.grid(row=0, column=0, pady=20, sticky='ew')
    Button(searchFrm, text='Go', command=lambda: search_movie()).grid(row=0, column=1, padx=2, sticky='ew') 
    Button(searchFrm, text='Reset', command=lambda: default_table()).grid(row=0, column=2, padx=2, sticky='ew')  
    searchFrm.grid(row=0, column=0)

    # Create the movie details table
    tableFrm = Frame(F4, relief=RAISED, borderwidth=1)
    tableFrm.grid(row=1, column=0, sticky='ns', pady=10)
    default_table()

    bottomFrm = Frame(F4)
    Button(bottomFrm, text='Back', width=8, command=lambda: show_frame(1)).grid(row=0, column=0, sticky='ws', padx=5)
    bottomFrm.grid(row=2, column=0, sticky='nsew')

    F4.pack()


#  5 Select a movie in SelectMovie page, see full info here
def MovieDetails(name):
    F5 = Frame(root)
    F5.rowconfigure(0, weight=1, minsize=300)
    F5.rowconfigure(1, weight=1, minsize=100)
    F5.columnconfigure(0, weight=1, minsize=100)

    movFrm = Frame(F5, borderwidth=1)
    posFrm = Frame(F5, borderwidth=1)
    BtnFrm = Frame(F5, borderwidth=1)

    # to get the poster
    getpos = "select poster from movieinfo where showid='{}'".format(name)
    cur.execute(getpos)
    posdet = cur.fetchone()
    path = str(posdet[0])
    p = Image.open(path)
    p = p.resize((250, 350))
    posimg = ImageTk.PhotoImage(p)
    lbl = Label(posFrm, image=posimg)
    lbl.image = posimg
    lbl.grid(row=0, column=0, padx=5, pady=15, sticky='w')

    # to get the details
    getall = 'select moviename,rating,language,duration,genre,age_rating,Description from movieinfo where showid={}'.format(name)
    cur.execute(getall)
    movDet = cur.fetchone()
    index = 0
    for i in movDet:
        Label(movFrm, text=i, wraplength=350, justify=LEFT).grid(row=index, column=1, padx=2, pady=10, sticky='w')
        index += 1

    Label(movFrm, text="Title:").grid(row=0, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Rating:").grid(row=1, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Language:").grid(row=2, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Duration:").grid(row=3, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Genre:").grid(row=4, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Age Rating:").grid(row=5, column=0, sticky='w', padx=5, pady=10)
    Label(movFrm, text="Description:").grid(row=6, column=0, sticky='nw', padx=5, pady=10)

    Button(BtnFrm, text='Back', command=lambda: show_frame(4), width=10).grid(row=0, column=0, padx=50, sticky='sw')
    Button(BtnFrm, text='Next', command=lambda: show_frame(6, name), width=10).grid(row=0, column=1, padx=50, sticky='se')

    movFrm.grid(row=0, column=3, rowspan=3, columnspan=3, padx=10, sticky='nw')
    posFrm.grid(row=0, column=0, columnspan=3, sticky='w')
    BtnFrm.grid(row=1, column=4, pady=20, sticky='s')
    F5.pack()


#  6 Pick seat, store take seat info to next page(7)
def PickSeat(showid):

    F6 = Frame(root)

    # Get booked seats (unavailable seats)
    seat_qry = "Select Seatno from SeatInfo where showid = '{}'".format(showid)
    cur.execute(seat_qry)
    seats = cur.fetchall()
    booked_seats = []
    for i in seats:
        booked_seats += i

    seats = []
    Frm1 = Frame(F6)
    x = 'A'
    global premsel
    global stdsel
    premsel = []
    stdsel = []

    # changing the seats color when picked
    def click(num):
        if seats[num].cget('background') == 'orange':
            seats[num].configure(bg='green')
            premsel.append(seats[num]['text'])
        elif seats[num].cget('background') == 'light blue':
            seats[num].configure(bg='green')
            stdsel.append(seats[num]['text'])
        elif seats[num].cget('background') == 'green':
            if num <= 19:
                seats[num].configure(bg='orange')
                premsel.remove(seats[num]['text'])
            else:
                seats[num].configure(bg='light blue')
                stdsel.remove(seats[num]['text'])

        if premsel != [] or stdsel != []:
            proceedBtn['state'] = NORMAL
        elif premsel == [] and stdsel == []:
            proceedBtn['state'] = DISABLED

        # displays the no. of seats and net price
        Label(F6, text='No. of premium seats:' + " " + str(len(premsel))).grid(row=3, column=0, columnspan=1)
        Label(F6, text='No. of standard seats:' + " " + str(len(stdsel))).grid(row=4, column=0, columnspan=1)
        Label(F6, text='Net price:' + " " + str(400 * len(premsel) + 200 * len(stdsel)), width=15).grid(row=5, column=0)

    btnFrm = Frame(F6)
    btnFrm.grid(row=6, column=0)
    Button(btnFrm, text='Back', command=lambda: show_frame(4)).grid(row=0, column=0, padx=3)
    proceedBtn = Button(btnFrm, text='Proceed', command=lambda: show_frame(7, showid), state=DISABLED)
    proceedBtn.grid(row=0, column=1, padx=3)

    index = 0
    # this creates the rows of seats with default colors
    for i in range(0, 10):
        for j in range(0, 10):
            if (i <= 1):
                if x + str(j + 1) in booked_seats:
                    Btn = Button(Frm1, text=(x + str(j + 1)), height=1, width=4, fg='black', bg='red', state=DISABLED, command=lambda num=index: click(num))
                else:
                    Btn = Button(Frm1, text=(x + str(j + 1)), height=1, width=4, fg='black', bg='orange', command=lambda num=index: click(num))
            else:
                if x + str(j + 1) in booked_seats:
                    Btn = Button(Frm1, text=(x + str(j + 1)), height=1, width=4, fg='black', bg='red', state=DISABLED, command=lambda num=index: click(num))
                else:
                    Btn = Button(Frm1, text=(x + str(j + 1)), height=1, width=4, fg='black', bg='light blue', command=lambda num=index: click(num))
            seats.append(Btn)
            seats[index].grid(row=i, column=j + 2, padx=10, pady=10)
            index += 1
        x = chr(ord(x) + 1)

    Frm1.grid(row=0, column=1, rowspan=6)

    Frm2 = Frame(F6)

    # for premium
    Button(Frm2, bg='orange', height=1, width=4, state=DISABLED).grid(row=0, column=0, padx=5, pady=5)
    Label(Frm2, text='PREMIUM').grid(row=0, column=1)

    # for standard
    Button(Frm2, bg='light blue', height=1, width=4, state=DISABLED).grid(row=1, column=0, padx=5, pady=5)
    Label(Frm2, text='STANDARD').grid(row=1, column=1)

    # for booked
    Button(Frm2, bg='red', height=1, width=4, state=DISABLED).grid(row=2, column=0, padx=5, pady=5)
    Label(Frm2, text='BOOKED').grid(row=2, column=1)

    # for selected
    Button(Frm2, bg='green', height=1, width=4, state=DISABLED).grid(row=3, column=0, padx=5, pady=5)
    Label(Frm2, text='SELECTED').grid(row=3, column=1)

    Frm2.grid(row=0, column=0, padx=10)

    # the screen
    Button(F6, text='SCREEN', width=70, fg='white', bg='black', state=DISABLED).grid(row=6, column=1, padx=50, pady=10)
    # to check the tickets
    Label(F6, text='No. of premium seats:' + " " + str(len(premsel))).grid(row=3, column=0)
    Label(F6, text='No. of standard seats:' + " " + str(len(stdsel))).grid(row=4, column=0)
    Label(F6, text='').grid(row=5, column=0)

    # the prices
    Frm3 = Frame(F6)
    Label(Frm3, text='Premium - Rs. 400').grid(row=0, column=0, padx=8, pady=5)
    Label(Frm3, text='Standard - Rs. 200').grid(row=1, column=0, padx=8, pady=5)
    Frm3.grid(row=1, column=0, padx=10)

    F6.grid(row=0, column=0)


# 7 Payment, upi, credit/debit
def Payment(showid):
    F7 = Frame(root)
    F7.columnconfigure(0, weight=1, minsize=150)
    F7.columnconfigure(1, weight=1, minsize=600)

    F7.rowconfigure(0, weight=1, minsize=100)
    F7.rowconfigure(1, weight=1, minsize=300)
   

    global net
    net = 400 * len(premsel) + 200 * len(stdsel)
    global modeop
    modeop = 'na'
    global allseats
    allseats = ''

    # the side frame with the payment options:
    ModeFrm = Frame(F7, bd=1, relief=RAISED)

    # Main frame
    PayFrm = Frame(F7)

    # movie details
    DetFrm = Frame(F7, bd=1, relief=RAISED)

    # getting the seats as a string
    prem = ''
    std = ''

    for i in range(0, len(premsel)):
        if i != len(premsel) - 1:
            prem += (premsel[i] + ',')
        else:
            prem += premsel[i]
    for j in range(0, len(stdsel)):
        if j != len(stdsel) - 1:
            std += (stdsel[j] + ',')
        else:
            std += stdsel[j]

    if prem == '':
        allseats = std
    elif std == '':
        allseats = prem
    else:
        allseats = prem + "," + std
    

    getall = "Select moviename, cast(Startdate_time as date), cast(startdate_time as time), duration from movieinfo where showid={}".format(showid)
    cur.execute(getall)
    data = cur.fetchone()
 
    Label(DetFrm, text='Movie: ' + str(data[0])).grid(row=0, column=0, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Date: ' + str(data[1])).grid(row=1, column=0, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Time: ' + str(data[2])).grid(row=1, column=1, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Duration: ' + str(data[3])).grid(row=1, column=2, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Premium Seats:' + prem, wraplength=200, justify=LEFT).grid(row=2, column=0, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Standard Seats:' + std, wraplength=200, justify=LEFT).grid(row=2, column=1, padx=20, pady=5, sticky='w')
    Label(DetFrm, text='Price: Rs. ' + str(net)).grid(row=0, column=1, padx=20, pady=5, sticky='w')

    def pay(n):
        global modeop
        for widgets in PayFrm.winfo_children():
            widgets.destroy()

        BottomFrm = Frame(PayFrm)
        UFrm = Frame(PayFrm)

        if n == 1:
            modeop = 'UPI'
            Label(UFrm, text='Scan the QR code given to pay:').pack(padx=10)
            qr = create('https://youtu.be/dQw4w9WgXcQ')
            code = qr.xbm(scale=5)
            xbm_image = BitmapImage(data=code, foreground='light blue', background='black')
            Lbl = Label(UFrm)
            Lbl.image = xbm_image
            Lbl.configure(image=xbm_image)
            Lbl.pack(padx=10, pady=10)
            Label(UFrm, text='Miniplex_07010@gmail.com', font=('times', 15)).pack(padx=10, pady=10)
            Button(BottomFrm, text='Proceed', width=10, command=lambda: show_frame(8, showid)).pack()

        elif n == 2:

            # converts credit card name to upper
            def upper(*args):
                namevar.set(namevar.get().upper())

            # checks digits for all numeric entries
            def num(chk1, chk2, chk3, chk4):
                if (chk1.isdigit() is False or chk2.isdigit() is False or chk3.isdigit() is False or chk4.isdigit() is False):
                    return False

            # checks expiry and date validity of mm and yyyy entries
            def expiry(mon, year):
                mon = int(mon)
                if (mon < 1 or mon > 12) or (len(year) > 4 or int(year) < date[2]) or int(year) > date[2] + 10:
                    Label(BottomFrm, text='Enter valid dates only').grid(row=1, column=0, sticky='nsew', pady=7)
                    return False

                elif mon < date[1] and int(year) == date[2]:
                    Label(BottomFrm, text='Expired').grid(row=1, column=0, sticky='nsew', pady=7)
                    return False

            # checks for numbers in name
            def namechk(nm):
                for i in nm:
                    if i.isdigit():
                        return True
                        break

            # proceed button check
            def proceed():
                check = 0
                if (Cnum.get() != '' and Cnum.get() != 'Enter credit card number:' and Name.get() != ''
                        and Name.get() != 'NAME ON THE CARD:' and Cnum1.get() != '' and Cnum1.get() != 'MM'
                        and Cnum2.get() != '' and Cnum2.get() != 'YYYY' and Cnum3.get() != '' and Cnum3.get() != 'CVV'):
                    if num(Cnum.get(), Cnum1.get(), Cnum2.get(), Cnum3.get()) == False:
                        check = 0
                        Label(BottomFrm, text='Enter numeric values only').grid(row=1, column=0, sticky='nsew', pady=7)

                    elif len(Cnum.get()) < 12 or len(Cnum.get()) > 16:
                        check = 0
                        Label(BottomFrm, text='Invalid credit card length').grid(row=1, column=0, sticky='nsew', pady=7)

                    elif namechk(Name.get()):
                        check = 0
                        Label(BottomFrm, text='Invalid name').grid(row=1, column=0, sticky='nsew', pady=7)

                    elif expiry(Cnum1.get(), Cnum2.get()) == False:
                        check = 0

                    elif len(Cnum3.get()) != 3:
                        Label(BottomFrm, text='Invalid cvv length').grid(row=1, column=0, sticky='nsew', pady=7)
                        check = 0

                    else:
                        check = 1

                else:
                    Label(BottomFrm, text='Please fill in the details correctly').grid(row=1, column=0, sticky='nsew', pady=7)

                if check == 1:
                    show_frame(8, showid)

            modeop = 'Credit/Debit'
            Label(UFrm, text='Enter your card details:').grid(row=0, column=0, padx=10, pady=10, sticky='w')
            UFrm.config(bd=1, relief=GROOVE)

            Label(UFrm, text='Card Number:').grid(row=1, column=0, padx=10, pady=10, sticky='w')
            Cnum = PlaceholderEntry(UFrm, 'Enter credit card number:', width=60)
            Cnum.grid(row=2, column=0, padx=10, pady=20, columnspan=10)

            namevar = StringVar(UFrm)
            Name = PlaceholderEntry(UFrm, 'NAME ON THE CARD:', width=60, textvariable=namevar)
            namevar.trace('w', upper)
            Name.grid(row=3, column=0, padx=10, pady=20, columnspan=10)

            Label(UFrm, text='Expiry:').grid(row=4, column=0, padx=10, pady=10, sticky='w')
            Cnum1 = PlaceholderEntry(UFrm, 'MM', width=7)
            Cnum1.grid(row=5, column=0, padx=10, pady=10, sticky='w')
            Label(UFrm, text=' / ').grid(row=5, column=0)
            Cnum2 = PlaceholderEntry(UFrm, 'YYYY', width=7)
            Cnum2.grid(row=5, column=0, padx=5, pady=10, sticky='e')
            Label(UFrm, text='CVV:').grid(row=4, column=1, padx=70, pady=10, sticky='w')
            Cnum3 = PlaceholderEntry(UFrm, 'CVV', width=10)
            Cnum3.grid(row=5, column=1, padx=70, pady=10, sticky='w')

            Btn = Button(BottomFrm, text='Proceed', width=10, command=proceed)
            Btn.grid(row=0, column=0, sticky='nsew')

        UFrm.pack(pady=20)
        BottomFrm.pack(pady=10)

    Label(ModeFrm, text='Modes of payment:').grid(row=0, column=0, padx=20, pady=20)
 
    Button(ModeFrm, text='UPI', width=10, command=lambda: pay(1)).grid(row=1, column=0, padx=20, pady=15)
   
    Button(ModeFrm, text='Credit', width=10, command=lambda: pay(2)).grid(row=2, column=0, padx=20, pady=15)

    BottomFrm = Frame(ModeFrm)
    Button(BottomFrm, text='Back', width=10, command=lambda: show_frame(6, showid)).grid(row=4, column=0, padx=20, pady=10, sticky='s')
    BottomFrm.grid(row=4, column=0, sticky='s', pady=230)
    ModeFrm.grid(row=0, column=0, sticky='nsew', rowspan=2)
    DetFrm.grid(row=0, column=1, sticky='nsew')
    PayFrm.grid(row=1, column=1, sticky='nsew')
    F7.pack()


def Ticket(showid):
    F8 = Frame(root, background='black')

    # Updating db
    get = 'select MAX(custid) from customerinfo'
    cur.execute(get)
    cid = cur.fetchone()
    cust = str(int(cid[0]) + 1)

    give = "insert into customerinfo values ('{}','{}','{}',{},'{}')".format(cust, showid, allseats, net, modeop)
    cur.execute(give)

    #update the seats booked, in picking seats these are red
    for i in premsel:
        giving = "insert into seatinfo values ('{}','{}')".format(showid, i)
        cur.execute(giving)
    for i in stdsel:
        giving = "insert into seatinfo values ('{}','{}')".format(showid, i)
        cur.execute(giving)
    mycon.commit()

    F8.columnconfigure(0, weight=1)
    F8.columnconfigure(1, weight=3)
    F8.columnconfigure(2, weight=1)
    F8.rowconfigure(0, weight=1)
    F8.rowconfigure(1, weight=1)  
    F8.rowconfigure(2, weight=5)
    F8.rowconfigure(3, weight=4)

    titleFrm = Frame(F8, bg='black')
    thankFrm = Frame(F8, bg='black')
    bodyFrm = Frame(F8, bg='black')
    body1Frm = Frame(bodyFrm, bg="white")
    body2Frm = Frame(bodyFrm, bg="white", relief=RAISED)
    pdfFrm = Frame(F8, bg='black')
    leftFrm = Frame(F8, bg='black')
    rightFrm = Frame(F8, bg='black')

    bodyFrm.columnconfigure(0, weight=1)
    bodyFrm.columnconfigure(1, weight=1)
   
    titleFrm.grid(row=0, column=1, sticky='WENS')
    thankFrm.grid(row=1, column=1, sticky='WENS')
    bodyFrm.grid(row=2, column=1, sticky='WENS')
    body1Frm.grid(row=0, column=0, sticky='wens')
    body2Frm.grid(row=0, column=1, sticky='wens')

    pdfFrm.grid(row=3, column=1, sticky='WENS')
    leftFrm.grid(row=0, column=0, rowspan=4, sticky='WENS')
    rightFrm.grid(row=0, column=2, rowspan=4, sticky='WENS')

    Label(titleFrm, text='MINIPLEX', font=('Georgia', 30,)).pack(fill=X, pady=20)
    Label(thankFrm, text="Thank you for your purchase!!", font=("Cascadia Mono SemiBold", 15), background="lightgreen").pack(fill=X)
    q1 = " SELECT Moviename,Startdate_time,duration,Custid,Seatnos,Mode_of_payment,Cost from movieinfo natural join customerinfo where Custid='{}';".format(cust)

    cur.execute(q1)
    paylist = cur.fetchall()
    # output values for diff labels
    Label(body1Frm, text=paylist[0][0], font=("Britannic Bold", 20), bg='white').grid(row=0, column=0, padx=20, sticky='w')
    Label(body1Frm, text="Miniplex,HSR LAYOUT,5th street,Bangalore", font=("Bodoni MT", 15), bg='white').grid(row=1, column=0, padx=20, sticky='w')
    Label(body1Frm, text='{:%b %d, %Y}'.format(paylist[0][1]), font=("Bodoni MT", 15), bg='white').grid(row=2, column=0, padx=20, sticky='w')
    Label(body1Frm, text=str(paylist[0][2]), font=("Bodoni MT", 15), bg='white').grid(row=3, column=0, padx=20, sticky='w')
    Label(body1Frm, text="Customer ID: {}".format(paylist[0][3]), font=("Bodoni MT", 15), bg='white').grid(row=4, column=0, padx=20, sticky='w')
    Label(body1Frm, text="Payment mode: {}".format(paylist[0][5]), font=("Bodoni MT", 15), bg='white').grid(row=5, column=0, padx=20, sticky='w')
    Label(body1Frm, text="Seats:{}".format(paylist[0][4]), font=("Bodoni MT", 15), bg='white', justify=LEFT, wraplength=400).grid(row=6, column=0, padx=20, sticky='w')
    Label(body1Frm, text="Amount: Rs {}".format(paylist[0][6]), font=("Bodoni MT", 15), bg='white').grid(row=7, column=0, padx=20, sticky='w')

    get_link_qry = "Select trailer_link from movieinfo where showid='{}'".format(showid)
    cur.execute(get_link_qry)
    trailer_link = cur.fetchone()
    trailer_link = trailer_link[0]

    qr = create(trailer_link + '+' + paylist[0][3])

    with open('baseqr.png', 'wb') as f:
        qr.png(f, scale=10)

    limg = Image.open('baseqr.png')
    width, height = limg.size
    logo_size = 150
    logo = Image.open('m-logo.png')

    # Calculate xmin, ymin, xmax, ymax to put the logo
    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    # resize the logo 
    logo = logo.resize((xmax - xmin, ymax - ymin))

    # put the logo in the qr code
    limg.paste(logo, (xmin, ymin, xmax, ymax))
    limg.save('saved qr.png')

    trial = Image.open('saved qr.png')
    trial = trial.resize((220, 200))
    timg = ImageTk.PhotoImage(trial)

    qrLbl = Label(body2Frm)
    qrLbl.image = timg
    qrLbl.configure(image=timg)
    qrLbl.pack(pady=30, padx=30)

    def download(format):
        bodyFrm.update()
        # Maths change based off system, 1.5 for ash, 3 for lav, none for aan
        x1 = bodyFrm.winfo_rootx() * 1.5
        y1 = bodyFrm.winfo_rooty() * 1.5
        x2 = bodyFrm.winfo_reqwidth() * 1.5 + x1
        y2 = bodyFrm.winfo_reqheight() * 1.5 + y1
        dimensions = (x1, y1, x2, y2)

        download_folder = os.path.expanduser("~") + "/Downloads/"  # Gives path of download folder
        img_name = download_folder + str(paylist[0][0]) + str(datetime.now().strftime("%m %d %Y %H %M %S")) + format
        image = ImageGrab.grab(bbox=dimensions)
        image.save(img_name)

        messagebox.showinfo('Ticket', 'Please check the download folder for your ticket.')

    mycon.close()

    Button(pdfFrm, text='Take Screenshot', bg='lightgreen', font=("Cascadia Mono SemiBold", 15), command=lambda: download('.png'), width=32).grid(row=0, column=0, sticky='nsew', padx=7)
    Button(pdfFrm, text="Print Ticket", bg="lightgreen", font=("Cascadia Mono SemiBold", 15), command=lambda: download('.pdf'), width=32).grid(row=0, column=1, sticky='nsew')

    if os.path.exists('saved qr.png') and os.path.exists('baseqr.png'):
        os.remove('saved qr.png')
        os.remove('baseqr.png')

    F8.pack(fill=BOTH, expand=True)


adm = Image.open('icon-admin.png')
adm = adm.resize((200, 200))
admImg = ImageTk.PhotoImage(adm)

tkt = Image.open('icon-tickets-png.webp')
tkt = tkt.resize((200, 200))
tktImg = ImageTk.PhotoImage(tkt)

mycon = con.connect(host="localhost", user="root", passwd="password", database="projectdb")
if mycon.is_connected():
    cur = mycon.cursor()
    StartUp()  

root.mainloop()
