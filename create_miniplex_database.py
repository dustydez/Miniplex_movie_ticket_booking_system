import mysql.connector as con

mycon = con.connect(host="localhost", user="root", passwd="password", database="projectdb")
if mycon.is_connected():
    print("Successfully connected to MySQL db")
else:
    print("Connection Unsuccessful")


def ex(y):
    cursor = mycon.cursor()
    cursor.execute(y)

ex('Drop table movieinfo')
ex('Drop table customerinfo')
ex('Drop table seatinfo')
ex("Drop table Passwordinfo")


x1 ="CREATE TABLE MOVIEINFO(Showid varchar(15) UNIQUE,Moviename varchar(50),Language varchar(10),Age_rating varchar(3),Rating int,Genre varchar(30),Description varchar(1000),Poster varchar(50),Startdate_time datetime, Duration time,Enddate_Time datetime, Trailer_link varchar(80))"
x2="CREATE TABLE customerinfo(Custid varchar(5),Showid varchar(15),Seatnos varchar(100),Cost int,Mode_of_payment varchar(25))"
x3="CREATE TABLE Seatinfo(Showid VARCHAR(15),Seatno VARCHAR(5))"
ex(x1)
ex(x2)
ex(x3)
movieinfo = (
'("01001","Doctor G","Hindi","A",4,"comedy","Uday Gupta finds himself as the lone male student in the Gynaecology department. His reluctance leads to chaos, confusion, comedy and eventually, great camaraderie with his fellow classmates.","docg.jpg","2022-11-30 21:00:00","02:03:00","2022-11-30 23:33:00","https://www.youtube.com/watch?v=XJrRrMCEmp8")',
'("01002","Black Adam","English","UA",3.5,"scifi","Nearly 5,000 years after he was bestowed with the almighty powers of the ancient gods and imprisoned just as quickly-Black Adam (Johnson) is freed from his earthly tomb, ready to unleash his unique form of justice on the modern world.","black adam.jpg","2022-11-30 14:00:00","02:04:00","2022-10-30 16:34:00", "https://www.youtube.com/watch?v=X0tOpBuYasI")',
'("01003","Kantara","Kannada","UA",4.9,"drama,action","Set in a fictional village of Dakshina Kannada, Kantara is a visual grandeur that brings alive the traditional culture of Kambla and Bhootha Kola. It is believed that Demigods are the guardians and their energies encircle the village. In the story, there is a ripple when a battle of ego swirls along tradition and culture of the land.","kantara.jpg","2022-12-12 21:00:00","02:30:00","2022-12-12 00:00:00", "https://www.youtube.com/watch?v=MTECjlKUgEE")',
'("01004","Sardar","Tamil","UA",4,"thriller,action","This film is a depiction of contrast between father and son`s beliefs. The son, a police officer, believes that any deed of his should be broadcasted whereas the father, an intelligence officer, spent thirty two years in a prison for the greater good.","Sardar.jpg","2022-11-01 14:00:00","02:46:00","2022-11-01 17:16:00", "https://www.youtube.com/watch?v=8OQzz_i3KFE")',
'("01005","Monster","Malayalam","UA",3.5,"adventure,crime","On their first wedding anniversary, Lucky Singh, an entrepreneur from Punjab walks into the lives of Anil Chandra and Bhamini. Little do they know that this man will change their future","monster.jpg","2022-12-05 21:00:00","02:15:00","2022-12-05 23:45:00", "https://www.youtube.com/watch?v=mnb0C8vs5x8")',
'("01006","Sardar","Tamil","UA",4,"thriller,action","This film is a depiction of contrast between father and son`s beliefs. The son, a police officer, believes that any deed of his should be broadcasted whereas the father, an intelligence officer, spent thirty two years in a prison for the greater good.","Sardar.jpg","2022-12-01 14:00:00","02:45:00","2022-12-01 17:15:00", "https://www.youtube.com/watch?v=8OQzz_i3KFE")',
'("01007","Monster","Malayalam","UA",3.5,"adventure,crime","On their first wedding anniversary, Lucky Singh, an entrepreneur from Punjab walks into the lives of Anil Chandra and Bhamini. Little do they know that this man will change their future","monster.jpg","2022-01-11 21:00:00", "02:15:00","2022-01-11 23:45:00", "https://www.youtube.com/watch?v=mnb0C8vs5x8")',
'("01008","Doctor G","Hindi","A",4,"comedy","Uday Gupta finds himself as the lone male student in the Gynaecology department. His reluctance leads to chaos, confusion, comedy and eventually, great camaraderie with his fellow classmates.","docg.jpg","2023-01-17 21:00:00","02:03:00","2023-01-17 23:33:00", "https://www.youtube.com/watch?v=XJrRrMCEmp8")',
'("01009","Black Adam","English","UA",3.5,"scifi","Nearly 5,000 years after he was bestowed with the almighty powers of the ancient gods and imprisoned just as quickly-Black Adam (Johnson) is freed from his earthly tomb, ready to unleash his unique form of justice on the modern world.","black adam.jpg","2023-02-20 14:00:00","02:04:00","2023-02-20 16:34:00", "https://www.youtube.com/watch?v=X0tOpBuYasI")',
'("10010","Black Adam","English","UA",3.5,"scifi","Nearly 5,000 years after he was bestowed with the almighty powers of the ancient gods and imprisoned just as quickly-Black Adam (Johnson) is freed from his earthly tomb, ready to unleash his unique form of justice on the modern world.","black adam.jpg","2023-02-20 17:00:00","02:04:00","2023-02-20 19:34:00", "https://www.youtube.com/watch?v=X0tOpBuYasI")')

for i in movieinfo:
    x = 'insert into movieinfo values' + i
    ex(x)

customerinfo=('("101","01001","H5,H6,H7",900,"UPI")',
              '("102","01002","G3,G2,G1",900,"Cash")',
              '("103","01003","H1,H2,H3",800,"Credit/Debit")',
              '("104","01004","J11,J12",600,"UPI")',
              '("105","01005","J5,J6",600,"Cash")')

for i in customerinfo:
    x = 'insert into customerinfo values' + i
    ex(x)

seatinfo=('("01001","H5")','("01001","H6")','("01001","H7")',
          '("01002","G3")',
          '("01003","H1")','("01003","H2")','("01003","H3")',
          '("01004","J11")','("01004","J12")',
          '("01005","J5")','("01005","J6")')

for i in seatinfo:
    x = 'insert into seatinfo values' + i
    ex(x)


x4 = "CREATE TABLE Passwordinfo(USERNAME VARCHAR(20),PASSWORD VARCHAR(20))"
x5 = "Insert into Passwordinfo values ('1user', '2pass')"
ex(x4)
ex(x5)

mycon.commit()
mycon.close()
