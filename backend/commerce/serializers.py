from rest_framework import serializers

from .models import Point, Printer, Check


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = 'id', 'name',
        read_only_fields = 'id',


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = 'id', 'point_id', 'name', 'check_type',
        read_only_fields = 'id',


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = 'id', 'printer_id', 'type', 'order', 'status', 'pdf_file',
        read_only_fields = 'id', 'pdf_file',


class CheckCreateFormSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(required=True)
    items = serializers.JSONField(required=True)
    address = serializers.CharField(required=True)
    client = serializers.JSONField(required=True)
    point_id = serializers.IntegerField(required=True)
