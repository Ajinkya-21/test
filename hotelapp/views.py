from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.db.models import Q
from datetime import datetime
from .models import Customer, Room, Room_check, Customer_log

# ---------------------- INDEX VIEW ----------------------
class IndexClass(View):
    def get(self, request):
        return render(request, 'hotelapp/index.html')


# ---------------------- ADMIN LOGIN ----------------------
class AdminLoginView(View):
    def get(self, request):
        return render(request, 'hotelapp/admin_login.html')
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('admin_dashboard')
        else:
            return render(request, 'hotelapp/admin_login.html', {'error': 'Invalid credentials'})


# ---------------------- ADMIN DASHBOARD ----------------------
class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'hotelapp/admin_dashboard.html')


# ---------------------- RECEPTION DASHBOARD ----------------------
class RecpDashboardView(View):
    def get(self, request):
        return render(request, 'hotelapp/recp_dashboard.html')


# ---------------------- ADD CUSTOMER ----------------------
class AddCustomerView(View):
    def get(self, request):
        rooms = Room.objects.filter(available=True)
        return render(request, 'hotelapp/add_customer.html', {'rooms': rooms})

    def post(self, request):
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        room_id = request.POST.get('room')
        room = Room.objects.get(id=room_id)
        customer = Customer.objects.create(name=name, contact=contact)
        Room_check.objects.create(cust=customer, room=room, check_in=timezone.now())
        room.available = False
        room.save()
        Customer_log.objects.create(cust_id=customer.id, name=customer.name, action='Added')
        return redirect('manage_customer')


# ---------------------- MANAGE CUSTOMER ----------------------
class ManageCustomerView(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'hotelapp/manage_customer.html', {'customers': customers})


# ---------------------- UPDATE CUSTOMER ----------------------
class UpdateCustomerView(View):
    def get(self, request, id):
        cust = get_object_or_404(Customer, id=id)
        return render(request, 'hotelapp/update_customer.html', {'cust': cust})

    def post(self, request, id):
        cust = get_object_or_404(Customer, id=id)
        cust.name = request.POST.get('name')
        cust.contact = request.POST.get('contact')
        cust.save()
        Customer_log.objects.create(cust_id=cust.id, name=cust.name, action='Updated')
        return redirect('manage_customer')


# ---------------------- DELETE CUSTOMER ----------------------
class DeleteCustomerView(View):
    def get(self, request, id):
        cust = get_object_or_404(Customer, id=id)
        rooms = Room_check.objects.filter(cust_id=id)
        if rooms.exists():
            for r in rooms:
                room = Room.objects.get(room_number=r.room.room_number)
                room.available = True
                room.save()
            rooms.delete()
        Customer_log.objects.create(cust_id=cust.id, name=cust.name, action='Deleted')
        cust.delete()
        return redirect('manage_customer')


# ---------------------- ROOM MANAGEMENT ----------------------
class RoomManagementView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'hotelapp/room_management.html', {'rooms': rooms})


# ---------------------- ADD ROOM ----------------------
class AddRoomView(View):
    def get(self, request):
        return render(request, 'hotelapp/add_room.html')

    def post(self, request):
        room_number = request.POST.get('room_number')
        type = request.POST.get('type')
        price = request.POST.get('price')
        Room.objects.create(room_number=room_number, type=type, price=price, available=True)
        return redirect('room_management')


# ---------------------- UPDATE ROOM ----------------------
class UpdateRoomView(View):
    def get(self, request, room_number):
        room = get_object_or_404(Room, room_number=room_number)
        return render(request, 'hotelapp/update_room.html', {'room': room})

    def post(self, request, room_number):
        room = get_object_or_404(Room, room_number=room_number)
        room.type = request.POST.get('type')
        room.price = request.POST.get('price')
        room.save()
        return redirect('room_management')


# ---------------------- DELETE ROOM ----------------------
class DeleteRoomView(View):
    def get(self, request, room_number):
        room = get_object_or_404(Room, room_number=room_number)
        room.delete()
        return redirect('room_management')


# ---------------------- CHECK CUSTOMER ID ----------------------
class CheckCustIdView(View):
    def get(self, request):
        return render(request, 'hotelapp/check_cust_id.html')

    def post(self, request):
        cust_id = request.POST.get('cust_id')
        try:
            cust = Customer.objects.get(id=cust_id)
            return redirect('checked_in', id=cust.id)
        except Customer.DoesNotExist:
            return render(request, 'hotelapp/check_cust_id.html', {'error': 'Customer not found'})


# ---------------------- CHECKED IN ----------------------
class CheckedInView(View):
    def get(self, request, id):
        cust = get_object_or_404(Customer, id=id)
        return render(request, 'hotelapp/checked_in.html', {'cust': cust})


# ---------------------- CHECK CUSTOMER ID OUT ----------------------
class CheckCustIdOutView(View):
    def get(self, request):
        return render(request, 'hotelapp/check_cust_id_out.html')


# ---------------------- SEARCH CUSTOMER RECEP ----------------------
class SearchCustomerRecpView(View):
    def get(self, request):
        search = request.GET.get('search', '')
        customers = Customer.objects.all()
        room_data = Room_check.objects.all()

        if search:
            customers = customers.filter(
                Q(id__iexact=search) |
                Q(name__icontains=search) |
                Q(contact__icontains=search)
            )

        return render(request, 'hotelapp/search_customer_recp.html', {
            'customers': customers,
            'search': search
        })


# ---------------------- CUSTOMER LIST ----------------------
class CustomerListView(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'hotelapp/customer_list.html', {'customers': customers})


# ---------------------- CUSTOMER MANAGEMENT ADMIN ----------------------
class CustomerManagementAdminView(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'hotelapp/customer_management_admin.html', {'customers': customers})


# ---------------------- GENERATE BILL ----------------------
class GenerateBillView(View):
    def get(self, request, id):
        cust = get_object_or_404(Customer, id=id)
        rooms = Room_check.objects.filter(cust_id=id)

        if not rooms.exists():
            return render(request, 'hotelapp/no_rooms.html', {'cust': cust})

        total_price = sum(room.room.price for room in rooms)
        return render(request, 'hotelapp/generate_bill.html', {
            'cust': cust,
            'rooms': rooms,
            'total_price': total_price
        })
