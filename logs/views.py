# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .models import MachineLog, DuplicateLog, ModeMessage
# from .serializers import MachineLogSerializer
# from django.core.exceptions import ValidationError
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from django.db.models import Count

# # Dictionary to map mode numbers to descriptions
# MODES = {
#     1: "Sewing - Machine is On - Production",
#     2: "Logout - Off - Idle",
#     3: "No Garment - Off - Non-Production",
#     4: "Meeting - Off - Non-Production",
#     5: "Maintenance - On - Non-Production",
# }

# @api_view(['POST'])
# def log_machine_data(request):
#     """
#     View to handle machine data logging.
    
#     Validates and processes incoming machine log data:
#     - Checks for valid mode
#     - Prevents duplicate entries
#     - Stores the log data
    
#     Returns:
#         Response with status and mode description
#     """
#     data = request.data

#     # Inform the user that the data from the machine is being processed
#     print("The data from the machine is being processed. Please wait...")

#     # Validate mode
#     try:
#         mode = int(data.get("MODE"))  # Convert mode to integer
#     except (TypeError, ValueError):
#         return Response({"message": "Invalid mode format"}, status=400)

#     if mode not in MODES:
#         return Response({"message": f"Invalid mode: {mode}. Valid modes are {list(MODES.keys())}"}, status=400)

#     # Process the serializer first to handle date/time validation
#     serializer = MachineLogSerializer(data=data)
#     if not serializer.is_valid():
#         return Response({
# 	"code":200,
# 	"message":"Log saved successfully",
	
# }, status=400)
    
#     # Check for duplicate with validated data
#     validated_data = serializer.validated_data
#     if MachineLog.objects.filter(
#         MACHINE_ID=validated_data.get("MACHINE_ID"),
#         LINE_NUMB=validated_data.get("LINE_NUMB"),
#         OPERATOR_ID=validated_data.get("OPERATOR_ID"),
#         DATE=validated_data.get("DATE"),
#         START_TIME=validated_data.get("START_TIME"),
#         END_TIME=validated_data.get("END_TIME"),
#         MODE=validated_data.get("MODE"),
#     ).exists():
#         DuplicateLog.objects.create(payload=data)
#         return Response({
#             "message": "Duplicate entry found", 
#             "status": "duplicate", 
#             "mode_description": MODES[mode]
#         }, status=409)

#     # Save log
#     serializer.save()
#     return Response({
# 	"code":200,
# 	"message":"Log saved successfully",
# 	}
# , status=201)
# @api_view(['GET'])
# def get_machine_logs(request):
#     """
#     View to retrieve all machine logs.
    
#     Fetches all machine logs from the database and enriches them
#     with mode descriptions from the MODES dictionary.
    
#     Returns:
#         Response containing serialized logs with mode descriptions
#     """
#     logs = MachineLog.objects.all()
#     serialized_logs = MachineLogSerializer(logs, many=True).data

#     # Add mode descriptions to the serialized logs
#     for log in serialized_logs:
#         log['mode_description'] = MODES.get(log.get('MODE'), 'Unknown mode')

#     return Response(serialized_logs)
#     return Response(serialized_logs)

# @api_view(['POST'])
# def user_login(request):
#     """
#     View to handle user login and authenticate using Django's built-in authentication system.
    
#     Validates and processes incoming user login data:
#     - Authenticates the user
#     - Returns a token if authentication is successful
    
#     Returns:
#         Response with status and message
#     """
#     data = request.data
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return Response({"message": "Username and password are required"}, status=400)

#     user = authenticate(username=username, password=password)
#     if user is not None:
#         # Authentication successful, generate token
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"message": "Login successful", "token": token.key}, status=200)
#     else:
#         return Response({"message": "Invalid credentials"}, status=400)

# @api_view(['GET'])
# def get_underperforming_operators(request):
#     """
#     Fetches the count of underperforming operators.
    
#     Criteria:
#     - Operators in non-production modes (mode 3, 4, 5)
#     - Counts the number of unique `operator_id` values

