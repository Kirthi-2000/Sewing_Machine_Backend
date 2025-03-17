from rest_framework import serializers
from .models import MachineLog, ModeMessage
<<<<<<< HEAD
from datetime import datetime

class MachineLogSerializer(serializers.ModelSerializer):
    DATE = serializers.CharField()  # Accept date as a string initially
    START_TIME = serializers.CharField()  # Accept time as a string initially
    END_TIME = serializers.CharField()  # Accept time as a string initially
    
    class Meta:
        model = MachineLog
        fields = '__all__'
=======

class MachineLogSerializer(serializers.ModelSerializer):
    mode_description = serializers.SerializerMethodField()

    class Meta:
        model = MachineLog
        fields = [
            "machine_id", "line_numb", "operator_id", "date", "start_time",
            "end_time", "login_time", "mode", "stitch_count", "needle_runtime",
            "needle_stoptime", "tx_logid", "str_logid", "device_id", "reserve",
            "mode_description", "created_at"  # Added created_at
        ]
>>>>>>> 625b6feb (dashboard analytics)

    def get_mode_description(self, obj):
        mode_message = ModeMessage.objects.filter(mode=obj.mode).first()
        return mode_message.message if mode_message else "N/A"
<<<<<<< HEAD
    
    def validate_DATE(self, value):
        """Validate and convert date from YYYY:MM:DD format"""
        try:
            date_obj = datetime.strptime(value, '%Y:%m:%d').date()
            return date_obj
        except ValueError:
            raise serializers.ValidationError("Date must be in YYYY:MM:DD format")
    
    def validate_START_TIME(self, value):
        """Validate and normalize time format"""
        try:
            # Handle single-digit hours and minutes
            parts = value.split(':')
            if len(parts) == 3:
                hour, minute, second = parts
                time_str = f"{int(hour):02d}:{int(minute):02d}:{int(second):02d}"
            elif len(parts) == 2:
                hour, minute = parts
                time_str = f"{int(hour):02d}:{int(minute):02d}:00"
            else:
                raise ValueError("Invalid time format")
                
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            return time_obj
        except ValueError:
            raise serializers.ValidationError("Time must be in HH:MM:SS format")
    
    def validate_END_TIME(self, value):
        """Validate and normalize time format"""
        try:
            # Handle single-digit hours and minutes
            parts = value.split(':')
            if len(parts) == 3:
                hour, minute, second = parts
                time_str = f"{int(hour):02d}:{int(minute):02d}:{int(second):02d}"
            elif len(parts) == 2:
                hour, minute = parts
                time_str = f"{int(hour):02d}:{int(minute):02d}:00"
            else:
                raise ValueError("Invalid time format")
                
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            return time_obj
        except ValueError:
            raise serializers.ValidationError("Time must be in HH:MM:SS format")
=======

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
>>>>>>> 625b6feb (dashboard analytics)
