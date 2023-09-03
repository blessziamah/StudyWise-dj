from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pydub import AudioSegment

import logging
from .main import transcribe_audio_variable, clean_up, summarize


# Create your views here.
def home(request):
	return render(request, 'soundwise/homepage.html')


def login_user(request):
	page = "login"
	if request.user.is_authenticated:
		return redirect("home")

	if request.method == "POST":
		username = request.POST.get("username").lower()
		password = request.POST.get("password")

		try:
			user = User.objects.get("username=username")
		except:
			messages.error(request, "User does not exist")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			return redirect('home')
		else:
			messages.info(request, "Username or password does not exist")

	return render(request, "soundwise/login-page.html", {"page": page})


def logout_user(request):
	logout(request)
	return redirect("home")


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			# load the profile instance created by the signal
			user.save()
			raw_password = form.cleaned_data.get('password1')

			# login user after signing up
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)

			# redirect user to home page
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'soundwise/sign-up-page.html', {'form': form})


def changePassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password was successfully updated!')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'soundwise/password_change.html', {'form': form})


def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audioFile'):
        audio_file = request.FILES['audioFile']
        # Process the uploaded audio file as needed (e.g., save it to a specific directory, analyze it, etc.).
        # You can access the audio file using audio_file.read(), audio_file.name, etc.

        # Return a JSON response to the frontend.
        return JsonResponse({'message': 'Audio file uploaded successfully'})
    else:
        return JsonResponse({'message': 'Audio file upload failed'}, status=400)



# Audio processing and API calls
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

@csrf_exempt
@require_POST
def process_audio(request):
	logger = logging.getLogger(__name__)  # Create a logger instance

	try:
		# Get the uploaded audio file from the request
		audio_file = request.FILES.get('audioFile')

		if audio_file:
			logger.info('Audio processing started')

			# Load the audio file
			test_audio = AudioSegment.from_file(audio_file)

			# Convert it to WAV format
			audio_data = test_audio.export(format="wav")

			# Perform audio transcription directly on the uploaded audio file
			transcribed_text = transcribe_audio_variable(audio_data)

			# Clean up the transcribed text
			corrected_text = clean_up(transcribed_text)

			should_summarize = request.POST.get('summarize', '0') == '1'

			# Initialize summary
			summary = ""

			if should_summarize:
				logger.info('Return summary')
				summary = summarize(corrected_text)
			else:
				logger.info('Summarization is not enabled.')

			# Log a message indicating successful processing
			logger.info('Audio processing successful')

			# Return the results as JSON
			response_data = {
				"transcribed_text": transcribed_text,
				"corrected_text": corrected_text,
				"summary": summary,
			}

			return JsonResponse(response_data)
		else:
			# Log an error if no audio file was provided
			logger.error('No audio file provided in the request')
			return JsonResponse({"error": "No audio file provided."}, status=400)
	except Exception as e:
		# Log the error message and return an error response
		logger.error(f'Error during audio processing: {str(e)}')
		return JsonResponse({"error": str(e)}, status=500)


def account_page(request):
	return render(request, 'soundwise/account.html')


