from datatables.api.v3.viewsets.data_table_type import DataTableTypeViewSet
from xui.ssp.api.serializers import SspDataTableTypeSerializer


class SspDataTableTypeViewSet(DataTableTypeViewSet):
    serializer_class = SspDataTableTypeSerializer