#     Returns:
#         JSON response with count
#     """
#     underperforming_modes = [3, 4, 5]  # Non-production modes
#     underperforming_count = (
#         MachineLog.objects.filter(mode__in=underperforming_modes)
#         .values("operator_id")  # Group by operator
#         .distinct()
#         .count()
#     )

#     return Response({"underperforming_operator_count": underperforming_count}, status=200)



# @api_view(['GET'])
# def get_machine_id_count(request):
#     """
#     Fetch total number of unique Machine IDs.
#     """
#     machine_count = MachineLog.objects.values("MACHINE_ID").distinct().count()
#     return Response({"machine_id_count": machine_count}, status=200)


# @api_view(['GET'])
# def get_line_number_count(request):
#     """
#     Fetch total number of unique Line Numbers.
#     """
#     line_count = MachineLog.objects.values("LINE_NUMB").distinct().count()
#     return Response({"line_number_count": line_count}, status=200)



# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db.models import Sum, Count
# from .models import MachineLog

# @api_view(['GET'])
# def calculate_line_efficiency(request):
#     line_stats = (
#         MachineLog.objects.values("LINE_NUMB")
#         .annotate(
#             total_machines=Count("MACHINE_ID", distinct=True),
#             total_runtime=Sum("NEEDLE_RUNTIME"),
#             total_stoptime=Sum("NEEDLE_STOPTIME")
#         )
#     )

#     response = {}
#     for stat in line_stats:
#         line_number = stat["LINE_NUMB"]
#         total_machines = stat["total_machines"]
#         total_runtime = stat["total_runtime"]
#         total_stoptime = stat["total_stoptime"]

#         efficiency = (total_runtime / (total_runtime + total_stoptime)) * 100 if (total_runtime + total_stoptime) > 0 else 0

#         response[f"Line {line_number}"] = {
#             "Total_Machines": total_machines,
#             "Efficiency": f"{efficiency:.2f}%"
#         }

#     return Response(response)

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from datetime import datetime, timedelta
# from .models import MachineLog
# from django.db.models import F

# def time_to_seconds(time_obj):
#     """Convert HH:MM:SS TimeField to total seconds."""
#     return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

# @api_view(['GET'])
# def calculate_operator_efficiency(request):
#     logs = MachineLog.objects.values("OPERATOR_ID", "START_TIME", "END_TIME")

#     response = []
#     standard_work_time = 8 * 3600  # 8 hours in seconds

#     for log in logs:
#         operator_id = log["OPERATOR_ID"]
#         start_time = log["START_TIME"]
#         end_time = log["END_TIME"]

#         start_seconds = time_to_seconds(start_time)
#         end_seconds = time_to_seconds(end_time)

#         # Handle cases where END_TIME is on the next day
#         if end_seconds < start_seconds:
#             end_seconds += 24 * 3600  # Add 24 hours in seconds

#         actual_work_time = end_seconds - start_seconds
#         efficiency = (actual_work_time / standard_work_time) * 100 if standard_work_time > 0 else 0

#         response.append({
#             "operator": f"Operator {operator_id}",
#             "efficiency": round(efficiency, 2)
#         })
#     return Response(response)


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import MachineLog, DuplicateLog, ModeMessage
from .serializers import MachineLogSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Sum, F, Count, Case, When, Value, FloatField, F, ExpressionWrapper, DurationField
from django.http import JsonResponse
from rest_framework.response import Response
from .models import MachineLog
from datetime import datetime, timedelta
from django.db.models.functions import Cast
from django.db.models import Min, Max
from datetime import date

# Dictionary to map mode numbers to descriptions
MODES = {
    1: "Sewing - Machine is On - Production",
    2: "Logout - Off - Idle",
    3: "No Garment - Off - Non-Production",
    4: "Meeting - Off - Non-Production",
    5: "Maintenance - On - Non-Production",
}

from datetime import datetime

