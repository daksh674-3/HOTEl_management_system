#!/usr/bin/env python3
"""
Hotel Management System - Room Module
This module contains the Room class, which represents a hotel room.
"""

class Room:
    """
    Room class representing a hotel room.
    
    This class contains information about a hotel room, including its
    number, type, price, and occupancy status.
    """
    
    def __init__(self, number, room_type, price, is_occupied=False):
        """
        Initialize a new Room object.
        
        Args:
            number (str): The room number
            room_type (str): The type of room (Single, Double, Suite, etc.)
            price (float): The price per night
            is_occupied (bool, optional): Whether the room is currently occupied
        """
        self.number = number
        self.type = room_type
        self.price = float(price)
        self.is_occupied = is_occupied
    
    def to_dict(self):
        """
        Convert the Room object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Room object
        """
        return {
            "number": self.number,
            "type": self.type,
            "price": self.price,
            "is_occupied": self.is_occupied
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Room object from a dictionary.
        
        Args:
            data (dict): A dictionary containing room data
            
        Returns:
            Room: A new Room object
        """
        return cls(
            data["number"],
            data["type"],
            data["price"],
            data["is_occupied"]
        )
    
    def __str__(self):
        """
        Return a string representation of the Room object.
        
        Returns:
            str: A string representation of the Room object
        """
        status = "Occupied" if self.is_occupied else "Available"
        return f"Room {self.number} ({self.type}): ${self.price:.2f} per night - {status}"