#!/alma/ACS-2016.6/Python/bin/python

import CONSOLE_MODULE__POA

import sys
import os
from sys import stdout
import TYPES
from Acspy.Servants.ContainerServices import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
from Acspy.Servants.ACSComponent import ACSComponent
import SYSTEMErr
import SYSTEMErrImpl
from SYSTEMErrImpl import SystemInAutoModeExImpl
from SYSTEMErrImpl import PositionOutOfLimitsExImpl
import Acsalarmpy
import Acsalarmpy.Timestamp as Timestamp
import Acsalarmpy.FaultState as FaultState

class Console2_test(CONSOLE_MODULE__POA.Console, ContainerServices, ComponentLifecycle, ACSComponent):


	def __init__(self):
		ACSComponent.__init__(self)
		ContainerServices.__init__(self)
		self.apertureTime = 500000
		self.elMax = 45.0
		self.azMax = 250.0	
		self.Mode = False  # TRUE = AUTOMATIC FALSE = NO AUTOMATIC\
		
		#alarm
		self.family = "Console2"
		self.member = "ALARM_SOURCE_MOUNT"
		self.code = 1
		self.fltstate = 0
		self.alarmSource = 0
		

	def initialize(self):
		'''
		Override this method inherited from ComponentLifecycle
		'''
		self.getLogger().logInfo("CONSOLE 2 INIT ACCESS")
		self.db = self.getComponent("DATABASE")
		self.scheduler = self.getComponent("SCHEDULER")
		self.instrument = self.getComponent("INSTRUMENT")
		self.telescope = self.getComponent( "TELESCOPE")

		Acsalarmpy.AlarmSystemInterfaceFactory.init()
		self.alarmSource = Acsalarmpy.AlarmSystemInterfaceFactory.createSource("ALARM_SYSTEM_SOURCES")
		self.fltstate=Acsalarmpy.AlarmSystemInterfaceFactory.createFaultState(self.family,self.member, self.code)
		self.fltstate.descriptor = FaultState.ACTIVE_STRING

	def cleanUp(self):
		'''
		Override this method inherited from ComponentLifecycle
		'''

	def setMode(self, *args):
		
		#self.getLogger().logDebug("CONSOLE 2 SET_MODE ACCESS")
		self.Mode = args[0]
		if (self.Mode):
			#self.scheduler.start()
			self.getLogger().logDebug("Atomatic Mode")
    		else:
			#self.scheduler.stop()
			self.getLogger().logDebug("Manual Mode")

		pass
		
	def getMode(self, *args):

		return self.Mode
		
	
	#INSTRUMENT
	def cameraOn(self, *args):
		
		#self.getLogger().logInfo("CONSOLE 2 CAMERA ON METHOD ACCESS")
		if(self.getMode()):

			self.fltstate.userTimestamp = Timestamp.Timestamp()
			self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
			self.alarmSource.push(self.fltstate)
			Acsalarmpy.AlarmSystemInterfaceFactory.done()

			self.getLogger().logError("AUTOMATIC MODE IS ON")

			ex2 = SystemInAutoModeExImpl()
                        ex2.log(self.getLogger())
			raise ex2

		else:
			self.getLogger().logInfo(self.instrument.cameraOn())
			
	
	def cameraOff(self, *args):
		#self.getLogger().logInfo("CONSOLE 2 CAMERA OFF METHOD ACCESS")
		if(self.getMode()):

			self.fltstate.userTimestamp = Timestamp.Timestamp()
			self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
			self.alarmSource.push(self.fltstate)
			Acsalarmpy.AlarmSystemInterfaceFactory.done()
			
			ex2 = SystemInAutoModeExImpl()
                        ex2.log(self.getLogger())
			raise ex2
			
		else:
			self.getLogger().logInfo(self.instrument.cameraOff())
	
	def setPixelBias(self, *args):
		#self.getLogger().logError("CONSOLE 2 SET PIXEL BIAS ACCESS")	
		if(self.getMode()):

			self.fltstate.userTimestamp = Timestamp.Timestamp()
			self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
			self.alarmSource.push(self.fltstate)
			Acsalarmpy.AlarmSystemInterfaceFactory.done()

			self.getLogger().logError("AUTOMATIC MODE IS ON")
			ex2 = SystemInAutoModeExImpl()
                        ex2.log(self.getLogger())
			raise ex2
		else:
			self.getLogger().logInfo(self.instrument.setPixelBias(args[0]))

	def setResetLevel(self, *args):
		#self.getLogger().logInfo("CONSOLE 2 RESET LEVEL ACCESS")	
		if(self.getMode()):

			self.fltstate.userTimestamp = Timestamp.Timestamp()
			self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
			self.alarmSource.push(self.fltstate)
			Acsalarmpy.AlarmSystemInterfaceFactory.done()

			self.getLogger().logError("AUTOMATIC MODE IS ON")
			ex2 = SystemInAutoModeExImpl()
                        ex2.log(self.getLogger())
			raise ex2
		else:
			self.getLogger().logInfo(self.instrument.setResetLevel(args[0]))

	def getCameraImage(self, *args):
		#self.getLogger().logCritical("CONSOLE 2 GET CAMERA IMAGE ACCESS")	
		if(self.getMode()):

			self.fltstate.userTimestamp = Timestamp.Timestamp()
			self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
			self.alarmSource.push(self.fltstate)
			Acsalarmpy.AlarmSystemInterfaceFactory.done()

			self.getLogger().logError("AUTOMATIC MODE IS ON")
			ex2 = SystemInAutoModeExImpl()
                        ex2.log(self.getLogger())
			raise ex2
			return b'error'
		else:			
			#return TYPES.ImageType(self.instrument.takeImage(self.apertureTime))
			return self.instrument.takeImage(self.apertureTime)


	#TELESCOPE
	def moveTelescope(self, *args):
		#self.getLogger().logInfo("CONSOLE 2 MOVE TELESCOPE ACCESS")
		
		if(self.getMode()):
			self.getLogger().logError("AUTOMATIC MODE IS ON")

			
		else:			
			if(args[0].az > self.azMax or args[0].el > self.elMax):
				self.family = "Console2"
				self.member = "ALARM_SOURCE_MOUNT"
				self.code = 2
				self.fltstate = 0
				self.alarmSource = 0
				self.alarmSource = Acsalarmpy.AlarmSystemInterfaceFactory.createSource("ALARM_SYSTEM_SOURCES")
				self.fltstate=Acsalarmpy.AlarmSystemInterfaceFactory.createFaultState(self.family,self.member, self.code)
				self.fltstate.descriptor = FaultState.ACTIVE_STRING

				self.fltstate.userTimestamp = Timestamp.Timestamp()
				self.fltstate.userProperties["TEST_PROPERTY"] = "SYSTEM IN AUTONOMOUS"
				self.alarmSource.push(self.fltstate)
				Acsalarmpy.AlarmSystemInterfaceFactory.done()
				self.getLogger().logError("INVALID NUMBER")

				ex2 = PositionOutOfLimitsExImpl()
                        	ex2.log(self.getLogger())
				raise ex2
				
			else:
				self.telescope.moveTo(TYPES.Position(args[0].az, args[0].el))	 


	def getTelescopePosition(self, *args):
		return self.telescope.getCurrentPosition()

	def setRGB(self, *args):
		#self.getLogger().logInfo("CONSOLE 2 SET RGB ACCESS")	
		pass
