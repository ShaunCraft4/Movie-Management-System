# Movie-Management-System
This is a movie management system using Python and MySQL. For the program to work please update the file "FlickIt.py" with your MySQL password. Then please run the following code one by one in the MySQL interpreter:

'''

create table Movies(Movie_ID char(5), Movie_Name varchar(100), Available_Front_Seats int, Available_Middle_Seats int, Available_Back_Seats int, Total_Available_Seats int, Show_Time time, Price int);

create table ReservationList(Customer_ID char(50), Name varchar(50), Movie_Name varchar(100), Seat_Plan varchar(50), Show_Time time, Price_Paid int, Food_And_Drinks varchar(50));

create table Refreshment_Prices(Item varchar(50), Price int);

insert into Movies Values("M000","Venom: The Last Dance", 25,50,25,100,013000,50);

insert into Movies Values("M001","The Lord Of the Rings: The Fellowship of the Ring", 25,50,25,100,024500,47);

insert into Movies Values("M002","Inception", 25,50,25,100,035000,51);

insert into Movies Values("M003","The Matrix", 25,50,25,100,050000,45);

insert into Movies Values("M004","Star Wars: Episode V - The Empire Strikes Back", 25,50,25,100,062500,49);

insert into Movies Values("M005","Interstellar",25,50,25,100,071500,54);

insert into Movies Values("M006","Inside Out 2", 25,50,25,100,083000,57);

insert into Movies Values("M007","Inside Out", 25,50,25,100,091500,55);

insert into Movies Values("M008","Openheimer", 25,50,25,100,114500,57);

insert into Movies Values("M009","Deadpool & Wolverine", 25,50,25,100,121500,51);

insert into Movies Values("M010","Despicable Me 4", 25,50,25,100,110000,49);

insert into Refreshment_Prices Values("Popcorn", 15);

insert into Refreshment_Prices Values("Slushies", 16);

insert into Refreshment_Prices Values("Milkshakes", 14);

insert into Refreshment_Prices Values("Soda", 15);

insert into Refreshment_Prices Values("Nachos", 18);

insert into Refreshment_Prices Values("Burger", 17);

insert into Refreshment_Prices Values("Hotdog", 17);

insert into Refreshment_Prices Values("Tea", 15);

insert into Refreshment_Prices Values("Coffee", 15);

insert into Refreshment_Prices Values("Fries", 16);

'''

You can add more movies and refreshments yourself using the following syntax:

'''

insert into Movies Values("MovieID(Please make sure it doesn't repeat and it is 4 characters long)","MovieName(under 100 characters long)", 25,50,25,100,(Please write the time of the movie without colons. Ex: For 12:30 write 123000. Please type this without the brackets),(Type the price of the movie in integers without brackets));

insert into Refreshment_Prices Values("FoodName(Under 50 characters)", (Please type the price of the food item without brackets in integers);

'''


Please note that for the application to work properly the monitor size should be 1920x1080 or greater.

Please note that you might need to install a few modules for the code to work. For this purpose please use the pip install command.
