from datatables.api.v3.serializers import DataTableTypeSerializer
from datatables.services import ResourceStructuredColumnsService
from infrastructure.models import CustomField


class SspDataTableTypeSerializer(DataTableTypeSerializer):
    def resource_dict(self, obj):
        resource_dict = super().resource_dict(obj)

        if obj.data_model == "resources.models.ResourceStructured":
            column_service = ResourceStructuredColumnsService()
            column_service.include_show_on_server_cfs = True

            server_cfs = column_service.get_server_custom_fields()
            server_cf_columns = [c["name"] for c in server_cfs.values("name")]
            server_predef_columns = [
                c["name"] for c in column_service.server_predefined_columns
            ]
            server_columns_without_filters = [
                "server",
                "disk_storage",
                "disk_type",
                "rate",
                "power_schedule",
            ]

            resource_cfs = CustomField.user_parameters.all()
            resource_cf_columns = [c["name"] for c in resource_cfs.values("name")]
            resource_predef_columns = [
                c["name"] for c in column_service.resource_predefined_columns
            ]
            resource_columns_without_filters = [
                "rate",
                "attributes",
                "servers",
            ]

            columns = obj.available_columns

            for col in columns:
                col_name = col["name"]
                col["sortable"] = True
                server_filter = None
                resource_filter = None

                if (
                    col_name not in server_predef_columns
                    and col_name not in resource_predef_columns
                    and col_name not in resource_columns_without_filters
                    and col_name not in server_columns_without_filters
                ):
                    if col_name in server_cf_columns:
                        col["sortable"] = False  # Custom fields not sortable
                        server_filter = f"server.{col_name}"
                    if col_name in resource_cf_columns:
                        col["sortable"] = False  # Custom fields not sortable
                        resource_filter = f"resource.{col_name}"

                    col["filters"] = {
                        "server": server_filter,
                        "resource": resource_filter,
                    }

                else:
                    if (
                        col_name in resource_predef_columns
                        and col_name not in resource_columns_without_filters
                    ):
                        resource_filter = f"resource.{col_name}"

                        if col_name == "group":
                            resource_filter = "resource.group"
                        if col_name == "owner":
                            resource_filter = "resource.owner"
                        if col_name == "resource_type":
                            resource_filter = "resource.resource_type"
                        if col_name == "blueprint":
                            resource_filter = "resource.blueprint"
                        if col_name == "status":
                            resource_filter = "resource.lifecycle"

                    if (
                        col_name in server_predef_columns
                        and col_name not in server_columns_without_filters
                    ):
                        server_filter = f"server.{col_name}"

                        if col_name == "added":
                            server_filter = "server.add_date"
                        if col_name == "resource_handler":
                            server_filter = "server.resource_handler"
                        if col_name == "environment":
                            server_filter = "server.environment"
                        if col_name == "family":
                            server_filter = "server.os_family.name"
                        if col_name == "os_build":
                            server_filter = "server.os_build"
                        if col_name == "group":
                            server_filter = "server.group"
                        if col_name == "owner":
                            server_filter = "server.owner"
                        if col_name == "power":
                            server_filter = "server.power_status"
                        if col_name == "resource_tier":
                            server_filter = "server.service_item.name"
                        if col_name == "storage":
                            server_filter = "server.disk_size"
                        if col_name == "tags":
                            server_filter = "server__tags"
                        if col_name == "unique_id":
                            server_filter = "server.resource_handler_svr_id"
                        if col_name == "status":
                            server_filter = "server.status"
                        if col_name == "cpus":
                            server_filter = "server.cpu_cnt"
                        if col_name == "disk":
                            server_filter = "server.disk_size"
                        if col_name == "memory":
                            server_filter = "server.mem_size"

                col["filters"] = {
                    "server": server_filter,
                    "resource": resource_filter,
                }

            resource_dict["available_columns"] = columns

        return resource_dict
