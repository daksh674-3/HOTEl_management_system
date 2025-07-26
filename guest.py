#!/usr/bin/env python3
"""
Hotel Management System - Guest Module
This module contains the Guest class, which represents a hotel guest.
"""

class Guest:
    """
    Guest class representing a hotel guest.
    
    This class contains information about a hotel guest, including their
    ID, name, contact information, and address.
    """
    
    def __init__(self, guest_id, name, phone, email, address):
        """
        Initialize a new Guest object.
        
        Args:
            guest_id (str): The unique identifier for the guest
            name (str): The guest's full name
            phone (str): The guest's phone number
            email (str): The guest's email address
            address (str): The guest's physical address
        """
        self.guest_id = guest_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    
    def to_dict(self):
        """
        Convert the Guest object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Guest object
        """
        return {
            "guest_id": self.guest_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Guest object from a dictionary.
        
        Args:
            data (dict): A dictionary containing guest data
            
        Returns:
            Guest: A new Guest object
        """
        return cls(
            data["guest_id"],
            data["name"],
            data["phone"],
            data["email"],
            data["address"]
        )
    
    def __str__(self):
        """
        Return a string representation of the Guest object.
        
        Returns:
            str: A string representation of the Guest object
        """
        return f"Guest {self.guest_id}: {self.name} - {self.phone}, {self.email}"