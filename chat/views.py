from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Room, Message
from django.utils import timezone
import uuid
# Create your views here.
from django.shortcuts import render, redirect
from .models import Room, Message
import uuid 
from django.utils.crypto import get_random_string

def home(request):
    # Implement logic to display the homepage with two buttons: Create Room and Enter Room

    
    return render(request, 'home.html')

# views.py



def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '') or f"Test Room{get_random_string(8).upper()}"
        room_id = request.POST.get('room_id', '').upper()
        description = request.POST.get('description', '')
        time_limit_hours = int(request.POST.get('time_limit', 1))
        time_limit = timezone.timedelta(hours=time_limit_hours)
        passkey = request.POST.get('passkey', '')

        # If room_id is blank, return an error message
        if not room_id:
            error_message = "Room ID is required."
            return render(request, 'create_room.html', {'error_message': error_message})

        # If room with the same room_id already exists, return an error message
        if Room.objects.filter(room_id=room_id).exists():
            error_message = "A room with the same Room ID already exists."
            return render(request, 'create_room.html', {'error_message': error_message})

        # Create the room with the provided details and unique room_id
        new_room = Room.objects.create(room_id=room_id, room_name=room_name, description=description, time_limit=time_limit, passkey=passkey)

        # Redirect the user to the chat interface for the newly created room
        return redirect('room_interface', room_id=new_room.id)

    # If it's a GET request or form submission failed, render the create room form
    return render(request, 'create_room.html')




def enter_room(request):
    # Implement logic to handle entering an existing room and redirect to the room interface
    room_id = 1
    return redirect('room_interface', room_id=room_id)

# def room_interface(request, room_id):
#     room = Room.objects.get(id=room_id)
    
#     if request.method == 'POST':
#         sender = 'User'  # You can customize this to get the sender's name from the user if needed
#         content = request.POST.get('message', '')
#         message = Message.objects.create(room=room, sender=sender, content=content)

#     messages = Message.objects.filter(room=room)

#     return render(request, 'room.html', {'room_id': room.room_name, 'messages': messages})
#     # Implement logic to display the chat interface for the specified room with chat history
#     # and handle sending chat messages using WebSocket
#     # return render(request, 'room.html', {'room_id': room_id})

def room_interface(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        sender = 'User'  # You can customize this to get the sender's name from the user if needed
        content = request.POST.get('message', '').upper()  # Convert the message content to uppercase
        message = Message.objects.create(room=room, sender=sender, content=content)

    messages = Message.objects.filter(room=room)

    # Create a dictionary that maps each message ID to its content
    message_data = {f"message{message.id}": message.content for message in messages}

    return render(request, 'room.html', {'room_id': room.room_name, 'messages': messages, 'message_data': message_data})
def enter_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id', '')
        passkey = request.POST.get('passkey', '')

        try:
            room = Room.objects.get(room_id=room_id)
            if room.passkey == passkey:
                return redirect('room_interface', room_id=room.id)
            else:
                error_message = "Room credentials not found. Please check the Room ID and Passkey."
                return render(request, 'enter_room.html', {'error_message': error_message})
        except Room.DoesNotExist:
            error_message = "Room credentials not found. Please check the Room ID and Passkey."
            return render(request, 'enter_room.html', {'error_message': error_message})

    # If it's a GET request or form submission failed, render the enter room form
    return render(request, 'enter_room.html')

def exit_room(request, room_id):
    # Implement logic to exit the room and redirect back to the homepage
    return redirect('home')