@api_view(['POST'])
def log_machine_data(request):
    """
    View to handle machine data logging with updated Tx Log ID and Str Log ID conditions.

    - Tx_LOGID: Now only saves the data without any condition.
    - Str_LOGID:
      - If > 1000, subtracts 1000 and stores only the adjusted value.
      - Checks if the adjusted Log ID exists for the same Machine ID before saving.
    """
    data = request.data

    print("Processing machine log data...")

    # Validate mode
    try:
        mode = int(data.get("MODE"))
    except (TypeError, ValueError):
        return Response({"message": "Invalid mode format"}, status=400)

    if mode not in MODES:
        return Response({"message": f"Invalid mode: {mode}. Valid modes are {list(MODES.keys())}"}, status=400)

    # Validate serializer
    serializer = MachineLogSerializer(data=data)
    if not serializer.is_valid():
        return Response({"message": "Validation failed", "errors": serializer.errors}, status=400)

    validated_data = serializer.validated_data

    # Extract Log IDs and Machine ID
    tx_log_id = validated_data.get("Tx_LOGID")
    str_log_id = validated_data.get("Str_LOGID")
    machine_id = validated_data.get("MACHINE_ID")

    if machine_id is None:
        return Response({"message": "MACHINE_ID is required"}, status=400)

    # Tx_LOGID: Only Save the Data Without Condition
    serializer.save()

    # Str_LOGID Handling
    if str_log_id is not None:
        try:
            str_log_id = int(str_log_id)  # Convert to integer
        except ValueError:
            return Response({"message": "Invalid Str_LOGID format"}, status=400)

        if str_log_id > 1000:
            adjusted_str_log_id = str_log_id - 1000  # Subtract 1000

            # Check if the adjusted STR Log ID exists for the same MACHINE_ID
            if MachineLog.objects.filter(Str_LOGID=adjusted_str_log_id, MACHINE_ID=machine_id).exists():
                return Response({
                    "code": 200,
                    "message": "STR Log ID already exists, data not saved"
                }, status=200)

            # Save with adjusted Str_LOGID
            validated_data["Str_LOGID"] = adjusted_str_log_id
            MachineLog.objects.create(**validated_data)

    return Response({
        "code": 200,
        "message": "Log saved successfully",
    }, status=201)

@api_view(['GET'])
def get_machine_logs(request):
    """
    View to retrieve all machine logs.
    
    Fetches all machine logs from the database and enriches them
    with mode descriptions from the MODES dictionary.
    
    Returns:
        Response containing serialized logs with mode descriptions
    """
    logs = MachineLog.objects.all()
    serialized_logs = MachineLogSerializer(logs, many=True).data

    # Add mode descriptions to the serialized logs
    for log in serialized_logs:
        log['mode_description'] = MODES.get(log.get('MODE'), 'Unknown mode')

    return Response(serialized_logs)
    return Response(serialized_logs)

@api_view(['POST'])
def user_login(request):
    """
    View to handle user login and authenticate using Django's built-in authentication system.
    
    Validates and processes incoming user login data:
    - Authenticates the user
    - Returns a token if authentication is successful
    
    Returns:
        Response with status and message
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        # Authentication successful, generate token
        token, created = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful", "token": token.key}, status=200)
    else:
        return Response({"message": "Invalid credentials"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Handles user logout by deleting the user's authentication token.
    Always returns "You have logged out successfully."
    """
    # Get the token from the request headers
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            token_key = auth_header.split()[1]  # Extract token value
            token = Token.objects.filter(key=token_key).first()

            if token:
                token.delete()

        except Exception:
            pass  # Ignore any errors during token deletion

    # Always return "You have logged out successfully."
    return Response({"message": "You have logged out successfully."}, status=200)

@api_view(['GET'])
def get_underperforming_operators(request):
    """
    Fetches the count of underperforming operators.
    
    Criteria:
    - Operators in non-production modes (mode 3, 4, 5)
    - Counts the number of unique `operator_id` values

    Returns:
        JSON response with count
    """
    underperforming_modes = [3, 4, 5]  # Non-production modes
    underperforming_count = (
        MachineLog.objects.filter(mode__in=underperforming_modes)
        .values("operator_id")  # Group by operator
        .distinct()
        .count()
    )

    return Response({"underperforming_operator_count": underperforming_count}, status=200)

