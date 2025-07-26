#!/usr/bin/env python3
"""
Hotel Management System - Hotel Module
This module contains the HotelManager class, which serves as the central
controller for the hotel management system.
"""

import os
import json
import datetime
from uuid import uuid4
from room import Room
from guest import Guest
from booking import Booking
from database import Database

class Bill:
    """Class representing a bill for a booking."""
    
    def __init__(self, bill_id, booking_id, amount, status="UNPAID"):
        """Initialize a new Bill object."""
        self.bill_id = bill_id
        self.booking_id = booking_id
        self.amount = amount
        self.status = status
        self.payment_date = None
    
    def to_dict(self):
        """Convert the Bill object to a dictionary."""
        return {
            "bill_id": self.bill_id,
            "booking_id": self.booking_id,
            "amount": self.amount,
            "status": self.status,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Bill object from a dictionary."""
        bill = cls(data["bill_id"], data["booking_id"], data["amount"], data["status"])
        if data["payment_date"]:
            bill.payment_date = datetime.datetime.fromisoformat(data["payment_date"]).date()
        return bill

class HotelManager:
    """
    HotelManager class that manages all hotel operations.
    
    This class serves as the central controller for the hotel management system,
    handling rooms, guests, bookings, and billing operations.
    """
    
    def __init__(self):
        """Initialize the HotelManager with a database connection."""
        self.db = Database()
        self.rooms = []
        self.guests = []
        self.bookings = []
        self.bills = []
        self.load_data()
    
    def load_data(self):
        """Load all data from the database."""
        self.rooms = self.db.load_rooms()
        self.guests = self.db.load_guests()
        self.bookings = self.db.load_bookings()
        self.bills = self.db.load_bills()
    
    def save_data(self):
        """Save all data to the database."""
        self.db.save_rooms(self.rooms)
        self.db.save_guests(self.guests)
        self.db.save_bookings(self.bookings)
        self.db.save_bills(self.bills)
    
    # Room Management Methods
    
    def add_room(self, room_number, room_type, price):
        """
        Add a new room to the hotel.
        
        Args:
            room_number (str): The room number
            room_type (str): The type of room (Single, Double, Suite, etc.)
            price (float): The price per night
            
        Returns:
            bool: True if the room was added successfully, False otherwise
        """
        if self.find_room(room_number):
            print(f"Room {room_number} already exists.")
            return False
        
        room = Room(room_number, room_type, float(price))
        self.rooms.append(room)
        self.save_data()
        return True
    
    def update_room(self, room_number, room_type=None, price=None):
        """
        Update an existing room's details.
        
        Args:
            room_number (str): The room number to update
            room_type (str, optional): The new room type
            price (float, optional): The new price per night
            
        Returns:
            bool: True if the room was updated successfully, False otherwise
        """
        room = self.find_room(room_number)
        if not room:
            print(f"Room {room_number} not found.")
            return False
        
        if room_type and room_type.strip():
            room.type = room_type
        
        if price and price.strip():
            try:
                room.price = float(price)
            except ValueError:
                print("Invalid price format. Price not updated.")
        
        self.save_data()
        return True
    
    def find_room(self, room_number):
        """
        Find a room by its number.
        
        Args:
            room_number (str): The room number to find
            
        Returns:
            Room: The room object if found, None otherwise
        """
        for room in self.rooms:
            if room.number == room_number:
                return room
        return None
    
    def view_all_rooms(self):
        """Display all rooms in the hotel."""
        if not self.rooms:
            print("No rooms available.")
            return
        
        print("\nROOM LIST:")
        print("-" * 60)
        print(f"{'Number':<10} {'Type':<15} {'Price':<10} {'Status':<10}")
        print("-" * 60)
        
        for room in self.rooms:
            status = "Occupied" if room.is_occupied else "Available"
            print(f"{room.number:<10} {room.type:<15} ${room.price:<9.2f} {status:<10}")
    
    # Guest Management Methods
    
    def add_guest(self, name, phone, email, address):
        """
        Register a new guest.
        
        Args:
            name (str): Guest's full name
            phone (str): Guest's phone number
            email (str): Guest's email address
            address (str): Guest's physical address
            
        Returns:
            str: The guest ID if registration was successful
        """
        guest_id = str(uuid4())[:8]  # Generate a unique ID
        guest = Guest(guest_id, name, phone, email, address)
        self.guests.append(guest)
        self.save_data()
        return guest_id
    
    def update_guest(self, guest_id, name=None, phone=None, email=None, address=None):
        """
        Update an existing guest's information.
        
        Args:
            guest_id (str): The guest ID to update
            name (str, optional): The new name
            phone (str, optional): The new phone number
            email (str, optional): The new email address
            address (str, optional): The new physical address
            
        Returns:
            bool: True if the guest was updated successfully, False otherwise
        """
        guest = self.find_guest(guest_id)
        if not guest:
            print(f"Guest with ID {guest_id} not found.")
            return False
        
        if name and name.strip():
            guest.name = name
        
        if phone and phone.strip():
            guest.phone = phone
        
        if email and email.strip():
            guest.email = email
        
        if address and address.strip():
            guest.address = address
        
        self.save_data()
        return True
    
    def find_guest(self, guest_id):
        """
        Find a guest by their ID.
        
        Args:
            guest_id (str): The guest ID to find
            
        Returns:
            Guest: The guest object if found, None otherwise
        """
        for guest in self.guests:
            if guest.guest_id == guest_id:
                return guest
        return None
    
    def search_guest(self, search_term):
        """
        Search for guests by name or ID.
        
        Args:
            search_term (str): The name or ID to search for
            
        Returns:
            list: A list of matching guest objects
        """
        results = []
        
        for guest in self.guests:
            if (search_term.lower() in guest.name.lower() or 
                search_term == guest.guest_id):
                results.append(guest)
        
        if not results:
            print(f"No guests found matching '{search_term}'.")
        else:
            print("\nSEARCH RESULTS:")
            print("-" * 80)
            print(f"{'ID':<10} {'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<20}")
            print("-" * 80)
            
            for guest in results:
                print(f"{guest.guest_id:<10} {guest.name:<20} {guest.phone:<15} {guest.email:<25} {guest.address:<20}")
        
        return results
    
    def view_all_guests(self):
        """Display all registered guests."""
        if not self.guests:
            print("No guests registered.")
            return
        
        print("\nGUEST LIST:")
        print("-" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<20}")
        print("-" * 80)
        
        for guest in self.guests:
            print(f"{guest.guest_id:<10} {guest.name:<20} {guest.phone:<15} {guest.email:<25} {guest.address:<20}")
    
    # Booking Management Methods
    
    def create_booking(self, guest_id, room_number, check_in, check_out):
        """
        Create a new booking.
        
        Args:
            guest_id (str): The guest ID
            room_number (str): The room number
            check_in (str): Check-in date in YYYY-MM-DD format
            check_out (str): Check-out date in YYYY-MM-DD format
            
        Returns:
            str: The booking ID if creation was successful, None otherwise
            
        Raises:
            ValueError: If the date format is invalid or check-out is before check-in
        """
        guest = self.find_guest(guest_id)
        if not guest:
            print(f"Guest with ID {guest_id} not found.")
            return None
        
        room = self.find_room(room_number)
        if not room:
            print(f"Room {room_number} not found.")
            return None
        
        try:
            check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
            
            if check_out_date <= check_in_date:
                raise ValueError("Check-out date must be after check-in date.")
            
            # Check if the room is available for the requested dates
            if not self.is_room_available(room_number, check_in_date, check_out_date):
                print(f"Room {room_number} is not available for the selected dates.")
                return None
            
            booking_id = str(uuid4())[:8]  # Generate a unique ID
            booking = Booking(booking_id, guest_id, room_number, check_in_date, check_out_date)
            self.bookings.append(booking)
            self.save_data()
            return booking_id
            
        except ValueError as e:
            raise ValueError(f"Invalid date format. Please use YYYY-MM-DD format. {str(e)}")
    
    def update_booking(self, booking_id, check_in=None, check_out=None):
        """
        Update an existing booking.
        
        Args:
            booking_id (str): The booking ID to update
            check_in (str, optional): The new check-in date
            check_out (str, optional): The new check-out date
            
        Returns:
            bool: True if the booking was updated successfully, False otherwise
            
        Raises:
            ValueError: If the date format is invalid or check-out is before check-in
        """
        booking = self.find_booking(booking_id)
        if not booking:
            print(f"Booking with ID {booking_id} not found.")
            return False
        
        check_in_date = booking.check_in
        check_out_date = booking.check_out
        
        if check_in and check_in.strip():
            try:
                check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid check-in date format. Please use YYYY-MM-DD format.")
        
        if check_out and check_out.strip():
            try:
                check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid check-out date format. Please use YYYY-MM-DD format.")
        
        if check_out_date <= check_in_date:
            raise ValueError("Check-out date must be after check-in date.")
        
        # Check if the room is available for the new dates
        if not self.is_room_available(booking.room_number, check_in_date, check_out_date, exclude_booking_id=booking_id):
            print(f"Room {booking.room_number} is not available for the selected dates.")
            return False
        
        booking.check_in = check_in_date
        booking.check_out = check_out_date
        self.save_data()
        return True
    
    def cancel_booking(self, booking_id):
        """
        Cancel an existing booking.
        
        Args:
            booking_id (str): The booking ID to cancel
            
        Returns:
            bool: True if the booking was cancelled successfully, False otherwise
        """
        booking = self.find_booking(booking_id)
        if not booking:
            print(f"Booking with ID {booking_id} not found.")
            return False
        
        # Remove the booking from the list
        self.bookings = [b for b in self.bookings if b.booking_id != booking_id]
        self.save_data()
        return True
    
    def find_booking(self, booking_id):
        """
        Find a booking by its ID.
        
        Args:
            booking_id (str): The booking ID to find
            
        Returns:
            Booking: The booking object if found, None otherwise
        """
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    def search_booking(self, search_term):
        """
        Search for bookings by ID, guest ID, or room number.
        
        Args:
            search_term (str): The ID, guest ID, or room number to search for
            
        Returns:
            list: A list of matching booking objects
        """
        results = []
        
        for booking in self.bookings:
            if (search_term == booking.booking_id or 
                search_term == booking.guest_id or 
                search_term == booking.room_number):
                results.append(booking)
        
        if not results:
            print(f"No bookings found matching '{search_term}'.")
        else:
            print("\nSEARCH RESULTS:")
            print("-" * 80)
            print(f"{'ID':<10} {'Guest ID':<10} {'Room':<10} {'Check-in':<12} {'Check-out':<12} {'Status':<10}")
            print("-" * 80)
            
            for booking in results:
                status = "Active" if booking.is_active else "Completed"
                print(f"{booking.booking_id:<10} {booking.guest_id:<10} {booking.room_number:<10} {booking.check_in.isoformat():<12} {booking.check_out.isoformat():<12} {status:<10}")
        
        return results
    
    def view_all_bookings(self):
        """Display all bookings."""
        if not self.bookings:
            print("No bookings available.")
            return
        
        print("\nBOOKING LIST:")
        print("-" * 80)
        print(f"{'ID':<10} {'Guest ID':<10} {'Room':<10} {'Check-in':<12} {'Check-out':<12} {'Status':<10}")
        print("-" * 80)
        
        for booking in self.bookings:
            status = "Active" if booking.is_active else "Completed"
            print(f"{booking.booking_id:<10} {booking.guest_id:<10} {booking.room_number:<10} {booking.check_in.isoformat():<12} {booking.check_out.isoformat():<12} {status:<10}")
    
    def is_room_available(self, room_number, check_in, check_out, exclude_booking_id=None):
        """
        Check if a room is available for the given dates.
        
        Args:
            room_number (str): The room number to check
            check_in (datetime.date): The check-in date
            check_out (datetime.date): The check-out date
            exclude_booking_id (str, optional): A booking ID to exclude from the check
            
        Returns:
            bool: True if the room is available, False otherwise
        """
        for booking in self.bookings:
            if booking.room_number == room_number:
                # Skip the booking if it's the one we're updating
                if exclude_booking_id and booking.booking_id == exclude_booking_id:
                    continue
                
                # Check if there's an overlap in dates
                if (check_in < booking.check_out and check_out > booking.check_in):
                    return False
        
        return True
    
    # Billing Methods
    
    def generate_bill(self, booking_id):
        """
        Generate a bill for a booking.
        
        Args:
            booking_id (str): The booking ID to generate a bill for
            
        Returns:
            Bill: The generated bill object if successful, None otherwise
        """
        booking = self.find_booking(booking_id)
        if not booking:
            print(f"Booking with ID {booking_id} not found.")
            return None
        
        # Check if a bill already exists for this booking
        for bill in self.bills:
            if bill.booking_id == booking_id:
                print(f"Bill already exists for booking {booking_id}.")
                return bill
        
        # Calculate the total amount
        room = self.find_room(booking.room_number)
        if not room:
            print(f"Room {booking.room_number} not found.")
            return None
        
        # Calculate the number of days
        days = (booking.check_out - booking.check_in).days
        amount = days * room.price
        
        # Generate a unique bill ID
        bill_id = str(uuid4())[:8]
        bill = Bill(bill_id, booking_id, amount)
        self.bills.append(bill)
        self.save_data()
        
        print(f"\nBILL DETAILS:")
        print("-" * 60)
        print(f"Bill ID: {bill.bill_id}")
        print(f"Booking ID: {bill.booking_id}")
        print(f"Guest ID: {booking.guest_id}")
        print(f"Room Number: {booking.room_number}")
        print(f"Check-in Date: {booking.check_in.isoformat()}")
        print(f"Check-out Date: {booking.check_out.isoformat()}")
        print(f"Number of Days: {days}")
        print(f"Room Rate per Night: ${room.price:.2f}")
        print(f"Total Amount: ${bill.amount:.2f}")
        print(f"Status: {bill.status}")
        print("-" * 60)
        
        return bill
    
    def process_payment(self, bill_id, amount):
        """
        Process a payment for a bill.
        
        Args:
            bill_id (str): The bill ID to process payment for
            amount (float): The payment amount
            
        Returns:
            bool: True if the payment was processed successfully, False otherwise
        """
        bill = None
        for b in self.bills:
            if b.bill_id == bill_id:
                bill = b
                break
        
        if not bill:
            print(f"Bill with ID {bill_id} not found.")
            return False
        
        if bill.status == "PAID":
            print(f"Bill with ID {bill_id} is already paid.")
            return False
        
        if amount < bill.amount:
            print(f"Payment amount (${amount:.2f}) is less than the bill amount (${bill.amount:.2f}).")
            return False
        
        bill.status = "PAID"
        bill.payment_date = datetime.datetime.now().date()
        self.save_data()
        
        print(f"\nPAYMENT DETAILS:")
        print("-" * 60)
        print(f"Bill ID: {bill.bill_id}")
        print(f"Amount Paid: ${amount:.2f}")
        print(f"Payment Date: {bill.payment_date.isoformat()}")
        print(f"Status: {bill.status}")
        print("-" * 60)
        
        return True
    
    def view_all_bills(self):
        """Display all bills."""
        if not self.bills:
            print("No bills available.")
            return
        
        print("\nBILL LIST:")
        print("-" * 80)
        print(f"{'Bill ID':<10} {'Booking ID':<10} {'Amount':<10} {'Status':<10} {'Payment Date':<12}")
        print("-" * 80)
        
        for bill in self.bills:
            payment_date = bill.payment_date.isoformat() if bill.payment_date else "N/A"
            print(f"{bill.bill_id:<10} {bill.booking_id:<10} ${bill.amount:<9.2f} {bill.status:<10} {payment_date:<12}")
    
    # Report Methods
    
    def generate_occupancy_report(self):
        """Generate and display an occupancy report."""
        if not self.rooms:
            print("No rooms available.")
            return
        
        total_rooms = len(self.rooms)
        occupied_rooms = 0
        
        today = datetime.datetime.now().date()
        
        for room in self.rooms:
            for booking in self.bookings:
                if (booking.room_number == room.number and 
                    booking.check_in <= today <= booking.check_out):
                    occupied_rooms += 1
                    break
        
        occupancy_rate = (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0
        
        print("\nOCCUPANCY REPORT:")
        print("-" * 60)
        print(f"Date: {today.isoformat()}")
        print(f"Total Rooms: {total_rooms}")
        print(f"Occupied Rooms: {occupied_rooms}")
        print(f"Available Rooms: {total_rooms - occupied_rooms}")
        print(f"Occupancy Rate: {occupancy_rate:.2f}%")
        print("-" * 60)
        
        # Room type breakdown
        room_types = {}
        for room in self.rooms:
            room_type = room.type
            if room_type not in room_types:
                room_types[room_type] = {"total": 0, "occupied": 0}
            
            room_types[room_type]["total"] += 1
            
            for booking in self.bookings:
                if (booking.room_number == room.number and 
                    booking.check_in <= today <= booking.check_out):
                    room_types[room_type]["occupied"] += 1
                    break
        
        print("\nROOM TYPE BREAKDOWN:")
        print("-" * 60)
        print(f"{'Room Type':<15} {'Total':<10} {'Occupied':<10} {'Available':<10} {'Occupancy Rate':<15}")
        print("-" * 60)
        
        for room_type, data in room_types.items():
            occupancy_rate = (data["occupied"] / data["total"]) * 100 if data["total"] > 0 else 0
            print(f"{room_type:<15} {data['total']:<10} {data['occupied']:<10} {data['total'] - data['occupied']:<10} {occupancy_rate:.2f}%")
    
    def generate_revenue_report(self, start_date, end_date):
        """
        Generate and display a revenue report for a specific period.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Raises:
            ValueError: If the date format is invalid
        """
        try:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
            if end < start:
                raise ValueError("End date must be after start date.")
        except ValueError as e:
            raise ValueError(f"Invalid date format. Please use YYYY-MM-DD format. {str(e)}")
        
        total_revenue = 0
        paid_bills = 0
        unpaid_bills = 0
        
        # Revenue by room type
        room_type_revenue = {}
        
        for bill in self.bills:
            # Find the booking for this bill
            booking = self.find_booking(bill.booking_id)
            if not booking:
                continue
            
            # Check if the payment date falls within the specified period
            if bill.status == "PAID" and bill.payment_date and start <= bill.payment_date <= end:
                total_revenue += bill.amount
                paid_bills += 1
                
                # Find the room for this booking
                room = self.find_room(booking.room_number)
                if room:
                    room_type = room.type
                    if room_type not in room_type_revenue:
                        room_type_revenue[room_type] = 0
                    room_type_revenue[room_type] += bill.amount
            
            # Count unpaid bills for bookings within the period
            if bill.status == "UNPAID" and booking.check_in <= end and booking.check_out >= start:
                unpaid_bills += 1
        
        print("\nREVENUE REPORT:")
        print("-" * 60)
        print(f"Period: {start.isoformat()} to {end.isoformat()}")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Paid Bills: {paid_bills}")
        print(f"Unpaid Bills: {unpaid_bills}")
        print("-" * 60)
        
        if room_type_revenue:
            print("\nREVENUE BY ROOM TYPE:")
            print("-" * 60)
            print(f"{'Room Type':<15} {'Revenue':<15} {'Percentage':<15}")
            print("-" * 60)
            
            for room_type, revenue in room_type_revenue.items():
                percentage = (revenue / total_revenue) * 100 if total_revenue > 0 else 0
                print(f"{room_type:<15} ${revenue:<14.2f} {percentage:.2f}%")
    
    def generate_guest_statistics(self):
        """Generate and display guest statistics."""
        if not self.guests:
            print("No guests registered.")
            return
        
        total_guests = len(self.guests)
        guests_with_bookings = set()
        
        for booking in self.bookings:
            guests_with_bookings.add(booking.guest_id)
        
        guests_with_bookings_count = len(guests_with_bookings)
        guests_without_bookings = total_guests - guests_with_bookings_count
        
        print("\nGUEST STATISTICS:")
        print("-" * 60)
        print(f"Total Registered Guests: {total_guests}")
        print(f"Guests with Bookings: {guests_with_bookings_count}")
        print(f"Guests without Bookings: {guests_without_bookings}")
        print("-" * 60)
        
        # Top guests by number of bookings
        guest_booking_count = {}
        for booking in self.bookings:
            guest_id = booking.guest_id
            if guest_id not in guest_booking_count:
                guest_booking_count[guest_id] = 0
            guest_booking_count[guest_id] += 1
        
        if guest_booking_count:
            print("\nTOP GUESTS BY NUMBER OF BOOKINGS:")
            print("-" * 60)
            print(f"{'Guest ID':<10} {'Name':<20} {'Bookings':<10}")
            print("-" * 60)
            
            # Sort guests by booking count in descending order
            sorted_guests = sorted(guest_booking_count.items(), key=lambda x: x[1], reverse=True)
            
            # Display top 5 guests or all if less than 5
            for i, (guest_id, count) in enumerate(sorted_guests[:5]):
                guest = self.find_guest(guest_id)
                name = guest.name if guest else "Unknown"
                print(f"{guest_id:<10} {name:<20} {count:<10}")