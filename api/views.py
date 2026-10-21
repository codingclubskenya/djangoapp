from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

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
from api.serializers import (
    SchoolSerializer, RegionSerializer, SchoolSaleSerializer,
    SchoolFollowUpSerializer, SchoolVisitSerializer,
    VisitCheckinSerializer, TaskSerializer, MessageSerializer,
    CatalogItemSerializer, OrderSerializer, OrderItemSerializer,
    SchoolSampleDistributionSerializer, TargetSerializer,
    EventSerializer, EventAssignmentSerializer, EventCheckinSerializer,
    EventSampleSerializer, EventOrderSerializer, EventSaleSerializer,
    EventLeadSerializer, EventTaskSerializer, EventPhotoSerializer,
    EventReportSerializer, EventExpenseSerializer,
    GeofenceSerializer, GeofenceEventSerializer,
    SocialConversationSerializer, SocialMessageSerializer,
    DebtCollectionSerializer, OpportunityActivitySerializer,
    PipelineHistorySerializer, ProfileSerializer,
    AuditEventSerializer, SupervisorAlertSerializer,
    SupervisorIncidentSerializer, SupervisorNoteSerializer,
    SupervisorNotificationSerializer, RoutePlanSerializer,
    SampleRequestSerializer, VisitationSerializer,
    ProjectFormSerializer, ProjectFormResponseSerializer,
)
from common.permissions import TenantAccessPermission, RoleBasedPermission


class BaseTenantViewSet(viewsets.ModelViewSet):
    """Base viewset with tenant filtering, RBAC, and search/ordering."""
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission, TenantAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['-created_at']

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            return self.queryset.filter(tenant=tenant).all()
        return self.queryset.none()

    def perform_create(self, serializer):
        tenant_obj = getattr(self.request.user, 'tenant', None)
        if tenant_obj and 'tenant' not in serializer.validated_data:
            serializer.save(tenant=tenant_obj)
        else:
            serializer.save()


