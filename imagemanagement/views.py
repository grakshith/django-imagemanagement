from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .forms import ImageForm
from .models import Image as img
from .models import AccessKey
from django.conf import settings
import base64,os
from PIL import Image 
from django.core.exceptions import ObjectDoesNotExist
import thread,zstd
import random,string
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
class FileSizeExceededError(Exception):
	def __init__(self,fileSize):
		maxFileSize='25000000 bytes'
		print "The input file exceeded the file size limit. The input file size is {0} The maximum file size is {1}".format(fileSize,maxFileSize)

def upload(request):
	if request.method=='GET':
		if 'accessKey' in request.GET:
			accessKey=request.GET['accessKey']
			access=get_object_or_404(AccessKey,accessKey=accessKey)
		else:
			return HttpResponse("Access Token required",status=401)
		form=ImageForm()
		return render(request,'upload.html',{'form':form})
	elif request.method=='POST':
		form=ImageForm(request.POST,request.FILES)
		if form.is_valid():
			file=form.save(commit=False)
			imagename=str(file.image)
			ext=imagename[imagename.rfind('.')+1:]
			try:
				list = handle_uploaded_file(request.FILES['image'],ext)
				name=list[0]
				url=list[1]
			except FileSizeExceededError:
				return HttpResponse("File Size Exceeded")
			except IndexError:
				pass
			else:
				if name is None:
					url='/media/images/'+url
					return HttpResponse("Image Exists at <a href="+url+">"+url+"</a>")
				else:
					file.name=name
					image_path='/media/images/'+name
					file.image.name=name
					file.save()
					thread.start_new_thread(asyncjob,(name,request,))
					return render(request,'image.html',{'image':image_path,'name':name})
		else:
			return redirect('/image')
	return HttpResponse("Successfully landed")

def handle_uploaded_file(f,ext):
	image=f.read()
	if len(image) > 25000000:
		raise FileSizeExceededError(len(image))
	name=str(hash(base64.b64encode(image)))+'.'+ext
	name=name.replace('-','a')
	try:
		image=img.objects.get(name=name)
	except ObjectDoesNotExist:
		return [name,None]
	else:
		return [None,name]
	#with open(os.path.join(settings.MEDIA_ROOT,'images/'))


def asyncjob(name,request):
	path=os.path.join(settings.MEDIA_ROOT,'images/'+name)
	im=Image.open(path)
	size=os.path.getsize(path)
	format=im.format
	temp_file_name=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))+'.'+format.lower()
	temp_file_path=os.path.join(settings.MEDIA_ROOT,'images/'+temp_file_name)
	try:
		im.save(temp_file_path,optimize=True,quality=80)
	except:
		pass
	new_size=os.path.getsize(temp_file_path)
	if(new_size>size):
		os.system('rm -f '+temp_file_name)
	else:
		command='mv \"'+temp_file_path+'\" \"'+path+'\"'
		print command
		os.system(command)

	model=get_object_or_404(img,name=name)
	model.old_size=size
	model.new_size=new_size
	model.save()
	#return render(request,'image.html',{'old_size':size,'new_size':size,'ratio':old_size/new_size,'reductionpc':(new_size-size)/size*100})


def ajaxView(request,imageid):
	image=get_object_or_404(img,name=imageid)
	old_size=image.old_size
	new_size=image.new_size
	if old_size!=0 and new_size!=0:
		return JsonResponse({'message':{'old_size':old_size,'new_size':new_size}})
	else:
		return JsonResponse({'message':'0'})
@csrf_exempt
def update_or_delete(request,filename):
	filepath=os.path.join(settings.MEDIA_ROOT,'images/'+filename)
	message=json.loads(request.body)
	accessKey=str(message['accessKey'])
	print accessKey
	if accessKey=='':
		return HttpResponse("Access Token required",status=401)
	try:
		access=get_object_or_404(AccessKey,accessKey=accessKey)
	except Exception as e:
		return HttpResponse(str(e),status=400)
	if request.method=='DELETE':
		image=img.objects.get(name=filename)
		image.delete()
		os.system('rm -f '+filepath)
		return JsonResponse({'message':"Success"})
	elif request.method=='PATCH':
		#print request.body
		try:
			image=base64.b64decode(message['image'])
			model=get_object_or_404(img,name=filename)
		except TypeError as e:
			return JsonResponse({'message':str(e)})
		except Exception as e:
			return HttpResponse(str(e),status=404)
		file=open(filepath,'wb')
		file.write(image)
		file.close()
		thread.start_new_thread(asyncjob,(filename,request,))
		return JsonResponse({'message':'Success'})
	else:
		return HttpResponse("Use only PATCH or DELETE methods")

def test(request):
	return render(request,'test.html')