@api_view(['GET'])
def get_machine_id_count(request):
    """
    Fetch total number of unique Machine IDs.
    """
    machine_count = MachineLog.objects.values("MACHINE_ID").distinct().count()
    return Response({"machine_id_count": machine_count}, status=200)

@api_view(['GET'])
def get_line_number_count(request):
    """
    Fetch total number of unique Line Numbers.
    """
    line_count = MachineLog.objects.values("LINE_NUMB").distinct().count()
    return Response({"line_number_count": line_count}, status=200)

@api_view(['GET'])
def calculate_line_efficiency(request):
    line_stats = (
        MachineLog.objects.values("LINE_NUMB")
        .annotate(
            total_machines=Count("MACHINE_ID", distinct=True),
            total_runtime=Sum("NEEDLE_RUNTIME"),
            total_stoptime=Sum("NEEDLE_STOPTIME")
        )
    )

    response = {}
    for stat in line_stats:
        line_number = stat["LINE_NUMB"]
        total_machines = stat["total_machines"]
        total_runtime = stat["total_runtime"]
        total_stoptime = stat["total_stoptime"]

        efficiency = (total_runtime / (total_runtime + total_stoptime)) * 100 if (total_runtime + total_stoptime) > 0 else 0

        response[f"Line {line_number}"] = {
            "Total_Machines": total_machines,
            "Efficiency": f"{efficiency:.2f}%"
        }

    return Response(response)

def time_to_seconds(time_obj):
    """Convert HH:MM:SS TimeField to total seconds."""
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

@api_view(['GET'])
def calculate_operator_efficiency(request):
    logs = MachineLog.objects.values("OPERATOR_ID", "START_TIME", "END_TIME")

    response = []
    standard_work_time = 8 * 3600  # 8 hours in seconds

    for log in logs:
        operator_id = log["OPERATOR_ID"]
        start_time = log["START_TIME"]
        end_time = log["END_TIME"]

        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)

        # Handle cases where END_TIME is on the next day
        if end_seconds < start_seconds:
            end_seconds += 24 * 3600  # Add 24 hours in seconds

        actual_work_time = end_seconds - start_seconds
        efficiency = (actual_work_time / standard_work_time) * 100 if standard_work_time > 0 else 0

        response.append({
            "operator": f"Operator {operator_id}",
            "efficiency": round(efficiency, 2)
        })

    return Response(response)

@api_view(['GET'])
def calculate_operator_idle_production_time(request):
    """
    Calculate the total idle and production time each operator spends in each mode on a particular date.
    Also calculates the stitching speed based on the runtime, needle stop time, and stitch count.
    
    Returns:
        Response containing operator ID, mode, date, total idle time, total production time, and stitching speed.
    """
    logs = MachineLog.objects.annotate(
        duration=ExpressionWrapper(
            Cast(F('END_TIME'), DurationField()) - Cast(F('START_TIME'), DurationField()),
            output_field=DurationField()
        )
    ).values('OPERATOR_ID', 'MODE', 'DATE', 'NEEDLE_RUNTIME', 'NEEDLE_STOPTIME', 'STITCH_COUNT').annotate(
        total_duration=Sum('duration')
    ).order_by('OPERATOR_ID', 'MODE', 'DATE')

    response = []
    for log in logs:
        total_duration_seconds = log['total_duration'].total_seconds()  # Convert duration to seconds
        total_duration_hours = total_duration_seconds / 3600  # Convert seconds to hours

        if log['MODE'] == 1:  # Production mode
            production_time = total_duration_hours
            idle_time = 0
        else:  # Idle mode
            production_time = 0
            idle_time = total_duration_hours

        # Calculate stitching speed: Stitch Count / (Needle Runtime + Needle Stop Time)
        # Avoid division by zero by ensuring the denominator is greater than zero.
        total_runtime_and_stop_time = log['NEEDLE_RUNTIME'] + log['NEEDLE_STOPTIME']
        stitching_speed = 0
        if total_runtime_and_stop_time > 0:
            stitching_speed = log['STITCH_COUNT'] / total_runtime_and_stop_time

        response.append({
            "operator_id": log['OPERATOR_ID'],
            "mode": log['MODE'],
            "date": log['DATE'],
            "total_idle_time": idle_time,
            "total_production_time": production_time,
            "stitching_speed": stitching_speed
        })

    return Response(response)

