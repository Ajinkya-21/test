from django.contrib import admin
from django.urls import path
from hotelapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexClass.as_view(), name='index'),
    path('admin_login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('recp_dashboard/', RecpDashboardView.as_view(), name='recp_dashboard'),
    path('add_customer/', AddCustomerView.as_view(), name='add_customer'),
    path('manage_customer/', ManageCustomerView.as_view(), name='manage_customer'),
    path('update_customer/<int:id>/', UpdateCustomerView.as_view(), name='update_customer'),
    path('delete_customer/<int:id>/', DeleteCustomerView.as_view(), name='delete_customer'),
    path('room_management/', RoomManagementView.as_view(), name='room_management'),
    path('add_room/', AddRoomView.as_view(), name='add_room'),
    path('update_room/<int:room_number>/', UpdateRoomView.as_view(), name='update_room'),
    path('delete_room/<int:room_number>/', DeleteRoomView.as_view(), name='delete_room'),
    path('check_cust_id/', CheckCustIdView.as_view(), name='check_cust_id'),
    path('checked_in/<int:id>/', CheckedInView.as_view(), name='checked_in'),
    path('check_cust_id_out/', CheckCustIdOutView.as_view(), name='check_cust_id_out'),
    path('search_customer_recp/', SearchCustomerRecpView.as_view(), name='search_customer_recp'),
    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer_management_admin/', CustomerManagementAdminView.as_view(), name='customer_management_admin'),
    path('generate_bill/<int:id>/', GenerateBillView.as_view(), name='generate_bill'),
]
