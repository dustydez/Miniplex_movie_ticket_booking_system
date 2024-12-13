# Miniplex_movie_ticket_booking_system

#### **Project Overview**
Miniplex is a Python-based movie ticket booking system designed to simplify the process of selecting movies, booking seats, and making payments. The project incorporates user-friendly features, an interactive interface, and efficient database management, making it an ideal solution for single-screen theatres.

---

#### **Features**
1. **Customer Features**:
   - Search and select movies based on language, genre, and show timings.
   - Book tickets by selecting available seats from a visual seating layout.
   - Payment options: UPI and credit/debit card.
   - Save tickets as screenshots or PDFs.

2. **Admin Features**:
   - Add and edit movie details, including show timings, genre, and descriptions.
   - Manage seat bookings and check revenue reports.
   - Update admin login credentials.

3. **Database Management**:
   - Tracks customer details, movie information, seat availability, and payment modes.
   - Prevents duplicate bookings and ensures data integrity.

4. **Visual Interface**:
   - Interactive pages for movie selection, ticket booking, and seat allocation.
   - Clear and simple navigation for both customers and administrators.

---

#### **Technical Details**
1. **Backend**: 
   - MySQL database with the following tables:
     - `Customerinfo`: Tracks bookings by customer.
     - `Seatinfo`: Stores reserved seats for each show.
     - `Movieinfo`: Holds details about movies, including ratings and schedules.
     - `Passwordinfo`: Secures admin login credentials.

2. **Frontend**:
   - Developed in Python using Tkinter for GUI.
   - Integrates QR codes for UPI payments and ticket information.

3. **Additional Features**:
   - QR code generation for UPI payments and ticket verification.
   - Automatic validation for seat bookings and show timing conflicts.

---

#### **Setup Instructions**
1. **Database Setup**:
   - Install MySQL and create the required tables using the provided schema.
   - Populate the database with sample data from the project code.

2. **Python Environment**:
   - Ensure Python 3.x is installed.
   - Install required libraries: `mysql-connector`, `tkinter`, `pillow`, `pyqrcode`, `tkcalendar`.

3. **Run the Application**:
   - Execute the main Python script (`Miniplex.py`) to launch the application.

---

#### **Usage**
1. **Customers**:
   - Start by searching for available movies.
   - Select seats and proceed to payment.
   - Save or print tickets for future use.

2. **Administrators**:
   - Log in to add or edit movie details.
   - View revenue reports and update passwords as needed.

---

#### **Future Enhancements**
- Expand functionality to support multi-screen theatres.
- Add customer reviews and ratings for movies.
- Implement staff management features.
- Include promotional discounts and offers.

---