@api_view(['GET'])
def calculate_operator_overall_production(request):
    """
    Calculate the overall production for each operator on each day.
    The total production is calculated by summing the production time, total stitches, average stitching speed,
    and production percentage relative to the total production time of all operators for each day.
    
    Returns:
        Response containing operator ID, date, total production time, total stitches, average stitching speed,
        and production percentage for each day.
    """
    # Get the total production time for all operators grouped by date
    total_production_time_all_operators_by_date = MachineLog.objects.annotate(
        duration=ExpressionWrapper(
            Cast(F('END_TIME'), DurationField()) - Cast(F('START_TIME'), DurationField()),
            output_field=DurationField()
        )
    ).values('DATE').annotate(
        total_production_time=Sum('duration')
    )

    # Get the production data for each operator grouped by date
    logs = MachineLog.objects.annotate(
        duration=ExpressionWrapper(
            Cast(F('END_TIME'), DurationField()) - Cast(F('START_TIME'), DurationField()),
            output_field=DurationField()
        )
    ).values('OPERATOR_ID', 'DATE').annotate(
        total_production_time=Sum('duration'),
        total_stitch_count=Sum('STITCH_COUNT'),
        total_needleruntime=Sum('NEEDLE_RUNTIME'),
        total_needlestoptime=Sum('NEEDLE_STOPTIME')
    ).order_by('OPERATOR_ID', 'DATE')

    # Preparing response data
    response = []
    for log in logs:
        # Get the total production time for all operators for the current date
        total_production_time_for_date = next(
            (item['total_production_time'] for item in total_production_time_all_operators_by_date if item['DATE'] == log['DATE']),
            None
        )
        
        # If no production data exists for this date, continue to the next log
        if total_production_time_for_date is None:
            continue

        total_production_time_seconds = log['total_production_time'].total_seconds()
        total_production_time_hours = total_production_time_seconds / 3600  # Convert seconds to hours

        # Calculate average stitching speed: Total Stitch Count / (Total Needle Runtime + Total Needle Stop Time)
        total_runtime_and_stop_time = log['total_needleruntime'] + log['total_needlestoptime']
        stitching_speed = 0
        if total_runtime_and_stop_time > 0:
            stitching_speed = log['total_stitch_count'] / total_runtime_and_stop_time

        # Calculate production percentage for this operator on this date
        production_percentage = (total_production_time_seconds / total_production_time_for_date.total_seconds()) * 100

        response.append({
            "operator_id": log['OPERATOR_ID'],
            "date": log['DATE'],
            "total_production_time_hours": total_production_time_hours,
            "total_stitch_count": log['total_stitch_count'],
            "average_stitching_speed": stitching_speed,
            "production_percentage": production_percentage
        })

    return Response(response)

@api_view(['GET'])
def calculate_line_production_percentage(request):
    """
    Calculate the total working hours of operators in each line and their production percentage per day.
    
    Returns:
        Response containing line number, date, total operators, total working hours, and production percentage.
    """
    line_stats = (
        MachineLog.objects.annotate(
            duration=ExpressionWrapper(
                Cast(F('END_TIME'), DurationField()) - Cast(F('START_TIME'), DurationField()),
                output_field=DurationField()
            )
        ).values("LINE_NUMB", "DATE", "OPERATOR_ID")
        .annotate(
            total_runtime=Sum("NEEDLE_RUNTIME"),
            total_stoptime=Sum("NEEDLE_STOPTIME"),
            total_working_hours=Sum('duration')
        )
    )

    response = []
    for stat in line_stats:
        line_number = stat["LINE_NUMB"]
        date = stat["DATE"]
        total_runtime = stat["total_runtime"]
        total_stoptime = stat["total_stoptime"]
        total_working_hours_seconds = stat["total_working_hours"].total_seconds()
        total_working_hours = total_working_hours_seconds / 3600  # Convert seconds to hours

        # Initial line data
        line_data = {
            "Line Number": line_number,
            "Date": date,
            "Total_Operators": 1,  # Starting with 1 for each operator
            "Total_Working_Hours": total_working_hours,
            "Production_Percentage": 0,  # Default production percentage
        }

        # If the line number and date already exists in response, update it
        for line in response:
            if line["Line Number"] == line_number and line["Date"] == date:
                line_data["Total_Operators"] += 1
                line_data["Total_Working_Hours"] += total_working_hours
                break
        else:
            response.append(line_data)

        # Calculate the production percentage (if runtime + stoptime > 0)
        total_runtime_and_stop_time = total_runtime + total_stoptime
        if total_runtime_and_stop_time > 0:
            line_data["Production_Percentage"] = round((line_data["Total_Working_Hours"] / (total_runtime_and_stop_time / 3600)) * 100, 2)

    return Response(response)

