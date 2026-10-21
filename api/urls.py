from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    SchoolViewSet, RegionViewSet, SchoolSaleViewSet,
    SchoolFollowUpViewSet, SchoolVisitViewSet, VisitCheckinViewSet,
    TaskViewSet, MessageViewSet, CatalogItemViewSet,
    OrderViewSet, OrderItemViewSet, SchoolSampleDistributionViewSet,
    TargetViewSet, EventViewSet, EventAssignmentViewSet,
    EventCheckinViewSet, EventSampleViewSet, EventOrderViewSet,
    EventSaleViewSet, EventLeadViewSet, EventTaskViewSet,
    EventPhotoViewSet, EventReportViewSet, EventExpenseViewSet,
    GeofenceViewSet, GeofenceEventViewSet,
    SocialConversationViewSet, SocialMessageViewSet,
    DebtCollectionViewSet, OpportunityActivityViewSet,
    PipelineHistoryViewSet, ProfileViewSet, AuditEventViewSet,
    SupervisorAlertViewSet, SupervisorIncidentViewSet,
    SupervisorNoteViewSet, SupervisorNotificationViewSet,
    RoutePlanViewSet, SampleRequestViewSet,
    VisitationViewSet, ProjectFormViewSet, ProjectFormResponseViewSet,
)

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'sales', SchoolSaleViewSet)
router.register(r'follow-ups', SchoolFollowUpViewSet)
router.register(r'visits', SchoolVisitViewSet)
router.register(r'checkins', VisitCheckinViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'catalog', CatalogItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'samples/distributions', SchoolSampleDistributionViewSet)
router.register(r'targets', TargetViewSet)
router.register(r'events', EventViewSet)
router.register(r'events/assignments', EventAssignmentViewSet)
router.register(r'events/checkins', EventCheckinViewSet)
router.register(r'events/samples', EventSampleViewSet)
router.register(r'events/orders', EventOrderViewSet)
router.register(r'events/sales', EventSaleViewSet)
router.register(r'events/leads', EventLeadViewSet)
router.register(r'events/tasks', EventTaskViewSet)
router.register(r'events/photos', EventPhotoViewSet)
router.register(r'events/reports', EventReportViewSet)
router.register(r'events/expenses', EventExpenseViewSet)
router.register(r'geofences', GeofenceViewSet)
router.register(r'geofence-events', GeofenceEventViewSet)
router.register(r'social/conversations', SocialConversationViewSet)
router.register(r'social/messages', SocialMessageViewSet)
router.register(r'debt-collections', DebtCollectionViewSet)
router.register(r'opportunity-activities', OpportunityActivityViewSet)
router.register(r'pipeline-history', PipelineHistoryViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'audit-events', AuditEventViewSet)
router.register(r'supervisor/alerts', SupervisorAlertViewSet)
router.register(r'supervisor/incidents', SupervisorIncidentViewSet)
router.register(r'supervisor/notes', SupervisorNoteViewSet)
router.register(r'supervisor/notifications', SupervisorNotificationViewSet)
router.register(r'route-plans', RoutePlanViewSet)
router.register(r'sample-requests', SampleRequestViewSet)
router.register(r'visitations', VisitationViewSet)
router.register(r'project/forms', ProjectFormViewSet)
router.register(r'project/form-responses', ProjectFormResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
