from django.contrib import admin
from tenant.models import Tenant
from users.models import User
from api.models import (
    School, Region, SchoolSale, SchoolFollowUp, SchoolVisit,
    VisitCheckin, Task, Message, CatalogItem, Order, OrderItem,
    SchoolSampleDistribution, Target, Event, EventAssignment,
    EventCheckin, EventSample, EventOrder, EventSale, EventLead,
    EventTask, EventPhoto, EventReport, EventExpense,
    Geofence, GeofenceEvent, SocialConversation, SocialMessage,
    DebtCollection, OpportunityActivity, PipelineHistory,
    Profile, AuditEvent, SupervisorAlert, SupervisorIncident,
    SupervisorNote, SupervisorNotification, RoutePlan,
    SampleRequest, Visitation, ProjectForm, ProjectFormResponse,
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'is_active', 'created_at')
    list_filter = ('is_active',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'tenant', 'created_at')
    list_filter = ('role', 'tenant')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'county', 'phone', 'source', 'captured_by', 'tenant', 'is_synced')
    list_filter = ('source', 'county', 'tenant', 'is_synced', 'created_at')
    search_fields = ('name', 'phone', 'county')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_region', 'assigned_to', 'supervisor', 'tenant', 'created_at')
    list_filter = ('tenant', 'created_at')
    search_fields = ('name', 'sub_region')


@admin.register(SchoolSale)
class SchoolSaleAdmin(admin.ModelAdmin):
    list_display = ('school', 'agent', 'stage', 'expected_value', 'probability', 'is_synced', 'created_at')
    list_filter = ('stage', 'risk_level', 'tenant', 'is_synced', 'created_at')
    search_fields = ('school__name', 'package_name')


@admin.register(SchoolFollowUp)
class SchoolFollowUpAdmin(admin.ModelAdmin):
    list_display = ('school', 'agent', 'status', 'due_at', 'is_synced')
    list_filter = ('status', 'tenant', 'is_synced')
    search_fields = ('school__name', 'notes')


@admin.register(SchoolVisit)
class SchoolVisitAdmin(admin.ModelAdmin):
    list_display = ('school', 'agent', 'status', 'visited_at', 'is_synced')
    list_filter = ('status', 'tenant', 'is_synced')
    search_fields = ('school__name', 'outcome')


@admin.register(VisitCheckin)
class VisitCheckinAdmin(admin.ModelAdmin):
    list_display = ('agent', 'school', 'checkin_at', 'checkout_at')
    list_filter = ('tenant', 'checkin_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'due_at', 'created_at')
    list_filter = ('status', 'target_role', 'tenant')
    search_fields = ('title', 'description')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'is_read', 'created_at')
    list_filter = ('is_read', 'tenant', 'created_at')
    search_fields = ('subject', 'body')


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sku', 'unit_price', 'stock_qty', 'is_active')
    list_filter = ('category', 'is_active', 'tenant')
    search_fields = ('name', 'sku', 'category')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'school', 'agent', 'status', 'checkout_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'tenant')
    search_fields = ('order_number', 'school_name')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'unit_price', 'line_total')
    list_filter = ('tenant',)
    search_fields = ('product_name', 'sku')


@admin.register(SchoolSampleDistribution)
class SchoolSampleDistributionAdmin(admin.ModelAdmin):
    list_display = ('school', 'agent', 'sample_name', 'quantity', 'distributed_at')
    list_filter = ('tenant', 'sample_category', 'distributed_at')
    search_fields = ('sample_name', 'school__name')


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('scope', 'target_type', 'target_period', 'assigned_to', 'created_at')
    list_filter = ('scope', 'target_type', 'target_period', 'tenant')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'status', 'start_at', 'end_at', 'created_at')
    list_filter = ('status', 'event_type', 'tenant')
    search_fields = ('name', 'description')


@admin.register(EventAssignment)
class EventAssignmentAdmin(admin.ModelAdmin):
    list_display = ('event', 'agent', 'role', 'assigned_at')
    list_filter = ('tenant', 'event')


@admin.register(EventCheckin)
class EventCheckinAdmin(admin.ModelAdmin):
    list_display = ('event', 'agent', 'checkin_at')
    list_filter = ('tenant', 'event')


@admin.register(EventSample)
class EventSampleAdmin(admin.ModelAdmin):
    list_display = ('event', 'agent', 'product_name', 'quantity', 'distributed_at')
    list_filter = ('tenant', 'event')


