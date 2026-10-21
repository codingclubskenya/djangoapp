import uuid

from django.db import models
from django.db.models import JSONField

from common.managers import TenantAwareManager
from tenant.models import Tenant
from users.models import User


def _uuid():
    return str(uuid.uuid4())


# ──────────────────────────────────────────────
#  REGION
# ──────────────────────────────────────────────
class Region(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    name = models.CharField(max_length=100)
    sub_region = models.CharField(max_length=100, null=True, blank=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='assigned_to', related_name='assigned_regions',
    )
    supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='supervisor_id', related_name='supervised_regions',
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_regions',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'regions'

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
#  SCHOOL SALE  (Opportunity)
# ──────────────────────────────────────────────
class SchoolSale(models.Model):
    STAGE_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('dormant', 'Dormant'),
    ]
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
        ('dormant', 'Dormant'),
    ]
    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='sales',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='school_sales',
    )
    package_name = models.CharField(max_length=255, null=True, blank=True)
    expected_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    stage = models.CharField(max_length=50, default='lead', db_column='sale_status', choices=STATUS_CHOICES)
    contact_person = models.CharField(max_length=255, null=True, blank=True, db_column='stage_contact_person')
    sample_quantity = models.IntegerField(null=True, blank=True)
    quotation_reference = models.CharField(max_length=255, null=True, blank=True)
    decision_owner = models.CharField(max_length=255, null=True, blank=True)
    negotiation_topic = models.TextField(null=True, blank=True)
    loss_reason = models.TextField(null=True, blank=True)
    dormant_reason = models.TextField(null=True, blank=True)
    stage_updated_at = models.DateTimeField(null=True, blank=True)
    expected_close_date = models.DateField(null=True, blank=True)
    probability = models.IntegerField(default=0)
    closed_at = models.DateTimeField(null=True, blank=True)
    next_action = models.TextField(null=True, blank=True)
    next_action_date = models.DateField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)
    risk_level = models.CharField(max_length=50, default='low', choices=RISK_CHOICES)
    weighted_forecast = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stage_sla_due_at = models.DateTimeField(null=True, blank=True)
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'school_sales'

    def __str__(self):
        return f"{self.school.name} - {self.stage}"


# ──────────────────────────────────────────────
#  SCHOOL FOLLOW-UP
# ──────────────────────────────────────────────
class SchoolFollowUp(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='followups',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='school_followups',
    )
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    next_step = models.TextField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='open', choices=STATUS_CHOICES, db_column='follow_up_status')
    completed_at = models.DateTimeField(null=True, blank=True)
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'school_follow_ups'

    def __str__(self):
        return f"Follow-up for {self.school.name}"


# ──────────────────────────────────────────────
#  SCHOOL VISIT
# ──────────────────────────────────────────────
class SchoolVisit(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='visits',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='school_visits',
    )
    outcome = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True, db_column='photo_url')
    photo_path = models.TextField(null=True, blank=True, db_column='photo_path')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, default='completed', db_column='visit_status')
    visited_at = models.DateTimeField(auto_now_add=True, db_column='visited_at')
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'school_visits'

    def __str__(self):
        return f"Visit to {self.school.name}"


# ──────────────────────────────────────────────
#  VISIT CHECKIN
# ──────────────────────────────────────────────
class VisitCheckin(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='agent_id', related_name='checkins',
    )
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='checkins',
    )
    checkin_at = models.DateTimeField(auto_now_add=True, db_column='checkin_at')
    checkout_at = models.DateTimeField(null=True, blank=True, db_column='checkout_at')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'visit_checkins'

    def __str__(self):
        return f"Check-in by {self.agent.email}"


# ──────────────────────────────────────────────
#  TASK
# ──────────────────────────────────────────────
class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target_role = models.IntegerField(default=2)
    due_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='open', choices=STATUS_CHOICES)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_tasks',
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='assigned_to', related_name='assigned_tasks',
    )
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  MESSAGE
# ──────────────────────────────────────────────
class Message(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='sender_id', related_name='sent_messages',
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='recipient_id', related_name='received_messages',
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    related_school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='related_school_id', related_name='messages',
    )
    related_task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='related_task_id', related_name='messages',
    )
    is_read = models.BooleanField(default=False, db_column='is_read')
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