def operator_report(request):
    report_data = MachineLog.objects.values('DATE', 'LINE_NUMB').annotate(
        start_time=Min('START_TIME'),
        end_time=Max('END_TIME'),
        sewing_hours=Sum(Case(
            When(MODE=1, then=F('NEEDLE_RUNTIME')),  # Sewing - Machine is On - Production
            default=Value(0), output_field=FloatField()
        )),
        idle_hours=Sum(Case(
            When(MODE=2, then=F('NEEDLE_STOPTIME')),  # Logout - Off - Idle
            default=Value(0), output_field=FloatField()
        )),
        meeting_hours=Sum(Case(
            When(MODE=4, then=F('NEEDLE_STOPTIME')),  # Meeting - Off - Non-Production
            default=Value(0), output_field=FloatField()
        )),
        no_feeding_hours=Sum(Case(
            When(MODE=3, then=F('NEEDLE_STOPTIME')),  # No Garment - Off - Non-Production
            default=Value(0), output_field=FloatField()
        )),
        maintenance_hours=Sum(Case(
            When(MODE=5, then=F('NEEDLE_RUNTIME')),  # Maintenance - On - Non-Production
            default=Value(0), output_field=FloatField()
        )),
        sewing_speed=ExpressionWrapper(
            Sum('STITCH_COUNT') / (Sum('NEEDLE_RUNTIME') + Sum('NEEDLE_STOPTIME')),
            output_field=FloatField()
        ),
        productive_time_percentage=ExpressionWrapper(
            (F('sewing_hours') / (F('sewing_hours') + F('idle_hours') + 
            F('meeting_hours') + F('no_feeding_hours') + F('maintenance_hours'))) * 100,
            output_field=FloatField()
        ),
        non_productive_time_percentage=ExpressionWrapper(
            100 - F('productive_time_percentage'),
            output_field=FloatField()
        )
    ).order_by('DATE', 'LINE_NUMB')

    return JsonResponse(list(report_data), safe=False)

