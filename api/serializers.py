from rest_framework import serializers
from api.models import (
    Region, SchoolSale, SchoolFollowUp, SchoolVisit, VisitCheckin,
    Task, Message, CatalogItem, Order, OrderItem,
    SchoolSampleDistribution, Target, Event, EventAssignment,
    EventCheckin, EventSample, EventOrder, EventSale, EventLead,
    EventTask, EventPhoto, EventReport, EventExpense,
    Geofence, GeofenceEvent, SocialConversation, SocialMessage,
    DebtCollection, OpportunityActivity, PipelineHistory,
    Profile, AuditEvent, SupervisorAlert, SupervisorIncident,
    SupervisorNote, SupervisorNotification, RoutePlan,
    SampleRequest, Visitation, ProjectForm, ProjectFormResponse,
    School,
)
from users.serializers import UserSerializer
from tenant.serializers import TenantSerializer


class SchoolSerializer(serializers.ModelSerializer):
    captured_by = UserSerializer(read_only=True)
    captured_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = School
        fields = [
            'id', 'tenant', 'name', 'phone', 'county', 'source',
            'external_place_id', 'external_vicinity', 'focus_areas',
            'book_category', 'dealer_type', 'shop_category', 'selected_product',
            'partner_subtype', 'latitude', 'longitude', 'gps_accuracy_meters',
            'photo_url', 'photo_path', 'captured_by', 'captured_by_id',
            'captured_at', 'capture_status', 'contact_name', 'contact_phone',
            'contact_title', 'feedback', 'notes', 'samples_left', 'sample_book',
            'engagement_type', 'school_ownership', 'school_ownership_other',
            'school_population', 'school_lifecycle_status', 'sample_proof_url',
            'sample_proof_path', 'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']

    def create(self, validated_data):
        validated_data.pop('captured_by_id', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('captured_by_id', None)
        return super().update(instance, validated_data)


# ──────────────────────────────────────────────
#  REGION
# ──────────────────────────────────────────────
class RegionSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    supervisor = UserSerializer(read_only=True)
    supervisor_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Region
        fields = [
            'id', 'tenant', 'name', 'sub_region',
            'assigned_to', 'assigned_to_id',
            'supervisor', 'supervisor_id',
            'created_by', 'created_by_id',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  SCHOOL SALE
# ──────────────────────────────────────────────
class SchoolSaleSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SchoolSale
        fields = [
            'id', 'tenant', 'school', 'school_id', 'agent', 'agent_id',
            'package_name', 'expected_value', 'notes', 'stage',
            'contact_person', 'sample_quantity', 'quotation_reference',
            'decision_owner', 'negotiation_topic', 'loss_reason',
            'dormant_reason', 'stage_updated_at', 'expected_close_date',
            'probability', 'closed_at', 'next_action', 'next_action_date',
            'last_activity_at', 'risk_level', 'weighted_forecast',
            'stage_sla_due_at', 'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  SCHOOL FOLLOW-UP
# ──────────────────────────────────────────────
class SchoolFollowUpSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SchoolFollowUp
        fields = [
            'id', 'tenant', 'school', 'school_id', 'agent', 'agent_id',
            'contact_person', 'next_step', 'due_at', 'notes',
            'status', 'completed_at', 'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  SCHOOL VISIT
# ──────────────────────────────────────────────
class SchoolVisitSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SchoolVisit
        fields = [
            'id', 'tenant', 'school', 'school_id', 'agent', 'agent_id',
            'outcome', 'notes', 'photo_url', 'photo_path',
            'latitude', 'longitude', 'status', 'visited_at',
            'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'visited_at', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  VISIT CHECKIN
# ──────────────────────────────────────────────
class VisitCheckinSerializer(serializers.ModelSerializer):
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = VisitCheckin
        fields = [
            'id', 'tenant', 'agent', 'agent_id', 'school', 'school_id',
            'checkin_at', 'checkout_at', 'latitude', 'longitude', 'notes',
        ]
        read_only_fields = ['id', 'checkin_at', 'tenant']


# ──────────────────────────────────────────────
#  TASK
# ──────────────────────────────────────────────
class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id', 'tenant', 'title', 'description', 'target_role',
            'due_at', 'status', 'created_by', 'created_by_id',
            'assigned_to', 'assigned_to_id',
            'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  MESSAGE
# ──────────────────────────────────────────────
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.CharField(write_only=True)
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.CharField(write_only=True)
    related_school = SchoolSerializer(read_only=True)
    related_school_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    related_task = TaskSerializer(read_only=True)
    related_task_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Message
        fields = [
            'id', 'tenant', 'sender', 'sender_id', 'recipient', 'recipient_id',
            'subject', 'body', 'related_school', 'related_school_id',
            'related_task', 'related_task_id',
            'is_read', 'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  CATALOG ITEM
# ──────────────────────────────────────────────
class CatalogItemSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = CatalogItem
        fields = [
            'id', 'tenant', 'name', 'category', 'sku',
            'item_type', 'unit_price', 'stock_qty', 'description',
            'is_active', 'is_synced', 'created_by', 'created_by_id',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  ORDER
# ──────────────────────────────────────────────
class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'tenant', 'order',
            'product_name', 'category', 'sku', 'quantity',
            'unit_price', 'line_total', 'notes',
            'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


class OrderSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'tenant', 'school', 'school_id', 'school_name', 'school_phone',
            'agent', 'agent_id', 'order_number', 'payment_method',
            'payment_reference', 'checkout_amount', 'status', 'notes',
            'submitted_at', 'approved_at',
            'is_synced', 'created_at', 'updated_at', 'items',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant', 'order_number']


# ──────────────────────────────────────────────
#  SCHOOL SAMPLE DISTRIBUTION
# ──────────────────────────────────────────────
class SchoolSampleDistributionSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SchoolSampleDistribution
        fields = [
            'id', 'tenant', 'school', 'school_id', 'agent', 'agent_id',
            'sample_name', 'sample_category', 'client_type',
            'quantity', 'returned_qty', 'stamped_receipt_url',
            'stamped_receipt_path', 'notes', 'distributed_at',
            'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'distributed_at', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  TARGET
# ──────────────────────────────────────────────
class TargetSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Target
        fields = [
            'id', 'tenant', 'scope', 'target_type', 'target_period',
            'region', 'region_id', 'assigned_to', 'assigned_to_id',
            'target_data', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  EVENT
# ──────────────────────────────────────────────
class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id', 'tenant', 'name', 'event_type', 'region',
            'start_at', 'end_at', 'expected_attendance', 'budget',
            'status', 'created_by', 'created_by_id',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


class EventAssignmentSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True)

    class Meta:
        model = EventAssignment
        fields = ['id', 'tenant', 'event', 'event_id', 'agent', 'agent_id', 'role', 'assigned_at']
        read_only_fields = ['id', 'assigned_at', 'tenant']


class EventCheckinSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventCheckin
        fields = ['id', 'tenant', 'event', 'event_id', 'agent', 'agent_id', 'checkin_at', 'notes']
        read_only_fields = ['id', 'checkin_at', 'tenant']


class EventSampleSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    product = CatalogItemSerializer(read_only=True)
    product_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventSample
        fields = [
            'id', 'tenant', 'event', 'event_id', 'agent', 'agent_id',
            'product', 'product_id', 'product_name', 'sku',
            'quantity', 'distributed_at',
        ]
        read_only_fields = ['id', 'distributed_at', 'tenant']


class EventOrderSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    order = OrderSerializer(read_only=True)
    order_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventOrder
        fields = ['id', 'tenant', 'event', 'event_id', 'order', 'order_id', 'agent', 'agent_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'tenant']


class EventSaleSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    school_sale = SchoolSaleSerializer(read_only=True)
    school_sale_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventSale
        fields = ['id', 'tenant', 'event', 'event_id', 'school_sale', 'school_sale_id', 'created_by', 'created_by_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'tenant']


class EventLeadSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventLead
        fields = [
            'id', 'tenant', 'event', 'event_id', 'school', 'school_id',
            'agent', 'agent_id', 'name', 'phone', 'email', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


class EventTaskSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    completed_by = UserSerializer(read_only=True)
    completed_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventTask
        fields = [
            'id', 'tenant', 'event', 'event_id', 'title', 'description',
            'sort_order', 'completed', 'completed_at', 'completed_by', 'completed_by_id', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


class EventPhotoSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventPhoto
        fields = [
            'id', 'tenant', 'event', 'event_id', 'agent', 'agent_id',
            'photo_url', 'photo_path', 'caption', 'uploaded_at',
        ]
        read_only_fields = ['id', 'uploaded_at', 'tenant']


class EventReportSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    generated_by = UserSerializer(read_only=True)
    generated_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventReport
        fields = [
            'id', 'tenant', 'event', 'event_id', 'summary',
            'findings', 'recommendations', 'generated_by',
            'generated_by_id', 'generated_at',
        ]
        read_only_fields = ['id', 'generated_at', 'tenant']


class EventExpenseSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    approved_by = UserSerializer(read_only=True)
    approved_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = EventExpense
        fields = [
            'id', 'tenant', 'event', 'event_id', 'agent', 'agent_id',
            'description', 'amount', 'status', 'approved_by',
            'approved_by_id', 'approved_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  GEOFENCE
# ──────────────────────────────────────────────
class GeofenceSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Geofence
        fields = [
            'id', 'tenant', 'name', 'description', 'region',
            'coordinates', 'assigned_to', 'assigned_to_id',
            'created_by', 'created_by_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


class GeofenceEventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)
    geofence = GeofenceSerializer(read_only=True)
    geofence_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = GeofenceEvent
        fields = [
            'id', 'tenant', 'user', 'user_id', 'geofence', 'geofence_id',
            'event_type', 'region', 'latitude', 'longitude', 'reason',
            'status', 'created_at', 'resolved_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  SOCIAL CONVERSATION
# ──────────────────────────────────────────────
class SocialConversationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SocialConversation
        fields = [
            'id', 'tenant', 'title', 'created_by', 'created_by_id',
            'is_group', 'participant_ids', 'created_at', 'updated_at', 'messages',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


class SocialMessageSerializer(serializers.ModelSerializer):
    conversation = SocialConversationSerializer(read_only=True)
    conversation_id = serializers.CharField(write_only=True)
    sender = UserSerializer(read_only=True)
    sender_id = serializers.CharField(write_only=True)

    class Meta:
        model = SocialMessage
        fields = [
            'id', 'tenant', 'conversation', 'conversation_id',
            'sender', 'sender_id', 'body', 'msg_type', 'media_url',
            'is_read', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  DEBT COLLECTION
# ──────────────────────────────────────────────
class DebtCollectionSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    collected_by = UserSerializer(read_only=True)
    collected_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = DebtCollection
        fields = [
            'id', 'tenant', 'school', 'school_id', 'collected_by', 'collected_by_id',
            'amount', 'payment_method', 'payment_reference', 'notes',
            'collected_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'collected_at', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  OPPORTUNITY ACTIVITY
# ──────────────────────────────────────────────
class OpportunityActivitySerializer(serializers.ModelSerializer):
    sale = SchoolSaleSerializer(read_only=True)
    sale_id = serializers.CharField(write_only=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    actor = UserSerializer(read_only=True)
    actor_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = OpportunityActivity
        fields = [
            'id', 'tenant', 'sale', 'sale_id', 'school', 'school_id',
            'actor', 'actor_id', 'activity_type', 'outcome', 'notes',
            'next_action', 'next_action_date', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  PIPELINE HISTORY
# ──────────────────────────────────────────────
class PipelineHistorySerializer(serializers.ModelSerializer):
    sale = SchoolSaleSerializer(read_only=True)
    sale_id = serializers.CharField(write_only=True)
    changed_by = UserSerializer(read_only=True)
    changed_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = PipelineHistory
        fields = [
            'id', 'tenant', 'sale', 'sale_id', 'old_stage', 'new_stage',
            'changed_by', 'changed_by_id', 'changed_at', 'notes',
        ]
        read_only_fields = ['id', 'changed_at', 'tenant']


# ──────────────────────────────────────────────
#  PROFILE
# ──────────────────────────────────────────────
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'tenant', 'user', 'user_id',
            'display_name', 'avatar_url', 'bio', 'updated_at',
        ]
        read_only_fields = ['id', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  AUDIT EVENT
# ──────────────────────────────────────────────
class AuditEventSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    actor_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = AuditEvent
        fields = [
            'id', 'tenant', 'actor', 'actor_id', 'action',
            'entity_type', 'entity_id', 'region', 'before_data',
            'after_data', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  SUPERVISOR ALERT
# ──────────────────────────────────────────────
class SupervisorAlertSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = SupervisorAlert
        fields = [
            'id', 'tenant', 'user', 'user_id', 'region',
            'alert_type', 'severity', 'status', 'message',
            'acked_at', 'resolved_at', 'ack_sla_met',
            'resolve_sla_met', 'escalated_to_admin', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  SUPERVISOR INCIDENT
# ──────────────────────────────────────────────
class SupervisorIncidentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SupervisorIncident
        fields = [
            'id', 'tenant', 'user', 'user_id', 'region',
            'incident_type', 'severity', 'status', 'notes',
            'created_by', 'created_by_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  SUPERVISOR NOTE
# ──────────────────────────────────────────────
class SupervisorNoteSerializer(serializers.ModelSerializer):
    supervisor = UserSerializer(read_only=True)
    supervisor_id = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = SupervisorNote
        fields = [
            'id', 'tenant', 'supervisor', 'supervisor_id',
            'user', 'user_id', 'region', 'context_type',
            'context_id', 'note', 'follow_up_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  SUPERVISOR NOTIFICATION
# ──────────────────────────────────────────────
class SupervisorNotificationSerializer(serializers.ModelSerializer):
    supervisor = UserSerializer(read_only=True)
    supervisor_id = serializers.CharField(write_only=True)

    class Meta:
        model = SupervisorNotification
        fields = [
            'id', 'tenant', 'supervisor', 'supervisor_id',
            'region', 'notification_type', 'title', 'body',
            'payload', 'scheduled_for', 'sent_at', 'read_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'tenant']


# ──────────────────────────────────────────────
#  ROUTE PLAN
# ──────────────────────────────────────────────
class RoutePlanSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    reviewed_by = UserSerializer(read_only=True)
    reviewed_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = RoutePlan
        fields = [
            'id', 'tenant', 'title', 'route_date',
            'assigned_to', 'assigned_to_id', 'school_ids', 'notes',
            'status', 'created_by', 'created_by_id',
            'reviewed_by', 'reviewed_by_id', 'reviewed_at',
            'review_note', 'is_synced', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  SAMPLE REQUEST
# ──────────────────────────────────────────────
class SampleRequestSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    requested_by = UserSerializer(read_only=True)
    requested_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    reviewed_by = UserSerializer(read_only=True)
    reviewed_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SampleRequest
        fields = [
            'id', 'tenant', 'request_code', 'school', 'school_id',
            'client_type', 'requested_by', 'requested_by_id', 'purpose', 'notes',
            'status', 'rejection_reason', 'reviewed_by', 'reviewed_by_id',
            'reviewed_at', 'needed_by', 'requested_at', 'items',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'request_code', 'requested_at', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  VISITATION
# ──────────────────────────────────────────────
class VisitationSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True)
    agent = UserSerializer(read_only=True)
    agent_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Visitation
        fields = [
            'id', 'tenant', 'school', 'school_id', 'agent', 'agent_id',
            'visit_type', 'outcome', 'notes', 'latitude', 'longitude', 'visited_at',
        ]
        read_only_fields = ['id', 'visited_at', 'tenant']


# ──────────────────────────────────────────────
#  PROJECT FORM
# ──────────────────────────────────────────────
class ProjectFormSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = ProjectForm
        fields = [
            'id', 'tenant', 'title', 'description', 'fields',
            'is_active', 'created_by', 'created_by_id',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tenant']


# ──────────────────────────────────────────────
#  PROJECT FORM RESPONSE
# ──────────────────────────────────────────────
class ProjectFormResponseSerializer(serializers.ModelSerializer):
    form = ProjectFormSerializer(read_only=True)
    form_id = serializers.CharField(write_only=True)
    submitted_by = UserSerializer(read_only=True)
    submitted_by_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    school = SchoolSerializer(read_only=True)
    school_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = ProjectFormResponse
        fields = [
            'id', 'tenant', 'form', 'form_id', 'submitted_by', 'submitted_by_id',
            'school', 'school_id', 'responses', 'submitted_at',
        ]
        read_only_fields = ['id', 'submitted_at', 'tenant']