# ──────────────────────────────────────────────
#  CATALOG ITEM
# ──────────────────────────────────────────────
class CatalogItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('sale', 'Sale Item'),
        ('sample', 'Sample Item'),
        ('service', 'Service'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    sku = models.CharField(max_length=255, unique=True, null=True, blank=True)
    item_type = models.CharField(max_length=50, default='sale', choices=ITEM_TYPE_CHOICES)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stock_qty = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_column='is_active')
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_catalog_items',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'catalog_items'

    def __str__(self):
        return f"{self.name} ({self.sku})"


# ──────────────────────────────────────────────
#  ORDER
# ──────────────────────────────────────────────
class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='orders',
    )
    school_name = models.CharField(max_length=255, null=True, blank=True, db_column='school_name')
    school_phone = models.CharField(max_length=50, null=True, blank=True, db_column='school_phone')
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='orders',
    )
    order_number = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment_method = models.CharField(max_length=50, default='cash', choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=255, null=True, blank=True)
    checkout_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default='pending', choices=STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number or f"Order #{self.id}"


# ──────────────────────────────────────────────
#  ORDER ITEM
# ──────────────────────────────────────────────
class OrderItem(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, db_column='order_id', related_name='items',
    )
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(null=True, blank=True)
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


# ──────────────────────────────────────────────
#  SAMPLE DISTRIBUTION
# ──────────────────────────────────────────────
class SchoolSampleDistribution(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='sample_distributions',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='sample_distributions',
    )
    sample_name = models.CharField(max_length=255)
    sample_category = models.CharField(max_length=100, null=True, blank=True)
    client_type = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    returned_qty = models.IntegerField(default=0)
    stamped_receipt_url = models.TextField(null=True, blank=True, db_column='stamped_receipt_url')
    stamped_receipt_path = models.TextField(null=True, blank=True, db_column='stamped_receipt_path')
    notes = models.TextField(null=True, blank=True)
    distributed_at = models.DateTimeField(auto_now_add=True, db_column='distributed_at')
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'school_sample_distributions'

    def __str__(self):
        return f"{self.sample_name} → {self.school.name}"


# ──────────────────────────────────────────────
#  TARGET
# ──────────────────────────────────────────────
class Target(models.Model):
    SCOPE_CHOICES = [
        ('agent', 'Agent'),
        ('region', 'Region'),
        ('tenant', 'Tenant'),
    ]
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    scope = models.CharField(max_length=50, choices=SCOPE_CHOICES)
    target_type = models.CharField(max_length=50)
    target_period = models.CharField(max_length=50, choices=PERIOD_CHOICES, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='region_id', related_name='targets',
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='assigned_to', related_name='targets',
    )
    target_data = JSONField(null=True, blank=True, db_column='target_data')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'targets'

    def __str__(self):
        return f"{self.target_type} - {self.scope}"


