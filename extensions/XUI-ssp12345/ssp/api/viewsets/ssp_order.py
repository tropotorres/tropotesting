from django.db.models import Q
from orders.api.v3.viewsets import OrderViewSet
from orders.models import Order


class SspOrderViewSet(OrderViewSet):
    # Override the get_queryset method in OrderViewSet
    # because it has some undesirable behavior for the ssp, and also
    # breaks some of the filtering/ordering functionality we want.
    def get_queryset(self):
        profile = self.request.user.userprofile
        qs = Order.objects.all()
        if not profile.super_admin:
            viewable_groups = profile.get_groups_for_permission("order.view")
            qs = qs.filter(Q(owner=profile) | Q(group__in=viewable_groups))

        # TODO add  these changes back to the OrderViewSet in CB
        # Possibly remove this ssp-specific version.
        # https://cloudbolt.atlassian.net/browse/ENG-24050
        qs = self.filter_queryset(qs)
        qs = self.order_queryset(qs)
        qs = self.select_related_queryset(qs)

        return qs
