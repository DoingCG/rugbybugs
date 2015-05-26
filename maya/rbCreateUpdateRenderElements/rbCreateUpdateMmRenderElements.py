




#rbCreateUpdateMmRenderElements Module
#------------------------------------------------------------------

'''
Description:
Creates/Updates Multi Matte VrayRenderElements according to our pipeline standards
'''

'''
ToDo:

'''




#Imports
#------------------------------------------------------------------
import pymel.core as pm
import maya.OpenMaya as openMaya







#RbCreateUpdateMmRenderElements class
#------------------------------------------------------------------

class RbCreateUpdateMmRenderElements():
	
	#Constructor / Main Procedure
	def __init__(self):
		
		#Instance Vars
		#------------------------------------------------------------------
		self.verbose = True
		
		
	
	#Top Level Methods
	#------------------------------------------------------------------
	
	#createUpdateMultiMatteElements
	def createUpdateMultiMatteElements(self, setStatusFunction = False):
		
		
		
		#Check if Vray Loaded, else set Status and return
		if not(self.vrayLoaded(setStatusFunction)): return None
		
		
		#deleteCurrentMultiMatteElements
		self.deleteCurrentMultiMatteElements()
		
		#getSceneObjectIDList
		objectIdList = self.getSceneObjectIdList()
		
		#createMultiMattes if objectIdList not empty
		if(objectIdList):
			#createMMs
			self.createMultiMattes(objectIdList)
			#setStatus
			if(setStatusFunction): setStatusFunction('Multi mattes created successfully')
			
		else:
			#setStatus
			if(setStatusFunction): setStatusFunction('No object Ids found, no Multi mattes created')
		
	
	
	
	
	
	
	
	#Methods
	#------------------------------------------------------------------
	
	
	#createMultiMattes
	def createMultiMattes(self, objectIdList):
		
		#create mMRE
		mMRE = self.createRenderElement('MultiMatteElement')
		self.renameMultiMatteRE(mMRE)
		#iterate through objectIdList
		indexId = 1
		index = 0
		for id in objectIdList:
			
			#check if %3 of indexId is not 0
			if(indexId % 3 != 0): 
				
				#set vray mm attr based on indexId
				if(indexId == 1): pm.setAttr(mMRE.vray_redid_multimatte, id)
				if(indexId == 2): pm.setAttr(mMRE.vray_greenid_multimatte, id)
				
				#increment indexId
				indexId = indexId + 1
			
			#else (meaning indexId % 3 == 0), create new renderelement and set indexId back to 1
			else:
				
				#set blue id attr for multimatte
				if(indexId == 3): pm.setAttr(mMRE.vray_blueid_multimatte, id)
				
				try:
					#try to access index+1 element from list to make sure current element has not been the last
					testId = objectIdList[index+1]
					#Create new renderelement
					mMRE = self.createRenderElement('MultiMatteElement')
					self.renameMultiMatteRE(mMRE)
					#set indexId back to one
					indexId = 1
				except:
					pass
			
			
			#increment list index
			index = index + 1
	
	
	#deleteCurrentMultiMatteElements
	def deleteCurrentMultiMatteElements(self):
		
		#get all Mm REs
		multiMatteREList = self.getRenderElementsByPrefix('rbMm')
		#delete if list != empty
		if(multiMatteREList): pm.delete(multiMatteREList)
		
	
	
	#getSceneObjectIdList
	def getSceneObjectIdList(self):
		
		#deselect all
		pm.select(cl = True)
	
		#list all scene objects
		sceneObjList = pm.ls(fl = True)
		
		#Iterate through scene objects list and if obj has vrayObjId attr then add to objIdList
		objIdList = []
		
		for obj in sceneObjList:
			if(pm.hasAttr(obj, 'vrayObjectID', checkShape = True)):
				objIdList.append(pm.getAttr(obj.vrayObjectID))
				
		#return duplicate free list
		return sorted(list(set(objIdList)))
		
		
	#renameMultiMatteRE
	def renameMultiMatteRE(self, mMRE):
		
		#rename
		pm.rename(mMRE, 'rbMmRenderElement')
		
		#SetAttrs on mMRE
		pm.setAttr(mMRE.vray_name_multimatte, mMRE.name())
	
	
	
	#Shared Methods
	#------------------------------------------------------------------
	
	
	#REWithAttrAndValueExists
	def REWithAttrAndValueExists(self, attrName, attrValue):
		
		#List all nodes of Type VRayRenderElement
		REList = pm.ls(fl = True, typ = 'VRayRenderElement')
		
		#if list < 1 return False (no RE in scene, ready to create)
		if not(REList): return False
		
		#if list larger check if REName in list of RElements
		for RE in REList:
			#check if RE has attr of attrName and if return True
			try:
				if(pm.getAttr(RE.name() +'.' +attrName) == attrValue): return True
			except:
				pass
		
		#Else False (ready to create)
		return False
		
		
		
	
	
	#getRenderElementsByPrefix
	def getRenderElementsByPrefix(self, prefix):
		
		#clear selection
		pm.select(cl = True)
		
		#get list of all REs
		renderElementsList = pm.ls(fl = True, typ = 'VRayRenderElement')
		
		#if renderElementList < 1 return renderElementList
		if not(renderElementsList): return renderElementsList
		
		#iterate through renderElementList and append to lsList when name beginning matches prefix
		lsResList = []
		prefixLength = len(prefix)
		for RE in renderElementsList:
			if(RE.name()[0:prefixLength] == prefix): lsResList.append(RE)
			
		return lsResList
	
	
	
	
	#createRenderElement
	def createRenderElement(self, renderElementName):
		
		#clear Selection
		pm.select(cl = True)
		
		#build MEL Cmd
		createRElementMELCmd = 'vrayAddRenderElement ' +renderElementName +';'
		
		#Execute
		pm.mel.eval(createRElementMELCmd)
		
		#return created RenderElementNode
		renderElement = pm.ls(sl = True, fl = True)[0]
		pm.select(cl = True)
		
		return renderElement
		
	
		
		
	#vrayLoaded
	def vrayLoaded(self, setStatusFunction = False):
		#Get list of all loaded plugIns
		plugInList = pm.pluginInfo( query=True, listPlugins=True )
		
		#Return true if loaded else setStatus and return false
		if('vrayformaya' in plugInList): return True
		
		if(setStatusFunction): setStatusFunction('Vray for Maya Plugin not loaded')
		return False
	
	
	
	
	