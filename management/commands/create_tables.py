from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create database tables manually'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Create CustomUser table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `gram_panchayate_system_customuser` (
                    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `password` varchar(128) NOT NULL,
                    `last_login` datetime(6) NULL,
                    `is_superuser` bool NOT NULL,
                    `username` varchar(150) NOT NULL UNIQUE,
                    `first_name` varchar(150) NOT NULL,
                    `last_name` varchar(150) NOT NULL,
                    `email` varchar(254) NOT NULL,
                    `is_staff` bool NOT NULL,
                    `is_active` bool NOT NULL,
                    `date_joined` datetime(6) NOT NULL,
                    `user_type` varchar(10) NOT NULL,
                    `mobile_number` varchar(15) NULL UNIQUE,
                    `created_at` datetime(6) NOT NULL
                )
            """)
            
            # Create OTP table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `gram_panchayate_system_otp` (
                    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `mobile_number` varchar(15) NOT NULL,
                    `otp` varchar(6) NOT NULL,
                    `created_at` datetime(6) NOT NULL,
                    `is_used` bool NOT NULL
                )
            """)
            
            # Create AdminProfile table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `gram_panchayate_system_adminprofile` (
                    `user_id` bigint NOT NULL PRIMARY KEY,
                    `designation` varchar(100) NOT NULL,
                    `department` varchar(100) NOT NULL,
                    FOREIGN KEY (`user_id`) REFERENCES `gram_panchayate_system_customuser` (`id`)
                )
            """)
            
            # Create CitizenProfile table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `gram_panchayate_system_citizenprofile` (
                    `user_id` bigint NOT NULL PRIMARY KEY,
                    `aadhaar_number` varchar(12) NOT NULL UNIQUE,
                    `address` longtext NOT NULL,
                    `date_of_birth` date NULL,
                    FOREIGN KEY (`user_id`) REFERENCES `gram_panchayate_system_customuser` (`id`)
                )
            """)
            
            # Create ClerkProfile table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `gram_panchayate_system_clerkprofile` (
                    `user_id` bigint NOT NULL PRIMARY KEY,
                    `panchayat_name` varchar(100) NOT NULL,
                    `designation` varchar(100) NOT NULL,
                    `employee_id` varchar(50) NOT NULL UNIQUE,
                    FOREIGN KEY (`user_id`) REFERENCES `gram_panchayate_system_customuser` (`id`)
                )
            """)
            
        self.stdout.write(
            self.style.SUCCESS('Successfully created database tables')
        )