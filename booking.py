#!/usr/bin/env python3
"""
Hotel Management System - Booking Module
This module contains the Booking class, which represents a hotel booking.
"""

import datetime

class Booking:
    """
    Booking class representing a hotel booking.
    
    This class contains information about a hotel booking, including its
    ID, associated guest and room, check-in and check-out dates, and status.
    """
    
    def __init__(self, booking_id, guest_id, room_number, check_in, check_out, is_active=True):
        """
        Initialize a new Booking object.
        
        Args:
            booking_id (str): The unique identifier for the booking
            guest_id (str): The ID of the guest making the booking
            room_number (str): The number of the room being booked
            check_in (datetime.date): The check-in date
            check_out (datetime.date): The check-out date
            is_active (bool, optional): Whether the booking is active
        """
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.is_active = is_active
    
    def to_dict(self):
        """
        Convert the Booking object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Booking object
        """
        return {
            "booking_id": self.booking_id,
            "guest_id": self.guest_id,
            "room_number": self.room_number,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Booking object from a dictionary.
        
        Args:
            data (dict): A dictionary containing booking data
            
        Returns:
            Booking: A new Booking object
        """
        check_in = datetime.datetime.fromisoformat(data["check_in"]).date()
        check_out = datetime.datetime.fromisoformat(data["check_out"]).date()
        
        return cls(
            data["booking_id"],
            data["guest_id"],
            data["room_number"],
            check_in,
            check_out,
            data["is_active"]
        )
    
    def __str__(self):
        """
        Return a string representation of the Booking object.
        
        Returns:
            str: A string representation of the Booking object
        """
        status = "Active" if self.is_active else "Inactive"
        return (f"Booking {self.booking_id}: Guest {self.guest_id}, "
                f"Room {self.room_number}, "
                f"Check-in: {self.check_in.isoformat()}, "
                f"Check-out: {self.check_out.isoformat()}, "
                f"Status: {status}")
    
    @property
    def duration(self):
        """
        Calculate the duration of the booking in days.
        
        Returns:
            int: The number of days between check-in and check-out
        """
        return (self.check_out - self.check_in).days
    
    @property
    def is_current(self):
        """
        Check if the booking is for the current date.
        
        Returns:
            bool: True if today is between check-in and check-out dates
        """
        today = datetime.datetime.now().date()
        return self.check_in <= today <= self.check_out
    
    @property
    def is_future(self):
        """
        Check if the booking is for a future date.
        
        Returns:
            bool: True if check-in date is in the future
        """
        today = datetime.datetime.now().date()
        return self.check_in > today
    
    @property
    def is_past(self):
        """
        Check if the booking is for a past date.
        
        Returns:
            bool: True if check-out date is in the past
        """
        today = datetime.datetime.now().date()
        return self.check_out < today