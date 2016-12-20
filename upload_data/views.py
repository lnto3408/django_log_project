#-*- coding:utf-8 -*-
import tarfile
import gzip
import os
import time
import commands
from subprocess import call

from .djago_Log_history_filter_script_2 import log_read
from django.http import HttpResponse

from django.shortcuts import render
from django.template import RequestContext
from .models import Document
from .forms import DocumentForm,UploadFileForm
from django.core.urlresolvers import reverse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.


def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		filename = filename.encode('utf-8')
		uploaded_file_url = fs.url(filename)
		ExtractPath = Extract(filename)
		ExtractPath =  ExtractPath.encode('utf-8')
		#print "ExtractPath : "+ ExtractPath 

		log_read(".*(Fast\sRecovery\sSFU|fail\sto\scheck\sSFU|SFU\sState\sgoes\sto\sBAD\sin|SFU\sState\sgoes\sto\sBAD\sin|fail\sto\scheck\sSFU|Fast\sRecovery\sSFU|Reset\sSFU|ixgbe:\sixg1:\sixgbe_watchdog_link_is_down:\sNIC\sLink\sis\sDown|ixgbe:\sixg1:\sixgbe_watchdog_link_is_down:\sNIC\sLink\sis\sUp|ixgbe_watchdog_link_is_up:\sNIC\sLink\sis\sUp|ixgbe_watchdog_link_is_up:\sNIC\sLink\sis\sDown|ixgbe_spoof_check:\s-1\sSpoofed\spackets\sdetected|AER:\sCorrected\serror\sreceived|PCIe\sBus\sError:\sseverity=Corrected|pcieport|warn_slowpath_common|transmit\squeue\s3\stimed\sout|Hardware\sname:\sX9SCL|Event\salarm\sgenerate).*",ExtractPath)
		log_read(".*(segfault\sat).*",ExtractPath)
		log_read(".*(RCU\sdetected|tick_periodic|tick_handle_periodic|smp_apic_timer_interrupt|apic_timer_interrupt|delay_tsc|const_udelay|deadlock_timer|run_timer_softirq|do_softirq|swapper\sNot\stainted|restore\saeu).*",ExtractPath)
		log_read(".*(management_cpu_usage\sis\s).*",ExtractPath)
		log_read(".*(had4).*",ExtractPath)
		log_read(".*(no\sifindex\sfound\sfor\sinterface|could\snot\sopen\snetlink\ssocket|Failed\sto\sopen\s/proc/net/dev_snmp6/).*",ExtractPath)
		log_read(".*(ixgbe_msix_lsc:|ixgbe_clean_tx_irq).*",ExtractPath)
		log_read(".*(reboot\sreason).*",ExtractPath)


		GetResult = open(ExtractPath+'/result.html','r')
		ReadResult = GetResult.readlines()

		os.system('rm -r '+ExtractPath)
		return render(request,'simple_upload.html', {
			'ReadResult': ReadResult
			})


#		return render(request, ExtractPath+'/result.html')

		#return render(request, 'simple_upload.html', {
		#	'uploaded_file_url': uploaded_file_url
		#	})
	return render(request, 'simple_upload.html')


def Extract(GetName):
	a = time.localtime()
	FolderName = "%d%d%d_%d%d%d" % (a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min,a.tm_sec)
	#Media_path = "/home/hyosung/tech/media_cdn"
	Media_path = FileSystemStorage()
	FileName = Media_path.path(GetName)
	
	if os.path.exists(FileName):
		#gzzip File
		if FileName.endswith('gz'):
			FileName = FileName.encode('utf-8')
			unzip = commands.getstatusoutput('gunzip '+FileName)

			print FileName[0:-3]
			print FileName[0:-3]

			if tarfile.is_tarfile(FileName[0:-3]):
				FileRead = tarfile.TarFile(FileName[0:-3],'r')

				get_namelist = FileName[0:-3].split('/')
				get_fileName = Media_path.path(get_namelist[-1]+'_'+FolderName)
				
				
				os.makedirs(get_fileName)
				Extract_Path=get_fileName 
				FileRead.extractall(Extract_Path)
				commands.getstatusoutput('sudo rm -r \"'+FileName[0:-3]+"\"")

				return Extract_Path 

		#tarfile
		elif tarfile.is_tarfile(FileName):
			#pio File
			if FileName.endswith('pio'):
				os.renames(FileName,FileName+'.gz')
				print type(FileName)
				FileName = FileName.encode('utf-8')
				unzip = commands.getstatusoutput('sudo gunzip \"'+FileName+'.gz\"')
				print unzip

				if unzip[0] > 0:
					os.renames(FileName+'.gz',FileName)

				#if tarfile.is_tarfile(FileName):
					FileRead = tarfile.TarFile(FileName,'r')
					#print "File Read : %s"%(FileRead)

					get_namelist = FileName.split('/')
					get_fileName = Media_path.path(get_namelist[-1]+'_'+FolderName)
			
					os.makedirs(get_fileName)
					Extract_Path=get_fileName 
					FileRead.extractall(Extract_Path)
					commands.getstatusoutput('sudo rm -r \"'+FileName+"\"")

					return Extract_Path 
				else:
					print "#### ELSE ####"

					FileRead = tarfile.TarFile(FileName,'r')

					get_namelist = FileName.split('/')
					get_fileName = Media_path.path(get_namelist[-1]+'_'+FolderName)
					os.makedirs(get_fileName)
					
					Extract_Path=get_fileName 
					FileRead.extractall(Extract_Path)
					commands.getstatusoutput('sudo rm -r \"'+FileName[0:-3]+"\"")

					return Extract_Path 

			#tar_file
			else :
				FileRead = tarfile.TarFile(FileName,'r')

				get_namelist = FileName.split('/')
				get_fileName = Media_path.path(get_namelist[-1]+'_'+FolderName)
			
			
				os.makedirs(get_fileName)
				Extract_Path=get_fileName 

				FileRead.extractall(Extract_Path)

				commands.getstatusoutput('sudo rm -r \"'+FileName+'\"')      #delete File
				return Extract_Path 


		

def Log_Filter(DirPath):
	Log_filter_exe = "/home/hyosung/tech/media_cdn/Log_history_filter_script_5.py"

	if os.path.exists(DirPath): 
		commands.getstatusoutput('cp \"'+Log_filter_exe+'\" \"'+DirPath+'\"')
		#commands.getstatusoutput('sudo python \"'+DirPath+'/Log_history_filter_script_5.py\"') 
		os.system('sudo python \"'+DirPath+'/Log_history_filter_script_5.py\"')
		os.system('sudo python \"'+DirPath+'/Log_history_filter_script_5.py\"')

'''
# origin code
def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return render(request, 'simple_upload.html', {
			'uploaded_file_url': uploaded_file_url
			})
	return render(request, 'simple_upload.html')
'''