@admin.register(EventOrder)
class EventOrderAdmin(admin.ModelAdmin):
    list_display = ('event', 'order', 'agent', 'created_at')
    list_filter = ('tenant', 'event')


@admin.register(EventSale)
class EventSaleAdmin(admin.ModelAdmin):
    list_display = ('event', 'school_sale', 'created_by', 'created_at')
    list_filter = ('tenant', 'event')


@admin.register(EventLead)
class EventLeadAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'agent', 'created_at')
    list_filter = ('tenant', 'event')


@admin.register(EventTask)
class EventTaskAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'completed', 'completed_at')
    list_filter = ('tenant', 'event', 'completed')


@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ('event', 'agent', 'caption', 'uploaded_at')
    list_filter = ('tenant', 'event')


@admin.register(EventReport)
class EventReportAdmin(admin.ModelAdmin):
    list_display = ('event', 'generated_by', 'generated_at')
    list_filter = ('tenant',)


@admin.register(EventExpense)
class EventExpenseAdmin(admin.ModelAdmin):
    list_display = ('event', 'agent', 'description', 'amount', 'status')
    list_filter = ('tenant', 'status')


@admin.register(Geofence)
class GeofenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'assigned_to', 'created_at')
    list_filter = ('tenant', 'region')


@admin.register(GeofenceEvent)
class GeofenceEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'geofence', 'event_type', 'status', 'created_at')
    list_filter = ('tenant', 'status', 'event_type')


@admin.register(SocialConversation)
class SocialConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_group', 'created_at')
    list_filter = ('tenant', 'is_group')


@admin.register(SocialMessage)
class SocialMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'msg_type', 'created_at')
    list_filter = ('tenant', 'msg_type')


@admin.register(DebtCollection)
class DebtCollectionAdmin(admin.ModelAdmin):
    list_display = ('school', 'collected_by', 'amount', 'collected_at')
    list_filter = ('tenant', 'payment_method')


@admin.register(OpportunityActivity)
class OpportunityActivitySerializerAdmin(admin.ModelAdmin):
    list_display = ('sale', 'activity_type', 'actor', 'created_at')
    list_filter = ('tenant', 'activity_type')


@admin.register(PipelineHistory)
class PipelineHistoryAdmin(admin.ModelAdmin):
    list_display = ('sale', 'old_stage', 'new_stage', 'changed_by', 'changed_at')
    list_filter = ('tenant',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'updated_at')
    list_filter = ('tenant',)


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('action', 'entity_type', 'entity_id', 'actor', 'created_at')
    list_filter = ('tenant', 'action', 'entity_type')


@admin.register(SupervisorAlert)
class SupervisorAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert_type', 'severity', 'status', 'created_at')
    list_filter = ('tenant', 'severity', 'status', 'alert_type')


@admin.register(SupervisorIncident)
class SupervisorIncidentAdmin(admin.ModelAdmin):
    list_display = ('user', 'incident_type', 'severity', 'status', 'created_at')
    list_filter = ('tenant', 'severity', 'status')


@admin.register(SupervisorNote)
class SupervisorNoteAdmin(admin.ModelAdmin):
    list_display = ('supervisor', 'user', 'context_type', 'created_at')
    list_filter = ('tenant', 'context_type')


@admin.register(SupervisorNotification)
class SupervisorNotificationAdmin(admin.ModelAdmin):
    list_display = ('supervisor', 'title', 'notification_type', 'sent_at')
    list_filter = ('tenant', 'notification_type', 'sent_at')


@admin.register(RoutePlan)
class RoutePlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'route_date', 'assigned_to', 'status', 'created_at')
    list_filter = ('tenant', 'status', 'route_date')


@admin.register(SampleRequest)
class SampleRequestAdmin(admin.ModelAdmin):
    list_display = ('request_code', 'school', 'requested_by', 'status', 'created_at')
    list_filter = ('tenant', 'status', 'client_type')


@admin.register(Visitation)
class VisitationAdmin(admin.ModelAdmin):
    list_display = ('school', 'agent', 'visit_type', 'visited_at')
    list_filter = ('tenant', 'visit_type')


@admin.register(ProjectForm)
class ProjectFormAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_by', 'created_at')
    list_filter = ('tenant', 'is_active')


@admin.register(ProjectFormResponse)
class ProjectFormResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'submitted_by', 'school', 'submitted_at')
    list_filter = ('tenant', 'form')