class SchoolViewSet(BaseTenantViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_fields = ['source', 'county', 'dealer_type', 'is_synced', 'created_at']
    search_fields = ['name', 'phone', 'county', 'contact_name']
    ordering_fields = ['name', 'created_at', 'updated_at', 'county']


class RegionViewSet(BaseTenantViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_fields = ['name', 'sub_region']
    search_fields = ['name', 'sub_region']
    ordering_fields = ['name', 'created_at']


class SchoolSaleViewSet(BaseTenantViewSet):
    queryset = SchoolSale.objects.all()
    serializer_class = SchoolSaleSerializer
    filterset_fields = ['stage', 'sale_status', 'risk_level', 'is_synced', 'school_id', 'agent_id']
    search_fields = ['package_name', 'notes']
    ordering_fields = ['expected_value', 'probability', 'created_at', 'stage_updated_at', 'closed_at']

    @action(detail=False, methods=['get'])
    def by_agent(self, request):
        agent_id = request.query_params.get('agent_id')
        if agent_id:
            self.queryset = self.queryset.filter(agent_id=agent_id)
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class SchoolFollowUpViewSet(BaseTenantViewSet):
    queryset = SchoolFollowUp.objects.all()
    serializer_class = SchoolFollowUpSerializer
    filterset_fields = ['status', 'follow_up_status', 'school_id', 'agent_id']
    search_fields = ['notes', 'next_step']
    ordering_fields = ['due_at', 'created_at', 'completed_at']


class SchoolVisitViewSet(BaseTenantViewSet):
    queryset = SchoolVisit.objects.all()
    serializer_class = SchoolVisitSerializer
    filterset_fields = ['visit_status', 'school_id', 'agent_id']
    search_fields = ['notes', 'outcome']
    ordering_fields = ['visited_at', 'created_at']


class VisitCheckinViewSet(BaseTenantViewSet):
    queryset = VisitCheckin.objects.all()
    serializer_class = VisitCheckinSerializer
    filterset_fields = ['agent_id', 'school_id']
    ordering_fields = ['checkin_at', 'checkout_at']

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        instance = self.get_object()
        from django.utils import timezone
        instance.checkout_at = timezone.now()
        instance.save()
        return Response({'status': 'checked_out'})


class TaskViewSet(BaseTenantViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'target_role', 'assigned_to', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['due_at', 'created_at', 'updated_at']


class MessageViewSet(BaseTenantViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['is_read', 'sender_id', 'recipient_id']
    search_fields = ['subject', 'body']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        return Response({'status': 'marked_read'})

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        msgs = self.get_queryset().filter(recipient=request.user)
        page = self.paginate_queryset(msgs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.get_serializer(msgs, many=True).data)


class CatalogItemViewSet(BaseTenantViewSet):
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    filterset_fields = ['category', 'item_type', 'is_active']
    search_fields = ['name', 'sku', 'category']
    ordering_fields = ['name', 'unit_price', 'created_at']


class OrderViewSet(BaseTenantViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['status', 'payment_method', 'school_id', 'agent_id', 'order_number']
    search_fields = ['order_number', 'notes']
    ordering_fields = ['created_at', 'submitted_at', 'approved_at', 'checkout_amount']


class OrderItemViewSet(BaseTenantViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filterset_fields = ['order_id', 'category', 'sku']
    search_fields = ['product_name', 'sku']
    ordering_fields = ['created_at']


class SchoolSampleDistributionViewSet(BaseTenantViewSet):
    queryset = SchoolSampleDistribution.objects.all()
    serializer_class = SchoolSampleDistributionSerializer
    filterset_fields = ['school_id', 'agent_id', 'sample_category']
    search_fields = ['sample_name']
    ordering_fields = ['distributed_at', 'created_at']


class TargetViewSet(BaseTenantViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filterset_fields = ['scope', 'target_type', 'target_period', 'region_id', 'assigned_to']
    ordering_fields = ['created_at']


class EventViewSet(BaseTenantViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ['status', 'event_type', 'region']
    search_fields = ['name']
    ordering_fields = ['start_at', 'end_at', 'created_at']


class EventAssignmentViewSet(BaseTenantViewSet):
    queryset = EventAssignment.objects.all()
    serializer_class = EventAssignmentSerializer
    filterset_fields = ['event_id', 'agent_id', 'role']
    ordering_fields = ['assigned_at']


class EventCheckinViewSet(BaseTenantViewSet):
    queryset = EventCheckin.objects.all()
    serializer_class = EventCheckinSerializer
    filterset_fields = ['event_id', 'agent_id']
    ordering_fields = ['checkin_at']


class EventSampleViewSet(BaseTenantViewSet):
    queryset = EventSample.objects.all()
    serializer_class = EventSampleSerializer
    filterset_fields = ['event_id', 'agent_id', 'product_id']
    ordering_fields = ['distributed_at']


class EventOrderViewSet(BaseTenantViewSet):
    queryset = EventOrder.objects.all()
    serializer_class = EventOrderSerializer
    filterset_fields = ['event_id', 'agent_id']
    ordering_fields = ['created_at']


class EventSaleViewSet(BaseTenantViewSet):
    queryset = EventSale.objects.all()
    serializer_class = EventSaleSerializer
    filterset_fields = ['event_id', 'created_by']
    ordering_fields = ['created_at']


class EventLeadViewSet(BaseTenantViewSet):
    queryset = EventLead.objects.all()
    serializer_class = EventLeadSerializer
    filterset_fields = ['event_id', 'agent_id', 'school_id']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['created_at']


class EventTaskViewSet(BaseTenantViewSet):
    queryset = EventTask.objects.all()
    serializer_class = EventTaskSerializer
    filterset_fields = ['event_id', 'completed']
    search_fields = ['title', 'description']
    ordering_fields = ['sort_order', 'created_at']


class EventPhotoViewSet(BaseTenantViewSet):
    queryset = EventPhoto.objects.all()
    serializer_class = EventPhotoSerializer
    filterset_fields = ['event_id', 'agent_id']
    ordering_fields = ['uploaded_at']


class EventReportViewSet(BaseTenantViewSet):
    queryset = EventReport.objects.all()
    serializer_class = EventReportSerializer
    filterset_fields = ['event_id']
    ordering_fields = ['generated_at']


class EventExpenseViewSet(BaseTenantViewSet):
    queryset = EventExpense.objects.all()
    serializer_class = EventExpenseSerializer
    filterset_fields = ['event_id', 'agent_id', 'status']
    ordering_fields = ['created_at']


class GeofenceViewSet(BaseTenantViewSet):
    queryset = Geofence.objects.all()
    serializer_class = GeofenceSerializer
    filterset_fields = ['region', 'assigned_to']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class GeofenceEventViewSet(BaseTenantViewSet):
    queryset = GeofenceEvent.objects.all()
    serializer_class = GeofenceEventSerializer
    filterset_fields = ['user_id', 'geofence_id', 'status', 'region']
    search_fields = ['reason']
    ordering_fields = ['created_at', 'resolved_at']


class SocialConversationViewSet(viewsets.ModelViewSet):
    queryset = SocialConversation.objects.all()
    serializer_class = SocialConversationSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            return self.queryset.filter(tenant=tenant, participant_ids__contains=[str(self.request.user.id)]).all()
        return self.queryset.none()

    def perform_create(self, serializer):
        tenant_obj = getattr(self.request.user, 'tenant', None)
        if tenant_obj:
            serializer.save(tenant=tenant_obj, participant_ids=[str(self.request.user.id)])
        else:
            serializer.save()


class SocialMessageViewSet(viewsets.ModelViewSet):
    queryset = SocialMessage.objects.all()
    serializer_class = SocialMessageSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.queryset.none()
        conv_id = self.request.query_params.get('conversation_id')
        if conv_id:
            return self.queryset.filter(tenant=tenant, conversation_id=conv_id)
        return self.queryset.filter(
            tenant=tenant,
            conversation__participant_ids__contains=[str(self.request.user.id)],
        )


class DebtCollectionViewSet(BaseTenantViewSet):
    queryset = DebtCollection.objects.all()
    serializer_class = DebtCollectionSerializer
    filterset_fields = ['school_id', 'collected_by', 'payment_method']
    search_fields = ['payment_reference', 'notes']
    ordering_fields = ['collected_at', 'created_at', 'amount']


class OpportunityActivityViewSet(BaseTenantViewSet):
    queryset = OpportunityActivity.objects.all()
    serializer_class = OpportunityActivitySerializer
    filterset_fields = ['sale_id', 'school_id', 'actor_id', 'activity_type']
    search_fields = ['notes', 'outcome']
    ordering_fields = ['created_at']


class PipelineHistoryViewSet(BaseTenantViewSet):
    queryset = PipelineHistory.objects.all()
    serializer_class = PipelineHistorySerializer
    filterset_fields = ['sale_id', 'changed_by']
    ordering_fields = ['changed_at']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission, TenantAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['display_name', 'user__email']
    ordering_fields = ['updated_at']

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            return self.queryset.filter(tenant=tenant).all()
        return self.queryset.none()

    def perform_create(self, serializer):
        tenant_obj = getattr(self.request.user, 'tenant', None)
        if tenant_obj:
            serializer.save(tenant=tenant_obj)
        else:
            serializer.save()


class AuditEventViewSet(BaseTenantViewSet):
    queryset = AuditEvent.objects.all()
    serializer_class = AuditEventSerializer
    filterset_fields = ['action', 'entity_type', 'entity_id']
    search_fields = ['action', 'entity_type']
    ordering_fields = ['created_at']


class SupervisorAlertViewSet(BaseTenantViewSet):
    queryset = SupervisorAlert.objects.all()
    serializer_class = SupervisorAlertSerializer
    filterset_fields = ['user_id', 'status', 'severity', 'alert_type', 'region']
    ordering_fields = ['created_at', 'acked_at', 'resolved_at']


class SupervisorIncidentViewSet(BaseTenantViewSet):
    queryset = SupervisorIncident.objects.all()
    serializer_class = SupervisorIncidentSerializer
    filterset_fields = ['user_id', 'status', 'severity', 'incident_type', 'region']
    ordering_fields = ['created_at', 'updated_at']


class SupervisorNoteViewSet(BaseTenantViewSet):
    queryset = SupervisorNote.objects.all()
    serializer_class = SupervisorNoteSerializer
    filterset_fields = ['supervisor_id', 'user_id', 'region', 'context_type']
    search_fields = ['note']
    ordering_fields = ['created_at', 'follow_up_at']


class SupervisorNotificationViewSet(BaseTenantViewSet):
    queryset = SupervisorNotification.objects.all()
    serializer_class = SupervisorNotificationSerializer
    filterset_fields = ['supervisor_id', 'status', 'notification_type', 'region']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at', 'sent_at', 'read_at']


class RoutePlanViewSet(BaseTenantViewSet):
    queryset = RoutePlan.objects.all()
    serializer_class = RoutePlanSerializer
    filterset_fields = ['status', 'route_date', 'assigned_to', 'created_by']
    search_fields = ['title', 'notes']
    ordering_fields = ['route_date', 'created_at', 'updated_at']


class SampleRequestViewSet(BaseTenantViewSet):
    queryset = SampleRequest.objects.all()
    serializer_class = SampleRequestSerializer
    filterset_fields = ['status', 'school_id', 'requested_by', 'client_type']
    search_fields = ['request_code', 'purpose', 'notes']
    ordering_fields = ['requested_at', 'created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'approved'
        instance.reviewed_by = request.user
        from django.utils import timezone
        instance.reviewed_at = timezone.now()
        instance.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'rejected'
        instance.reviewed_by = request.user
        from django.utils import timezone
        instance.reviewed_at = timezone.now()
        rejection_reason = request.data.get('rejection_reason', '')
        if rejection_reason:
            instance.rejection_reason = rejection_reason
            instance.save()
        return Response({'status': 'rejected'})


class VisitationViewSet(BaseTenantViewSet):
    queryset = Visitation.objects.all()
    serializer_class = VisitationSerializer
    filterset_fields = ['school_id', 'agent_id', 'visit_type']
    search_fields = ['notes', 'outcome']
    ordering_fields = ['visited_at', 'created_at']


class ProjectFormViewSet(BaseTenantViewSet):
    queryset = ProjectForm.objects.all()
    serializer_class = ProjectFormSerializer
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']


class ProjectFormResponseViewSet(BaseTenantViewSet):
    queryset = ProjectFormResponse.objects.all()
    serializer_class = ProjectFormResponseSerializer
    filterset_fields = ['form_id', 'submitted_by', 'school_id']
    ordering_fields = ['submitted_at']
