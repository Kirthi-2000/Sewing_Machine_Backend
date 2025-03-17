from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import DateWidget, DateTimeWidget, TimeWidget
from .models import MachineLog

class MachineLogResource(resources.ModelResource):
    DATE = fields.Field(column_name='DATE', attribute='DATE', widget=DateWidget(format='%Y-%m-%d'))
    START_TIME = fields.Field(column_name='START_TIME', attribute='START_TIME', widget=TimeWidget(format='%H:%M:%S'))
    END_TIME = fields.Field(column_name='END_TIME', attribute='END_TIME', widget=TimeWidget(format='%H:%M:%S'))
    created_at = fields.Field(column_name='created_at', attribute='created_at', widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = MachineLog
        import_id_fields = ['MACHINE_ID', 'DATE', 'START_TIME']  # Use unique fields instead of 'id'
        exclude = ('id',)  # Auto-generated in DB

    def before_import_row(self, row, **kwargs):
        """Fix date and time formats before import."""
        # Convert DATE to YYYY-MM-DD
        if 'DATE' in row:
            row['DATE'] = row['DATE'].replace('/', '-')
            row['DATE'] = '-'.join(row['DATE'].split('-')[::-1])  # Convert DD-MM-YYYY to YYYY-MM-DD
        
        # Ensure created_at follows correct format
        if 'created_at' in row:
            row['created_at'] = row['created_at'].replace('/', '-')
            if len(row['created_at'].split()) == 2:
                date_part, time_part = row['created_at'].split()
                row['created_at'] = '-'.join(date_part.split('-')[::-1]) + " " + time_part

class MachineLogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MachineLogResource
    list_display = ('MACHINE_ID', 'OPERATOR_ID', 'DATE', 'START_TIME', 'END_TIME', 'MODE')
    search_fields = ('MACHINE_ID', 'OPERATOR_ID', 'DATE')
    list_filter = ('DATE', 'MODE')

admin.site.register(MachineLog, MachineLogAdmin)