def operator_report_new(request):
    # Query the MachineLog model and aggregate necessary fields
    report_data = MachineLog.objects.values('DATE', 'OPERATOR_ID').annotate(
        sewing_hours=Sum(Case(
            When(MODE=1, then=F('NEEDLE_RUNTIME')),
            default=Value(0), output_field=FloatField()
        )),
        idle_hours=Sum(Case(
            When(MODE=2, then=F('NEEDLE_STOPTIME')),
            default=Value(0), output_field=FloatField()
        )),
        no_feeding_hours=Sum(Case(
            When(MODE=3, then=F('NEEDLE_STOPTIME')),
            default=Value(0), output_field=FloatField()
        )),
        meeting_hours=Sum(Case(
            When(MODE=4, then=F('NEEDLE_STOPTIME')),
            default=Value(0), output_field=FloatField()
        )),
        maintenance_hours=Sum(Case(
            When(MODE=5, then=F('NEEDLE_RUNTIME')),
            default=Value(0), output_field=FloatField()
        )),
        sewing_speed=ExpressionWrapper(
            Sum('STITCH_COUNT') / (Sum('NEEDLE_RUNTIME') + Sum('NEEDLE_STOPTIME')),
            output_field=FloatField()
        ),
        productive_time_percentage=ExpressionWrapper(
            (F('sewing_hours') / (F('sewing_hours') + F('idle_hours') +
            F('meeting_hours') + F('no_feeding_hours') + F('maintenance_hours'))) * 100,
            output_field=FloatField()
        ),
        non_productive_time_percentage=ExpressionWrapper(
            100 - F('productive_time_percentage'),
            output_field=FloatField()
        )
    ).order_by('DATE', 'OPERATOR_ID')

    # Fetch operator names based on operator IDs (assuming you have an Operator model)
    operator_data = MachineLog.objects.values('OPERATOR_ID').distinct()
    operator_name_map = {operator['OPERATOR_ID']: f"Operator {operator['OPERATOR_ID']}" for operator in operator_data}

    # Add operator names to each report entry
    report_with_operator_names = [
        {
            **data,
            'OPERATOR_NAME': operator_name_map.get(data['OPERATOR_ID'], 'Unknown')
        }
        for data in report_data
    ]

    # Format the report as per the specified column names
    formatted_report = [
        {
            'Date': data['DATE'],
            'Operator ID': data['OPERATOR_ID'],
            'Operator Name': data['OPERATOR_NAME'],
            'Sewing Hours': data['sewing_hours'],
            'Idle Hours': data['idle_hours'],
            'Meeting Hours': data['meeting_hours'],
            'No Feeding Hours': data['no_feeding_hours'],
            'Maintenance Hours': data['maintenance_hours'],
            'Productive Time in %': data['productive_time_percentage'],
            'NPT in %': data['non_productive_time_percentage'],
            'Sewing Speed': data['sewing_speed']
        }
        for data in report_with_operator_names
    ]

    return JsonResponse(formatted_report, safe=False)


from django.db.models import Sum, Case, When, Value, FloatField, F, ExpressionWrapper
from django.http import JsonResponse
from datetime import datetime
from .models import MachineLog  # Ensure you have the correct model import