# ──────────────────────────────────────────────
#  EVENT  (Campaign / Trade Show)
# ──────────────────────────────────────────────
class Event(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    expected_attendance = models.IntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, default='planned', choices=STATUS_CHOICES)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_events',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
#  EVENT ASSIGNMENT
# ──────────────────────────────────────────────
class EventAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='assignments',
    )
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='agent_id', related_name='event_assignments',
    )
    role = models.CharField(max_length=50, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True, db_column='assigned_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_assignments'
        unique_together = ('event', 'agent')

    def __str__(self):
        return f"{self.agent.email} → {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT CHECK-IN
# ──────────────────────────────────────────────
class EventCheckin(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='checkins',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_checkins',
    )
    checkin_at = models.DateTimeField(auto_now_add=True, db_column='checkin_at')
    notes = models.TextField(null=True, blank=True)

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_checkins'

    def __str__(self):
        return f"Check-in at {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT SAMPLE
# ──────────────────────────────────────────────
class EventSample(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='samples',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_samples',
    )
    product = models.ForeignKey(
        CatalogItem, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='product_id', related_name='event_samples',
    )
    product_name = models.CharField(max_length=255, null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    distributed_at = models.DateTimeField(auto_now_add=True, db_column='distributed_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_samples'

    def __str__(self):
        return f"{self.product_name} @ {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT ORDER
# ──────────────────────────────────────────────
class EventOrder(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='orders',
    )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='order_id', related_name='event_orders',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_orders',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_orders'

    def __str__(self):
        return f"Order for {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT SALE
# ──────────────────────────────────────────────
class EventSale(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='sales',
    )
    school_sale = models.ForeignKey(
        SchoolSale, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_sale_id', related_name='event_sales',
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_event_sales',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_sales'

    def __str__(self):
        return f"Sale at {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT LEAD
# ──────────────────────────────────────────────
class EventLead(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='leads',
    )
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='event_leads',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_leads',
    )
    name = models.CharField(max_length=255, null=True, blank=True, db_column='lead_name')
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_leads'

    def __str__(self):
        return f"Lead at {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT TASK
# ──────────────────────────────────────────────
class EventTask(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='tasks',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='completed_by', related_name='completed_event_tasks',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_tasks'

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  EVENT PHOTO
# ──────────────────────────────────────────────
class EventPhoto(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='photos',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_photos',
    )
    photo_url = models.TextField(null=True, blank=True, db_column='photo_url')
    photo_path = models.TextField(null=True, blank=True, db_column='photo_path')
    caption = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column='uploaded_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_photos'

    def __str__(self):
        return f"Photo @ {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT REPORT
# ──────────────────────────────────────────────
class EventReport(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='report',
    )
    summary = models.TextField(null=True, blank=True)
    findings = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    generated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='generated_by', related_name='generated_event_reports',
    )
    generated_at = models.DateTimeField(auto_now_add=True, db_column='generated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_reports'

    def __str__(self):
        return f"Report for {self.event.name}"


# ──────────────────────────────────────────────
#  EVENT EXPENSE
# ──────────────────────────────────────────────
class EventExpense(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, db_column='event_id', related_name='expenses',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='event_expenses',
    )
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='approved_by', related_name='approved_event_expenses',
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'event_expenses'

    def __str__(self):
        return f"Expense @ {self.event.name}"


# ──────────────────────────────────────────────
#  GEOFENCE
# ──────────────────────────────────────────────
class Geofence(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    coordinates = JSONField(null=True, blank=True, db_column='coordinates')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='assigned_to', related_name='assigned_geofences',
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_geofences',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'geofences'

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
#  GEOFENCE EVENT
# ──────────────────────────────────────────────
class GeofenceEvent(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='geofence_events',
    )
    geofence = models.ForeignKey(
        Geofence, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='geofence_id', related_name='events',
    )
    event_type = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, db_column='lat')
    longitude = models.FloatField(null=True, blank=True, db_column='lng')
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='open', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    resolved_at = models.DateTimeField(null=True, blank=True)

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'geofence_events'

    def __str__(self):
        return f"{self.event_type} for {self.user.email}"


# ──────────────────────────────────────────────
#  SOCIAL CONVERSATION
# ──────────────────────────────────────────────
class SocialConversation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_conversations',
    )
    is_group = models.BooleanField(default=False, db_column='is_group')
    participant_ids = JSONField(null=True, blank=True, db_column='participant_ids')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'social_conversations'

    def __str__(self):
        return self.title or f"Conversation {self.id}"


# ──────────────────────────────────────────────
#  SOCIAL MESSAGE
# ──────────────────────────────────────────────
class SocialMessage(models.Model):
    MSG_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('file', 'File'),
        ('system', 'System'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    conversation = models.ForeignKey(
        SocialConversation, on_delete=models.CASCADE,
        db_column='conversation_id', related_name='messages',
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='sender_id', related_name='social_messages',
    )
    body = models.TextField(null=True, blank=True)
    msg_type = models.CharField(max_length=50, default='text', choices=MSG_TYPE_CHOICES, db_column='type')
    media_url = models.TextField(null=True, blank=True, db_column='media_url')
    is_read = models.BooleanField(default=False, db_column='is_read')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'social_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"Message in {self.conversation}"


# ──────────────────────────────────────────────
#  DEBT COLLECTION
# ──────────────────────────────────────────────
class DebtCollection(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='debt_collections',
    )
    collected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='collected_by', related_name='debt_collections',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cash')
    payment_reference = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True, db_column='collected_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'debt_collections'

    def __str__(self):
        return f"KES {self.amount} from {self.school.name}"


# ──────────────────────────────────────────────
#  OPPORTUNITY ACTIVITY
# ──────────────────────────────────────────────
class OpportunityActivity(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    sale = models.ForeignKey(
        SchoolSale, on_delete=models.CASCADE, db_column='opportunity_id', related_name='activities',
    )
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='opportunity_activities',
    )
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='actor_id', related_name='opportunity_activities',
    )
    activity_type = models.CharField(max_length=100)
    outcome = models.TextField(null=True, blank=True, db_column='activity_outcome')
    notes = models.TextField(null=True, blank=True)
    next_action = models.TextField(null=True, blank=True)
    next_action_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'opportunity_activities'

    def __str__(self):
        return f"{self.activity_type} for {self.sale}"


# ──────────────────────────────────────────────
#  PIPELINE HISTORY
# ──────────────────────────────────────────────
class PipelineHistory(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    sale = models.ForeignKey(
        SchoolSale, on_delete=models.CASCADE, db_column='pipeline_id', related_name='pipeline_history',
    )
    old_stage = models.CharField(max_length=50, null=True, blank=True)
    new_stage = models.CharField(max_length=50)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='changed_by', related_name='pipeline_changes',
    )
    changed_at = models.DateTimeField(auto_now_add=True, db_column='changed_at')
    notes = models.TextField(null=True, blank=True)

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'pipeline_history'
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.old_stage or 'New'} → {self.new_stage}"


# ──────────────────────────────────────────────
#  PROFILE
# ──────────────────────────────────────────────
class Profile(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='profile',
    )
    display_name = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.TextField(null=True, blank=True, db_column='avatar_url')
    bio = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return self.display_name or self.user.email


# ──────────────────────────────────────────────
#  AUDIT EVENT
# ──────────────────────────────────────────────
class AuditEvent(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='actor_id', related_name='audit_events',
    )
    action = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=255)
    region = models.CharField(max_length=100, null=True, blank=True)
    before_data = JSONField(null=True, blank=True, db_column='before_data')
    after_data = JSONField(null=True, blank=True, db_column='after_data')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} on {self.entity_type}"


