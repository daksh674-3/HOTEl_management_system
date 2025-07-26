# Hotel Management System

A comprehensive hotel management system built with Python that allows hotel staff to manage rooms, guests, bookings, and billing operations through a command-line interface.

## Features

- **Room Management**: Add, update, view, and search for rooms
- **Guest Management**: Register guests, update information, search for guests
- **Booking Management**: Create, update, cancel, and search for bookings
- **Billing**: Generate bills, process payments, view billing history
- **Reports**: Generate occupancy, revenue, and guest statistics reports
- **Data Persistence**: All data is saved to JSON files for persistence

## Project Structure

- `main.py`: The entry point of the application with the command-line interface
- `hotel.py`: Contains the HotelManager class, which serves as the central controller
- `room.py`: Contains the Room class for room management
- `guest.py`: Contains the Guest class for guest management
- `booking.py`: Contains the Booking class for booking management
- `database.py`: Contains the Database class for data storage and retrieval
- `data/`: Directory where all data files are stored (created automatically)

## Requirements

- Python 3.6 or higher

## Installation

1. Clone or download this repository
2. Navigate to the project directory

## Usage

To start the Hotel Management System, run:

```bash
python main.py
```

### Room Management

- View all rooms
- Add new rooms
- Update room details
- Search for rooms by number

### Guest Management

- View all registered guests
- Register new guests
- Update guest information
- Search for guests by name or ID

### Booking Management

- View all bookings
- Create new bookings
- Update booking details
- Cancel bookings
- Search for bookings by ID, guest ID, or room number

### Billing

- Generate bills for bookings
- Process payments
- View all bills

### Reports

- Generate occupancy reports
- Generate revenue reports for specific periods
- View guest statistics

## Data Storage

All data is stored in JSON files in the `data` directory:

- `rooms.json`: Room data
- `guests.json`: Guest data
- `bookings.json`: Booking data
- `bills.json`: Bill data

## Example Workflow

1. Add rooms to the hotel
2. Register guests
3. Create bookings for guests
4. Generate bills for bookings
5. Process payments
6. Generate reports

## License

This project is open-source and available under the MIT License.