def operator_report_new2(request):
    # Fetch query parameters
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)

    # Filter by selected date range
    filters = {}
    if from_date:
        filters["DATE__gte"] = from_date
    if to_date:
        filters["DATE__lte"] = to_date

    # Query and aggregate data
    report_data = MachineLog.objects.filter(**filters).values('DATE', 'OPERATOR_ID').annotate(
        sewing_hours=Sum(Case(When(MODE=1, then=F('NEEDLE_RUNTIME')), default=Value(0), output_field=FloatField())),
        idle_hours=Sum(Case(When(MODE=2, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        no_feeding_hours=Sum(Case(When(MODE=3, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        meeting_hours=Sum(Case(When(MODE=4, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        maintenance_hours=Sum(Case(When(MODE=5, then=F('NEEDLE_RUNTIME')), default=Value(0), output_field=FloatField())),
        sewing_speed=ExpressionWrapper(
            Sum('STITCH_COUNT') / (Sum('NEEDLE_RUNTIME') + Sum('NEEDLE_STOPTIME')),
            output_field=FloatField()
        ),
        productive_time_percentage=ExpressionWrapper(
            (F('sewing_hours') / (F('sewing_hours') + F('idle_hours') +
            F('meeting_hours') + F('no_feeding_hours') + F('maintenance_hours'))) * 100,
            output_field=FloatField()
        ),
        non_productive_time_percentage=ExpressionWrapper(
            100 - F('productive_time_percentage'),
            output_field=FloatField()
        )
    ).order_by('DATE', 'OPERATOR_ID')

    # Add operator names
    operator_data = MachineLog.objects.values('OPERATOR_ID').distinct()
    operator_name_map = {operator['OPERATOR_ID']: f"Operator {operator['OPERATOR_ID']}" for operator in operator_data}

    report_with_operator_names = [
        {
            **data,
            'OPERATOR_NAME': operator_name_map.get(data['OPERATOR_ID'], 'Unknown')
        }
        for data in report_data
    ]

    return JsonResponse(report_with_operator_names, safe=False)

@api_view(['GET'])
def operator_summary(request):
    operators = MachineLog.objects.values('OPERATOR_ID').annotate(
        sewing_hours=Sum('NEEDLE_RUNTIME')  # Convert seconds to hours
    )
    return Response(operators)

@api_view(['GET'])
def operator_reports(request, operator_id):
    logs = MachineLog.objects.filter(OPERATOR_ID=operator_id)
    today = date.today()

    # Aggregated Values
    total_production_hours = logs.filter(MODE=1).aggregate(
        total=Sum('NEEDLE_RUNTIME', default=0, output_field=FloatField())
    )['total'] or 0

    total_non_production_hours = logs.exclude(MODE=1).aggregate(
        total=Sum('NEEDLE_STOPTIME', default=0, output_field=FloatField())
    )['total'] or 0

    total_idle_hours = logs.filter(MODE=2).aggregate(
        total=Sum('NEEDLE_STOPTIME', default=0, output_field=FloatField())
    )['total'] or 0

    sewing_hours_percentage = (total_production_hours / (total_production_hours + total_non_production_hours) * 100) \
        if (total_production_hours + total_non_production_hours) > 0 else 0

    # Fetch today's data separately
    today_logs = logs.filter(DATE=today)
    
    today_production_hours = today_logs.filter(MODE=1).aggregate(
        total=Sum('NEEDLE_RUNTIME', default=0, output_field=FloatField())
    )['total'] or 0

    today_non_production_hours = today_logs.exclude(MODE=1).aggregate(
        total=Sum('NEEDLE_STOPTIME', default=0, output_field=FloatField())
    )['total'] or 0

    today_idle_hours = today_logs.filter(MODE=2).aggregate(
        total=Sum('NEEDLE_STOPTIME', default=0, output_field=FloatField())
    )['total'] or 0

    # Fetch Table Data (All days)
    table_data = logs.values('DATE').annotate(
        sewing_hours=Sum(Case(When(MODE=1, then=F('NEEDLE_RUNTIME')), default=Value(0), output_field=FloatField())),
        idle_hours=Sum(Case(When(MODE=2, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        meeting_hours=Sum(Case(When(MODE=4, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        no_feeding_hours=Sum(Case(When(MODE=3, then=F('NEEDLE_STOPTIME')), default=Value(0), output_field=FloatField())),
        maintenance_hours=Sum(Case(When(MODE=5, then=F('NEEDLE_RUNTIME')), default=Value(0), output_field=FloatField())),
        sewing_speed=Sum('STITCH_COUNT') / (Sum('NEEDLE_RUNTIME') + Sum('NEEDLE_STOPTIME')),
        stitch_count=Sum('STITCH_COUNT')
    ).order_by('DATE')

    formatted_table_data = [
        {
            'Date': data['DATE'],
            'Sewing Hours': data['sewing_hours'],
            'Idle Hours': data['idle_hours'],
            'Meeting Hours': data['meeting_hours'],
            'No Feeding Hours': data['no_feeding_hours'],
            'Maintenance Hours': data['maintenance_hours'],
            'Productive Time in %': (data['sewing_hours'] / (
                data['sewing_hours'] + data['idle_hours'] +
                data['meeting_hours'] + data['no_feeding_hours'] +
                data['maintenance_hours']
            )) * 100 if data['sewing_hours'] > 0 else 0,
            'NPT in %': 100 - ((data['sewing_hours'] / (
                data['sewing_hours'] + data['idle_hours'] +
                data['meeting_hours'] + data['no_feeding_hours'] +
                data['maintenance_hours']
            )) * 100) if data['sewing_hours'] > 0 else 100,
            'Sewing Speed': data['sewing_speed'],
            'Stitch Count': data['stitch_count']
        }
        for data in table_data
    ]

    return Response({
        "totalProductionHours": round(total_production_hours, 2),
        "totalNonProductionHours": round(total_non_production_hours, 2),
        "totalIdleHours": round(total_idle_hours, 2),
        "todayProductionHours": round(today_production_hours, 2),
        "todayNonProductionHours": round(today_non_production_hours, 2),
        "todayIdleHours": round(today_idle_hours, 2),
        "sewingHoursPercentage": round(sewing_hours_percentage, 2),
        "tableData": formatted_table_data
    })
