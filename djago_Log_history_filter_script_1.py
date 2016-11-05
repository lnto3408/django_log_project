#-*- coding: utf-8 -*-
import os
import re
import sys
import gzip
import tarfile

#log file open
def log_read(filter_regex,DirPath):
	w_file = open(DirPath+r"/result.html",'a')


	SFU_Fast_recovery = ".*(Fast\sRecovery\sSFU|fail\sto\scheck\sSFU|SFU\sState\sgoes\sto\sBAD\sin|SFU\sState\sgoes\sto\sBAD\sin|fail\sto\scheck\sSFU|Fast\sRecovery\sSFU|Reset\sSFU|ixgbe:\sixg1:\sixgbe_watchdog_link_is_down:\sNIC\sLink\sis\sDown|ixgbe:\sixg1:\sixgbe_watchdog_link_is_down:\sNIC\sLink\sis\sUp|ixgbe_watchdog_link_is_up:\sNIC\sLink\sis\sUp|ixgbe_watchdog_link_is_up:\sNIC\sLink\sis\sDown|ixgbe_spoof_check:\s-1\sSpoofed\spackets\sdetected|AER:\sCorrected\serror\sreceived|PCIe\sBus\sError:\sseverity=Corrected|pcieport|warn_slowpath_common|transmit\squeue\s3\stimed\sout|Hardware\sname:\sX9SCL|Event\salarm\sgenerate).*"
	VRRP_sigsegv = ".*(segfault\sat).*"
	RCU_stall = ".*(RCU\sdetected|tick_periodic|tick_handle_periodic|smp_apic_timer_interrupt|apic_timer_interrupt|delay_tsc|const_udelay|deadlock_timer|run_timer_softirq|do_softirq|swapper\sNot\stainted|restore\saeu).*"
	MGMT_cpuhigh = ".*(management_cpu_usage\sis\s).*"
		# failover_history = ".*(Be\sto\sstart\sipv4\sfailover\sdaemon\snow|Failover\sstatus\sis\sgoing\sinto|Master\sdown\stimer\sexpired|Going\sto\sready\swork\sfor|Switching\sto\smaster\smode\sis\sprogressing|Switching\sto\smaster|backup\smode\shas\scompleted).*"
	failover_history = ".*(had4).*"
	snmpd_descriptor = ".*(no\sifindex\sfound\sfor\sinterface|could\snot\sopen\snetlink\ssocket|Failed\sto\sopen\s/proc/net/dev_snmp6/).*"
	hardware_system =".*(ixgbe_msix_lsc:|ixgbe_clean_tx_irq).*"
	reboot_reason = ".*(reboot\sreason).*"


	#extract all
	if os.path.exists(DirPath+r"/var/lib/tftpboot/sfu_log.tar"):
		tarfile.open(DirPath+r"/var/lib/tftpboot/sfu_log.tar").extractall(path=DirPath+r"/var/lib/tftpboot/")

	#elif os.path.exists(DirPath+r"/var/lib/tftpboot/sfu_backup.tar"):
	#	os.system('sudo mkdir 'DirPath+r"/var/lib/tftpboot/sfu_backup") 
	#	tarfile.open(DirPath+r"/var/lib/tftpboot/sfu_backup.tar").extractall(path=DirPath+r"/var/lib/tftpboot/sfu_backup/")

	else:
		pass 

		
		# filter_list = [SFU_Fast_recovery,VRRP_sigsegv,RCU_stall,MGMT_cpuhigh,failover_history,snmpd_descriptor]

		# for a in filter_list:
		# 	if filter_regex == a:
		# 		w_file.write("################## %s ##################\n"%



	if filter_regex == SFU_Fast_recovery:
		w_file.write("<a href=\"http://192.168.201.144/issues/25556\"><h3>################## SFU Fast Recovery # http://redmine.piolink.com/issues/25556 ##################</a></h3><br>\n")
	elif filter_regex == VRRP_sigsegv:
		w_file.write("<a href=\"http://192.168.201.144/issues/30953\"><h3>################## VRRP_sigsegv      # http://redmine.piolink.com/issues/30953 ##################</a></h3><br>\n")
	elif filter_regex == RCU_stall:
			w_file.write("<a href=\"http://192.168.201.144/issues/15721\"><h3>################## RCU_stall         # http://redmine.piolink.com/issues/15721 ##################</a></h3><br>\n")
	elif filter_regex == MGMT_cpuhigh:	
			w_file.write("<h3>################## MGMT_cpu          ##################</h3><br>\n")
	elif filter_regex == failover_history:	
			w_file.write("<h3>################## failover          ##################</h3><br>\n")			
	elif filter_regex == snmpd_descriptor:	
			w_file.write("<a href=\"http://192.168.201.144/issues/28933\"><h3>################## snmpd_descriptor  # http://redmine.piolink.com/issues/28933 ##################</a></h3><br>\n")			
	elif filter_regex == hardware_system:
			w_file.write("<a href=\"http://192.168.201.144/issues/25553\"><h3>################## hardware_system  # http://redmine.piolink.com/issues/25553 ##################</a></h3><br>\n")			

	elif filter_regex == reboot_reason:
			w_file.write("<h3>################## Reboot Reason     ##################</h3><br>\n")			

	Syslog_path_gz = DirPath+r"/opt/k2/var/log/syslog.gz"
	Syslog_path = DirPath+r"/opt/k2/var/log/syslog"
	SFU_path_gz = DirPath+r"/opt/k2/var/log/k2/sfu.log.gz"
	SFU_path = DirPath+r"/opt/k2/var/log/k2/sfu.log"		
	Netconfd_path_gz = DirPath+r"/opt/k2/var/log/k2/amss.netconfd.log.gz"
	Netconfd_path = DirPath+r"/opt/k2/var/log/k2/amss.netconfd.log"
	Amss_log_path_gz = DirPath+r"/opt/k2/var/log/k2/amss.log.gz"	
	Amss_log_path = DirPath+r"/opt/k2/var/log/k2/amss.log"
	Keepsfu_path_gz = DirPath+r"/opt/k2/var/log/k2/amss.keepsfu.log.gz"	
	Keepsfu_path = DirPath+r"/opt/k2/var/log/k2/amss.keepsfu.log"
	Socat_log_path_gz = DirPath+r"/var/lib/tftpboot/socat_log.gz"
	Socat_log_path = DirPath+r"/var/lib/tftpboot/socat_log"
	Tftpboot_message_path_gz = DirPath+r"/var/lib/tftpboot/messages_all.gz"
	Tftpboot_message_path = DirPath+r"/var/lib/tftpboot/messages_all"

	path_list = [Syslog_path_gz,Syslog_path,SFU_path_gz,SFU_path,Netconfd_path_gz,Netconfd_path,Amss_log_path_gz,Amss_log_path,Keepsfu_path_gz,Keepsfu_path,Socat_log_path_gz,Socat_log_path,Tftpboot_message_path_gz,Tftpboot_message_path,hardware_system]


	for path_a in path_list:
		if os.path.exists(path_a):
			if path_a.endswith(".gz"):

				w_file.write("<font-size=\"3\">************** %s **************</font><br>\n"%path_a[29:])
				log_read = gzip.open(path_a,'r')
				result_read = log_read.readlines()

				
				for i in result_read:  				 #read a per line from the log file
					compile_bug = re.compile(filter_regex)
					match_line = compile_bug.match(i)

					if match_line:
						w_file.write("<font size=\"2\">"+i+"</font><br>")
					else:
						pass
				w_file.write("<br>\n")


			else:
				w_file.write("<font size=\"3\">************** %s **************</font><br>\n"%path_a[29:])
				log_read = open(path_a,'r')
				result_read = log_read.readlines()
				for i in result_read:  				 #read a per line from the log file
					compile_bug = re.compile(filter_regex)
					match_line = compile_bug.match(i)
					if match_line:
						w_file.write("<font size=\"2\">"+i+"</font><br>")
					else:
						pass
				w_file.write("<br>\n")

		else:
			# w_file.write("No such file or directory : %s \n" %path_a)
			pass 


		# 
		# if os.path.exists(w_file):
		# arrange_result = open(os.path.abspath(w_file),'r')
		# last_result = []
		# arrange_result_read = arrange_result.readlines()
		# for i in arrange_result_read:
		# 	last_result.append(i)
			
		# 	# w_file_2.wirte(i)
		# print(last_result)

		