# ──────────────────────────────────────────────
#  SUPERVISOR ALERT
# ──────────────────────────────────────────────
class SupervisorAlert(models.Model):
    SEVERITY_CHOICES = [
        ('red', 'Red'),
        ('amber', 'Amber'),
        ('green', 'Green'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('acked', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='supervisor_alerts',
    )
    region = models.CharField(max_length=100, null=True, blank=True)
    alert_type = models.CharField(max_length=100, db_column='alert_type')
    severity = models.CharField(max_length=50, default='amber', choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=50, default='open', choices=STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
    acked_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    ack_sla_met = models.BooleanField(default=False, db_column='ack_sla_met')
    resolve_sla_met = models.BooleanField(default=False, db_column='resolve_sla_met')
    escalated_to_admin = models.BooleanField(default=False, db_column='escalated_to_admin')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'supervisor_alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alert_type} for {self.user.email}"


# ──────────────────────────────────────────────
#  SUPERVISOR INCIDENT
# ──────────────────────────────────────────────
class SupervisorIncident(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='supervisor_incidents',
    )
    region = models.CharField(max_length=100, null=True, blank=True)
    incident_type = models.CharField(max_length=100, db_column='incident_type')
    severity = models.CharField(max_length=50, default='high', choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=50, default='open', choices=STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_incidents',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'supervisor_incidents'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.incident_type} for {self.user.email}"


# ──────────────────────────────────────────────
#  SUPERVISOR NOTE
# ──────────────────────────────────────────────
class SupervisorNote(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    supervisor = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='supervisor_id', related_name='supervisor_notes',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='user_id', related_name='received_notes',
    )
    region = models.CharField(max_length=100, null=True, blank=True)
    context_type = models.CharField(max_length=100, null=True, blank=True)
    context_id = models.CharField(max_length=36, null=True, blank=True)
    note = models.TextField()
    follow_up_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'supervisor_notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Note on {self.user.email}"


# ──────────────────────────────────────────────
#  SUPERVISOR NOTIFICATION
# ──────────────────────────────────────────────
class SupervisorNotification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    supervisor = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='supervisor_id', related_name='supervisor_notifications',
    )
    region = models.CharField(max_length=100, null=True, blank=True)
    notification_type = models.CharField(max_length=100, db_column='notification_type')
    title = models.CharField(max_length=255)
    body = models.TextField()
    payload = models.TextField(null=True, blank=True)
    scheduled_for = models.DateTimeField(auto_now_add=True, db_column='scheduled_for')
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'supervisor_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  ROUTE PLAN
# ──────────────────────────────────────────────
class RoutePlan(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    title = models.CharField(max_length=255)
    route_date = models.DateField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='assigned_to', related_name='route_plans',
    )
    school_ids = JSONField(null=True, blank=True, db_column='school_ids')
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='assigned')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_route_plans',
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='reviewed_by', related_name='reviewed_route_plans',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_note = models.TextField(null=True, blank=True, db_column='review_note')
    is_synced = models.BooleanField(default=False, db_column='isSynced')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'route_plans'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  SAMPLE REQUEST
# ──────────────────────────────────────────────
class SampleRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    ]
    CLIENT_TYPE_CHOICES = [
        ('school', 'School'),
        ('agent', 'Agent'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    request_code = models.CharField(max_length=255, unique=True, null=True, blank=True, db_column='request_code')
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='sample_requests',
    )
    client_type = models.CharField(max_length=50, choices=CLIENT_TYPE_CHOICES, null=True, blank=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='requested_by', related_name='requested_samples',
    )
    purpose = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='PENDING', choices=STATUS_CHOICES)
    rejection_reason = models.TextField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='reviewed_by', related_name='approved_samples',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    needed_by = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True, db_column='requested_at')
    items = JSONField(null=True, blank=True, db_column='items')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'sample_requests'
        ordering = ['-request_code']

    def __str__(self):
        return self.request_code or f"Sample request #{self.id}"


