#!/usr/bin/env python3
"""
Hotel Management System - Database Module
This module contains the Database class, which handles data storage and retrieval.
"""

import os
import json
from room import Room
from guest import Guest
from booking import Booking

class Database:
    """
    Database class that handles data storage and retrieval.
    
    This class provides methods to load and save data to JSON files,
    serving as a simple data persistence layer for the hotel management system.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize a new Database object.
        
        Args:
            data_dir (str, optional): The directory where data files are stored
        """
        self.data_dir = data_dir
        self._ensure_data_dir_exists()
    
    def _ensure_data_dir_exists(self):
        """Ensure that the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_file_path(self, file_name):
        """
        Get the full path to a data file.
        
        Args:
            file_name (str): The name of the file
            
        Returns:
            str: The full path to the file
        """
        return os.path.join(self.data_dir, file_name)
    
    def _save_to_file(self, data, file_name):
        """
        Save data to a JSON file.
        
        Args:
            data (list): The data to save
            file_name (str): The name of the file
            
        Returns:
            bool: True if the data was saved successfully, False otherwise
        """
        try:
            file_path = self._get_file_path(file_name)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data to {file_name}: {str(e)}")
            return False
    
    def _load_from_file(self, file_name):
        """
        Load data from a JSON file.
        
        Args:
            file_name (str): The name of the file
            
        Returns:
            list: The loaded data, or an empty list if the file doesn't exist
        """
        try:
            file_path = self._get_file_path(file_name)
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {file_name}: {str(e)}")
            return []
    
    # Room data methods
    
    def save_rooms(self, rooms):
        """
        Save room data to a file.
        
        Args:
            rooms (list): A list of Room objects
            
        Returns:
            bool: True if the data was saved successfully, False otherwise
        """
        room_data = [room.to_dict() for room in rooms]
        return self._save_to_file(room_data, "rooms.json")
    
    def load_rooms(self):
        """
        Load room data from a file.
        
        Returns:
            list: A list of Room objects
        """
        room_data = self._load_from_file("rooms.json")
        return [Room.from_dict(data) for data in room_data]
    
    # Guest data methods
    
    def save_guests(self, guests):
        """
        Save guest data to a file.
        
        Args:
            guests (list): A list of Guest objects
            
        Returns:
            bool: True if the data was saved successfully, False otherwise
        """
        guest_data = [guest.to_dict() for guest in guests]
        return self._save_to_file(guest_data, "guests.json")
    
    def load_guests(self):
        """
        Load guest data from a file.
        
        Returns:
            list: A list of Guest objects
        """
        guest_data = self._load_from_file("guests.json")
        return [Guest.from_dict(data) for data in guest_data]
    
    # Booking data methods
    
    def save_bookings(self, bookings):
        """
        Save booking data to a file.
        
        Args:
            bookings (list): A list of Booking objects
            
        Returns:
            bool: True if the data was saved successfully, False otherwise
        """
        booking_data = [booking.to_dict() for booking in bookings]
        return self._save_to_file(booking_data, "bookings.json")
    
    def load_bookings(self):
        """
        Load booking data from a file.
        
        Returns:
            list: A list of Booking objects
        """
        booking_data = self._load_from_file("bookings.json")
        return [Booking.from_dict(data) for data in booking_data]
    
    # Bill data methods
    
    def save_bills(self, bills):
        """
        Save bill data to a file.
        
        Args:
            bills (list): A list of Bill objects
            
        Returns:
            bool: True if the data was saved successfully, False otherwise
        """
        bill_data = [bill.to_dict() for bill in bills]
        return self._save_to_file(bill_data, "bills.json")
    
    def load_bills(self):
        """
        Load bill data from a file.
        
        Returns:
            list: A list of Bill objects
        """
        from hotel import Bill  # Import here to avoid circular imports
        
        bill_data = self._load_from_file("bills.json")
        return [Bill.from_dict(data) for data in bill_data]