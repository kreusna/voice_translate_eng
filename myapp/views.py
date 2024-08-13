from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import UploadSerializer
# Create your views here.

import torchaudio
from transformers import AutoProcessor, SeamlessM4Tv2Model


processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

def index(request):
    return render(request, 'showAudio.html')


class TodoListApiView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
            '''
            List all the todo items for given requested user
            '''
            serializer = [1, 2, 3]
            return Response(serializer, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = [1, 2, 3]
        return Response(serializer, status=status.HTTP_200_OK)

class UploadViewSet(APIView):
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs):
        file_uploaded = request.FILES.get('file')
        getContent = file_uploaded.read()
        # content_type = file_uploaded.content_type
        with open('file.mp3', 'wb') as f_vid:
            f_vid.write(getContent)
        

        audio, orig_freq = torchaudio.load("file.mp3", format="mp3")
        audio = torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000) # must be a 16 kHz waveform array
        audio_inputs = processor(audios=audio, return_tensors="pt")
        audio_array_from_audio = model.generate(**audio_inputs, tgt_lang="eng")[0].cpu()
        torchaudio.save(
            "myapp/static/test.mp3",
            audio_array_from_audio,  # or audio_array_from_text
            sample_rate=model.config.sampling_rate,
            format='mp3',
        )
        
        return FileResponse(audio,filename="Sample.mp3",as_attachment=True)
    