# ──────────────────────────────────────────────
#  VISITATION
# ──────────────────────────────────────────────
class Visitation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, db_column='school_id', related_name='visitations',
    )
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='agent_id', related_name='visitations',
    )
    visit_type = models.CharField(max_length=100, null=True, blank=True, db_column='visit_type')
    outcome = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True, db_column='visited_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'visitations'

    def __str__(self):
        return f"Visitation to {self.school.name}"


# ──────────────────────────────────────────────
#  PROJECT FORM
# ──────────────────────────────────────────────
class ProjectForm(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    fields = JSONField(null=True, blank=True, db_column='fields')
    is_active = models.BooleanField(default=True, db_column='is_active')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='created_by', related_name='created_project_forms',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'project_forms'

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
#  PROJECT FORM RESPONSE
# ──────────────────────────────────────────────
class ProjectFormResponse(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_column='tenant_id')
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False)
    form = models.ForeignKey(
        ProjectForm, on_delete=models.CASCADE, db_column='form_id', related_name='responses',
    )
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='submitted_by', related_name='submitted_forms',
    )
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='school_id', related_name='form_responses',
    )
    responses = JSONField(null=True, blank=True, db_column='responses')
    submitted_at = models.DateTimeField(auto_now_add=True, db_column='submitted_at')

    objects = TenantAwareManager()
    admin = models.Manager()

    class Meta:
        db_table = 'project_form_responses'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Response to {self.form.title}"
