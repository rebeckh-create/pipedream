#!/usr/bin/env python3
"""
Studio Business Administration System
Main module for automating yoga/fitness studio business operations
"""

import os
import json
import sqlite3
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import uuid

@dataclass
class Client:
    """Client/Member data structure"""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    membership_type: str
    membership_status: str  # active, expired, suspended
    join_date: str
    expiry_date: str
    emergency_contact: str = ""
    medical_notes: str = ""
    created_at: str = ""
    updated_at: str = ""

@dataclass
class ClassSession:
    """Class session data structure"""
    id: str
    name: str
    instructor: str
    date: str
    time: str
    duration: int  # minutes
    capacity: int
    enrolled: int
    room: str
    class_type: str
    price: float
    status: str  # scheduled, completed, cancelled
    created_at: str = ""

@dataclass
class Booking:
    """Booking data structure"""
    id: str
    client_id: str
    class_id: str
    booking_date: str
    status: str  # confirmed, cancelled, no_show, attended
    payment_status: str  # paid, pending, refunded
    created_at: str = ""

@dataclass
class Instructor:
    """Instructor data structure"""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    specialties: List[str]
    hourly_rate: float
    status: str  # active, inactive
    certifications: List[str]
    hire_date: str
    created_at: str = ""

class StudioAdmin:
    """Main class for studio business administration"""
    
    def __init__(self, db_path: str = "data/studio.db"):
        """Initialize the studio administration system"""
        self.db_path = db_path
        self._setup_logging()
        self._create_directories()
        self._setup_database()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/admin_{datetime.datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Studio administration system initialized")
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = ["data", "exports", "reports", "backups"]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _setup_database(self):
        """Setup SQLite database with required tables"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            # Clients table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    membership_type TEXT,
                    membership_status TEXT,
                    join_date TEXT,
                    expiry_date TEXT,
                    emergency_contact TEXT,
                    medical_notes TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Classes table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS classes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    instructor TEXT,
                    date TEXT,
                    time TEXT,
                    duration INTEGER,
                    capacity INTEGER,
                    enrolled INTEGER DEFAULT 0,
                    room TEXT,
                    class_type TEXT,
                    price REAL,
                    status TEXT,
                    created_at TEXT
                )
            ''')
            
            # Bookings table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    class_id TEXT,
                    booking_date TEXT,
                    status TEXT,
                    payment_status TEXT,
                    created_at TEXT,
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (class_id) REFERENCES classes (id)
                )
            ''')
            
            # Instructors table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS instructors (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    specialties TEXT,
                    hourly_rate REAL,
                    status TEXT,
                    certifications TEXT,
                    hire_date TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
            self.logger.info("Database tables created/verified")
    
    # CLIENT MANAGEMENT
    def add_client(self, client_data: Dict[str, Any]) -> str:
        """Add a new client to the system"""
        client_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        client = Client(
            id=client_id,
            first_name=client_data['first_name'],
            last_name=client_data['last_name'],
            email=client_data['email'],
            phone=client_data.get('phone', ''),
            membership_type=client_data.get('membership_type', 'drop-in'),
            membership_status=client_data.get('membership_status', 'active'),
            join_date=client_data.get('join_date', now.split('T')[0]),
            expiry_date=client_data.get('expiry_date', ''),
            emergency_contact=client_data.get('emergency_contact', ''),
            medical_notes=client_data.get('medical_notes', ''),
            created_at=now,
            updated_at=now
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                client.id, client.first_name, client.last_name, client.email,
                client.phone, client.membership_type, client.membership_status,
                client.join_date, client.expiry_date, client.emergency_contact,
                client.medical_notes, client.created_at, client.updated_at
            ))
            conn.commit()
        
        self.logger.info(f"Added new client: {client.first_name} {client.last_name}")
        return client_id
    
    def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
            row = cursor.fetchone()
            
            if row:
                return Client(**dict(row))
            return None
    
    def search_clients(self, search_term: str) -> List[Client]:
        """Search clients by name or email"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM clients 
                WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
                ORDER BY last_name, first_name
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            return [Client(**dict(row)) for row in cursor.fetchall()]
    
    def update_client(self, client_id: str, updates: Dict[str, Any]) -> bool:
        """Update client information"""
        updates['updated_at'] = datetime.datetime.now().isoformat()
        
        set_clause = ', '.join([f'{key} = ?' for key in updates.keys()])
        values = list(updates.values()) + [client_id]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f'UPDATE clients SET {set_clause} WHERE id = ?', values)
            conn.commit()
            
        self.logger.info(f"Updated client {client_id}")
        return cursor.rowcount > 0
    
    # CLASS MANAGEMENT
    def create_class(self, class_data: Dict[str, Any]) -> str:
        """Create a new class session"""
        class_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        class_session = ClassSession(
            id=class_id,
            name=class_data['name'],
            instructor=class_data['instructor'],
            date=class_data['date'],
            time=class_data['time'],
            duration=class_data.get('duration', 60),
            capacity=class_data.get('capacity', 20),
            enrolled=0,
            room=class_data.get('room', 'Main Studio'),
            class_type=class_data.get('class_type', 'yoga'),
            price=class_data.get('price', 20.0),
            status='scheduled',
            created_at=now
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO classes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                class_session.id, class_session.name, class_session.instructor,
                class_session.date, class_session.time, class_session.duration,
                class_session.capacity, class_session.enrolled, class_session.room,
                class_session.class_type, class_session.price, class_session.status,
                class_session.created_at
            ))
            conn.commit()
        
        self.logger.info(f"Created class: {class_session.name} on {class_session.date}")
        return class_id
    
    def get_classes_by_date(self, date: str) -> List[ClassSession]:
        """Get all classes for a specific date"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM classes WHERE date = ? ORDER BY time
            ''', (date,))
            
            return [ClassSession(**dict(row)) for row in cursor.fetchall()]
    
    def get_upcoming_classes(self, days: int = 7) -> List[ClassSession]:
        """Get upcoming classes for next N days"""
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM classes 
                WHERE date BETWEEN ? AND ? AND status = 'scheduled'
                ORDER BY date, time
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            return [ClassSession(**dict(row)) for row in cursor.fetchall()]
    
    # BOOKING MANAGEMENT
    def book_class(self, client_id: str, class_id: str) -> str:
        """Book a client into a class"""
        # Check if class has capacity
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT capacity, enrolled FROM classes WHERE id = ?
            ''', (class_id,))
            class_info = cursor.fetchone()
            
            if not class_info:
                raise ValueError("Class not found")
            
            capacity, enrolled = class_info
            if enrolled >= capacity:
                raise ValueError("Class is full")
            
            # Create booking
            booking_id = str(uuid.uuid4())
            now = datetime.datetime.now().isoformat()
            
            booking = Booking(
                id=booking_id,
                client_id=client_id,
                class_id=class_id,
                booking_date=now.split('T')[0],
                status='confirmed',
                payment_status='pending',
                created_at=now
            )
            
            # Insert booking and update class enrollment
            conn.execute('''
                INSERT INTO bookings VALUES (?,?,?,?,?,?,?)
            ''', (
                booking.id, booking.client_id, booking.class_id,
                booking.booking_date, booking.status, booking.payment_status,
                booking.created_at
            ))
            
            conn.execute('''
                UPDATE classes SET enrolled = enrolled + 1 WHERE id = ?
            ''', (class_id,))
            
            conn.commit()
        
        self.logger.info(f"Booked client {client_id} into class {class_id}")
        return booking_id
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking"""
        with sqlite3.connect(self.db_path) as conn:
            # Get booking info
            cursor = conn.execute('''
                SELECT class_id FROM bookings WHERE id = ? AND status = 'confirmed'
            ''', (booking_id,))
            result = cursor.fetchone()
            
            if not result:
                return False
            
            class_id = result[0]
            
            # Update booking status and decrease class enrollment
            conn.execute('''
                UPDATE bookings SET status = 'cancelled' WHERE id = ?
            ''', (booking_id,))
            
            conn.execute('''
                UPDATE classes SET enrolled = enrolled - 1 WHERE id = ?
            ''', (class_id,))
            
            conn.commit()
        
        self.logger.info(f"Cancelled booking {booking_id}")
        return True
    
    def get_client_bookings(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all bookings for a client with class details"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT b.*, c.name as class_name, c.date, c.time, c.instructor
                FROM bookings b
                JOIN classes c ON b.class_id = c.id
                WHERE b.client_id = ?
                ORDER BY c.date DESC, c.time DESC
            ''', (client_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    # REPORTING
    def get_daily_report(self, date: str) -> Dict[str, Any]:
        """Generate daily report for a specific date"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get classes for the day
            classes = conn.execute('''
                SELECT * FROM classes WHERE date = ?
            ''', (date,)).fetchall()
            
            # Get bookings for the day
            bookings = conn.execute('''
                SELECT COUNT(*) as total_bookings, 
                       SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed,
                       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
                FROM bookings b
                JOIN classes c ON b.class_id = c.id
                WHERE c.date = ?
            ''', (date,)).fetchone()
            
            # Calculate revenue
            revenue = conn.execute('''
                SELECT SUM(c.price) as total_revenue
                FROM bookings b
                JOIN classes c ON b.class_id = c.id
                WHERE c.date = ? AND b.status = 'confirmed' AND b.payment_status = 'paid'
            ''', (date,)).fetchone()
            
            return {
                'date': date,
                'classes_scheduled': len(classes),
                'total_bookings': bookings['total_bookings'] or 0,
                'confirmed_bookings': bookings['confirmed'] or 0,
                'cancelled_bookings': bookings['cancelled'] or 0,
                'revenue': revenue['total_revenue'] or 0.0,
                'classes': [dict(c) for c in classes]
            }
    
    def get_membership_report(self) -> Dict[str, Any]:
        """Generate membership status report"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            total_clients = conn.execute('SELECT COUNT(*) as count FROM clients').fetchone()['count']
            
            by_status = conn.execute('''
                SELECT membership_status, COUNT(*) as count 
                FROM clients 
                GROUP BY membership_status
            ''').fetchall()
            
            by_type = conn.execute('''
                SELECT membership_type, COUNT(*) as count 
                FROM clients 
                GROUP BY membership_type
            ''').fetchall()
            
            # Expiring memberships (next 30 days)
            thirty_days = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
            expiring = conn.execute('''
                SELECT COUNT(*) as count FROM clients 
                WHERE expiry_date BETWEEN ? AND ? AND membership_status = 'active'
            ''', (datetime.date.today().isoformat(), thirty_days)).fetchone()['count']
            
            return {
                'total_clients': total_clients,
                'by_status': {row['membership_status']: row['count'] for row in by_status},
                'by_type': {row['membership_type']: row['count'] for row in by_type},
                'expiring_soon': expiring
            }
    
    def export_data(self, table: str, filename: str = None) -> str:
        """Export table data to JSON"""
        if not filename:
            filename = f"exports/{table}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(f'SELECT * FROM {table}')
            data = [dict(row) for row in cursor.fetchall()]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        self.logger.info(f"Exported {table} data to {filename}")
        return filename

def main():
    """Main entry point for the studio administration system"""
    try:
        admin = StudioAdmin()
        
        # Example usage
        print("Studio Business Administration System")
        print("====================================")
        
        # Show some stats
        membership_report = admin.get_membership_report()
        print(f"Total Clients: {membership_report['total_clients']}")
        
        upcoming_classes = admin.get_upcoming_classes()
        print(f"Upcoming Classes (7 days): {len(upcoming_classes)}")
        
        return 0
        
    except Exception as e:
        print(f"Error initializing studio administration: {e}")
        return 1

if __name__ == "__main__":
    exit(main())