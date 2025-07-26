#!/usr/bin/env python3
"""
Hotel Management System - Main Module
This module serves as the entry point for the Hotel Management System.
It provides a command-line interface for users to interact with the system.
"""

import os
import sys
import time
from hotel import HotelManager

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the application header."""
    print("\n" + "=" * 60)
    print(" " * 20 + "HOTEL MANAGEMENT SYSTEM")
    print("=" * 60 + "\n")

def display_menu():
    """Display the main menu options."""
    print("\nMAIN MENU:")
    print("1. Room Management")
    print("2. Guest Management")
    print("3. Booking Management")
    print("4. Billing")
    print("5. Reports")
    print("6. Exit")
    print("\nPlease select an option (1-6): ", end="")

def room_management_menu(hotel):
    """Display and handle room management options."""
    while True:
        clear_screen()
        print("\nROOM MANAGEMENT:")
        print("1. View All Rooms")
        print("2. Add New Room")
        print("3. Update Room Details")
        print("4. Search Room")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            hotel.view_all_rooms()
            input("\nPress Enter to continue...")
        elif choice == '2':
            room_number = input("Enter Room Number: ")
            room_type = input("Enter Room Type (Single/Double/Suite): ")
            price = input("Enter Room Price per Night: ")
            try:
                price = float(price)
                hotel.add_room(room_number, room_type, price)
                print("\nRoom added successfully!")
            except ValueError:
                print("\nInvalid price. Please enter a valid number.")
            input("\nPress Enter to continue...")
        elif choice == '3':
            room_number = input("Enter Room Number to Update: ")
            if hotel.find_room(room_number):
                room_type = input("Enter New Room Type (leave blank to keep current): ")
                price = input("Enter New Room Price (leave blank to keep current): ")
                hotel.update_room(room_number, room_type, price)
                print("\nRoom updated successfully!")
            else:
                print(f"\nRoom {room_number} not found.")
            input("\nPress Enter to continue...")
        elif choice == '4':
            room_number = input("Enter Room Number to Search: ")
            room = hotel.find_room(room_number)
            if room:
                print(f"\nRoom Details:\nNumber: {room.number}\nType: {room.type}\nPrice: ${room.price:.2f}\nStatus: {'Occupied' if room.is_occupied else 'Available'}")
            else:
                print(f"\nRoom {room_number} not found.")
            input("\nPress Enter to continue...")
        elif choice == '5':
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

def guest_management_menu(hotel):
    """Display and handle guest management options."""
    while True:
        clear_screen()
        print("\nGUEST MANAGEMENT:")
        print("1. View All Guests")
        print("2. Register New Guest")
        print("3. Update Guest Information")
        print("4. Search Guest")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1':
            hotel.view_all_guests()
            input("\nPress Enter to continue...")
        elif choice == '2':
            name = input("Enter Guest Name: ")
            phone = input("Enter Guest Phone: ")
            email = input("Enter Guest Email: ")
            address = input("Enter Guest Address: ")
            hotel.add_guest(name, phone, email, address)
            print("\nGuest registered successfully!")
            input("\nPress Enter to continue...")
        elif choice == '3':
            guest_id = input("Enter Guest ID to Update: ")
            guest = hotel.find_guest(guest_id)
            if guest:
                name = input("Enter New Name (leave blank to keep current): ")
                phone = input("Enter New Phone (leave blank to keep current): ")
                email = input("Enter New Email (leave blank to keep current): ")
                address = input("Enter New Address (leave blank to keep current): ")
                hotel.update_guest(guest_id, name, phone, email, address)
                print("\nGuest information updated successfully!")
            else:
                print(f"\nGuest with ID {guest_id} not found.")
            input("\nPress Enter to continue...")
        elif choice == '4':
            search_term = input("Enter Guest Name or ID to Search: ")
            hotel.search_guest(search_term)
            input("\nPress Enter to continue...")
        elif choice == '5':
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

def booking_management_menu(hotel):
    """Display and handle booking management options."""
    while True:
        clear_screen()
        print("\nBOOKING MANAGEMENT:")
        print("1. View All Bookings")
        print("2. Create New Booking")
        print("3. Update Booking")
        print("4. Cancel Booking")
        print("5. Search Booking")
        print("6. Back to Main Menu")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            hotel.view_all_bookings()
            input("\nPress Enter to continue...")
        elif choice == '2':
            guest_id = input("Enter Guest ID: ")
            if not hotel.find_guest(guest_id):
                print(f"\nGuest with ID {guest_id} not found. Please register the guest first.")
                input("\nPress Enter to continue...")
                continue
                
            room_number = input("Enter Room Number: ")
            if not hotel.find_room(room_number):
                print(f"\nRoom {room_number} not found.")
                input("\nPress Enter to continue...")
                continue
                
            check_in = input("Enter Check-in Date (YYYY-MM-DD): ")
            check_out = input("Enter Check-out Date (YYYY-MM-DD): ")
            
            try:
                booking_id = hotel.create_booking(guest_id, room_number, check_in, check_out)
                if booking_id:
                    print(f"\nBooking created successfully! Booking ID: {booking_id}")
                else:
                    print("\nFailed to create booking. Room might be unavailable for the selected dates.")
            except ValueError as e:
                print(f"\nError: {e}")
            
            input("\nPress Enter to continue...")
        elif choice == '3':
            booking_id = input("Enter Booking ID to Update: ")
            booking = hotel.find_booking(booking_id)
            if booking:
                print("\nLeave fields blank to keep current values.")
                check_in = input("Enter New Check-in Date (YYYY-MM-DD): ")
                check_out = input("Enter New Check-out Date (YYYY-MM-DD): ")
                
                try:
                    if hotel.update_booking(booking_id, check_in, check_out):
                        print("\nBooking updated successfully!")
                    else:
                        print("\nFailed to update booking. Room might be unavailable for the selected dates.")
                except ValueError as e:
                    print(f"\nError: {e}")
            else:
                print(f"\nBooking with ID {booking_id} not found.")
            
            input("\nPress Enter to continue...")
        elif choice == '4':
            booking_id = input("Enter Booking ID to Cancel: ")
            if hotel.cancel_booking(booking_id):
                print("\nBooking cancelled successfully!")
            else:
                print(f"\nBooking with ID {booking_id} not found or already cancelled.")
            
            input("\nPress Enter to continue...")
        elif choice == '5':
            search_term = input("Enter Booking ID, Guest ID, or Room Number to Search: ")
            hotel.search_booking(search_term)
            input("\nPress Enter to continue...")
        elif choice == '6':
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

def billing_menu(hotel):
    """Display and handle billing options."""
    while True:
        clear_screen()
        print("\nBILLING:")
        print("1. Generate Bill for Booking")
        print("2. View All Bills")
        print("3. Process Payment")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == '1':
            booking_id = input("Enter Booking ID: ")
            bill = hotel.generate_bill(booking_id)
            if bill:
                print(f"\nBill generated successfully! Bill ID: {bill.bill_id}")
            else:
                print(f"\nFailed to generate bill. Booking with ID {booking_id} not found or already billed.")
            
            input("\nPress Enter to continue...")
        elif choice == '2':
            hotel.view_all_bills()
            input("\nPress Enter to continue...")
        elif choice == '3':
            bill_id = input("Enter Bill ID: ")
            amount = input("Enter Payment Amount: ")
            
            try:
                amount = float(amount)
                if hotel.process_payment(bill_id, amount):
                    print("\nPayment processed successfully!")
                else:
                    print(f"\nBill with ID {bill_id} not found or already paid.")
            except ValueError:
                print("\nInvalid amount. Please enter a valid number.")
            
            input("\nPress Enter to continue...")
        elif choice == '4':
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

def reports_menu(hotel):
    """Display and handle reports options."""
    while True:
        clear_screen()
        print("\nREPORTS:")
        print("1. Occupancy Report")
        print("2. Revenue Report")
        print("3. Guest Statistics")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == '1':
            hotel.generate_occupancy_report()
            input("\nPress Enter to continue...")
        elif choice == '2':
            start_date = input("Enter Start Date (YYYY-MM-DD): ")
            end_date = input("Enter End Date (YYYY-MM-DD): ")
            
            try:
                hotel.generate_revenue_report(start_date, end_date)
            except ValueError as e:
                print(f"\nError: {e}")
            
            input("\nPress Enter to continue...")
        elif choice == '3':
            hotel.generate_guest_statistics()
            input("\nPress Enter to continue...")
        elif choice == '4':
            break
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

def main():
    """Main function to run the Hotel Management System."""
    hotel = HotelManager()
    
    while True:
        clear_screen()
        display_header()
        display_menu()
        
        choice = input()
        
        if choice == '1':
            room_management_menu(hotel)
        elif choice == '2':
            guest_management_menu(hotel)
        elif choice == '3':
            booking_management_menu(hotel)
        elif choice == '4':
            billing_menu(hotel)
        elif choice == '5':
            reports_menu(hotel)
        elif choice == '6':
            clear_screen()
            print("\nThank you for using the Hotel Management System!")
            print("Exiting the program...\n")
            sys.exit(0)
        else:
            print("\nInvalid option. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()