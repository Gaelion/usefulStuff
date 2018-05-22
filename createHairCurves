import math
import maya.cmds as cmds
import pymel.core as pym
import maya.OpenMaya as om
from maya import OpenMaya
from functools import partial
from shiboken import wrapInstance  # @UnresolvedImport
import maya.OpenMayaUI as apiUI
from PySide import QtCore, QtGui
from ilion_maya.gui_utils import lib as gui_utils  #  @ UnresolvedImport

def maya_main_window():
	main_win_ptr = apiUI.MQtUtil.mainWindow()
	return wrapInstance(long(main_win_ptr), QtGui.QWidget)

class ControlUI(QtGui.QWidget):
	def __init__(self, parent = maya_main_window()):
		super(ControlUI, self).__init__(parent)
		self.locsOn = True
		self.crvOn = True
		self.multCrvOn = False
		self.crvNumber = 20
		self.crvDgree = 1
		self.locExist = False
		self.headGeom = None
		self.chuncksGeoOn = False
		self.createWindow()
		self.connectSignals()
		self.updateWindow()

	def createWindow(self):
		self.main_layout = QtGui.QVBoxLayout()
		self.setLayout(self.main_layout)
		self.main_ui = gui_utils.addUiFromFile('ui/createCrvHair.ui', 'rigging_curvehair', self)

	def connectSignals(self):
		updateCrvDegree_1 = partial(self.updateCrvDegree, button=self.main_ui.crv_d_btn_1)
		updateCrvDegree_3 = partial(self.updateCrvDegree, button=self.main_ui.crv_d_btn_3)
		updateCrvDegree_5 = partial(self.updateCrvDegree, button=self.main_ui.crv_d_btn_5)

		self.main_ui.crv_d_btn_1.toggled.connect(updateCrvDegree_1)
		self.main_ui.crv_d_btn_3.toggled.connect(updateCrvDegree_3)
		self.main_ui.crv_d_btn_5.toggled.connect(updateCrvDegree_5)

		self.main_ui.createCrvs_btn.clicked.connect(self.callProcess)
		self.main_ui.createBaseLoc_btn.clicked.connect(self.manageHeadLoc)

	def updateCrvDegree(self,isChecked,button):
		if isChecked:
			btnSetStyleSheet='background-color: rgb({0},{1},{2});'.format (67,137,67)
			self.crvDgree = button.text()
		else :
			btnSetStyleSheet="background-color: grey"
		button.setStyleSheet(btnSetStyleSheet)

	def updateHeadLoc(self):
		self.locExist = cmds.objExists("head_Loc")
		if self.locExist:
			self.main_ui.createBaseLoc_btn.setText("Delete Base Locator")
			btnSetStyleSheet='background-color: rgb({0},{1},{2});'.format (67,137,67)
			self.main_ui.createBaseLoc_btn.setStyleSheet(btnSetStyleSheet)
		else:
			self.main_ui.createBaseLoc_btn.setText("Create Base Locator")
			btnSetStyleSheet='background-color: rgb({0},{1},{2});'.format (195,58,58)
			self.main_ui.createBaseLoc_btn.setStyleSheet(btnSetStyleSheet)

	def updateWindow(self):
		for btn in (self.main_ui.crv_d_btn_1,self.main_ui.crv_d_btn_3,self.main_ui.crv_d_btn_5):
			self.updateCrvDegree(btn.isChecked(),btn)
		self.updateHeadLoc()
		self.main_ui.createCrvs_btn.show()
		self.main_ui.curveHairProgressBar.hide()

		if self.headGeom is not None:
			self.main_ui.headGeoName_lab.setText(self.headGeom)
			self.main_ui.headGeoName_lab.setStyleSheet('QLabel {foreground-color: None; color: green;}')
		else:
			self.main_ui.headGeoName_lab.setText("No geo Picked")
			self.main_ui.headGeoName_lab.setStyleSheet('QLabel {foreground-color: None; color: red;}')
		cmds.refresh(f=1)

	def waitWindow(self):
		self.main_ui.createBaseLoc_btn.setText("..Select Head Geometry..")
		btnSetStyleSheet='background-color: rgb({0},{1},{2});'.format (176,148,53)
		self.main_ui.createBaseLoc_btn.setStyleSheet(btnSetStyleSheet)

	def manageHeadLoc(self):
		self.updateHeadLoc()
		if self.locExist:
			cmds.delete("head_Loc")
			self.updateWindow()
		else:
			self.selectGeoContextTool()

	def callProcess(self):
		if not self.locExist:
			cmds.warning("Please, Create the Base Locator")
			return
		if not self.getUIdata():
			return
		self.main_ui.createCrvs_btn.hide()
		self.main_ui.curveHairProgressBar.show()
		CreateCurveHair(locsOn = self.locsOn,
						crvOn = self.crvOn,
						multCrvOn = self.multCrvOn,
						crvNumber = self.crvNumber,
						crvDgree = self.crvDgree,
						snapToGeo = self.snapToGeo,
						chuncksGeoOn = self.chuncksGeoOn,
						useUI = True)
		self.updateWindow()

	def getUIdata(self):
		self.locsOn = self.main_ui.locators_chk.isChecked()
		self.crvOn = self.main_ui.centerCrv_chk.isChecked()
		self.multCrvOn = self.main_ui.multiCrv_chk.isChecked()
		self.crvNumber = self.main_ui.crvNumb_val.value()
		self.chuncksGeoOn = self.main_ui.chuncksGeo_chk.isChecked()
		if not self.main_ui.snapToBase_chk.isChecked():
			self.snapToGeo = None
		else :
			self.snapToGeo = self.headGeom
		if not True in [self.locsOn,self.crvOn,self.multCrvOn]:
			return False
		return True

	def createHeadLoc(self):
		if not len(cmds.ls(sl=1)) == 0:
			bbList = []
			for sel in cmds.ls(sl=1):
				bbox = cmds.xform(sel, q=1, boundingBox=1)
				bbList.append(bbox)
			bbFinal = []
			for bb in bbList:
				if len(bbFinal) == 0:
					bbFinal = bb
				for val in [0,1,2]:
					if bb[val] < bbFinal[val]: bbFinal[val] = bb[val]
				for val in [3,4,5]:
					if bb[val] > bbFinal[val]: bbFinal[val] = bb[val]
			centerX = (bbFinal[0] + bbFinal[3]) / 2.0
			centerY = (bbFinal[1] + bbFinal[4]) / 2.0
			centerZ = (bbFinal[2] + bbFinal[5]) / 2.0
			loca = cmds.spaceLocator(n="head_Loc",)
			cmds.xform(loca, t=(centerX,centerY,centerZ))
		else:
			cmds.spaceLocator(n="head_Loc")
		cmds.warning("Please, Move the head_Loc. Close to the 'birth' of the hairs")

	def selectGeoContextPress(self):
		pressPosition = cmds.draggerContext( 'selGeoContext', query=True, anchorPoint=True)
		# grabbing current 3d view
		active_view = apiUI.M3dView.active3dView()

		# Screen position of mouse
		x = int(pressPosition[0])
		y = int(pressPosition[1])

		#making my ray source and direction
		ray_source = OpenMaya.MPoint()
		ray_direction = OpenMaya.MVector()

		#Converting to world
		active_view.viewToWorld(x ,y , ray_source, ray_direction)

		#Select from screen
		om.MGlobal.selectFromScreen(x,y, om.MGlobal.kReplaceList)
		objects = om.MSelectionList()
		om.MGlobal.getActiveSelectionList(objects)

		#Convert from MSelectionList object to string
		fromScreen = []
		objects.getSelectionStrings(fromScreen)

		self.headGeom = fromScreen[0]
		if cmds.objExists(fromScreen[0]):
			self.createHeadLoc()

		cmds.setToolTo('moveSuperContext')
		self.updateWindow()


	def selectGeoContextTool(self):
		self.waitWindow()
		ctx = partial(self.selectGeoContextPress)
		if(cmds.draggerContext('selGeoContext', exists=True)):
			cmds.deleteUI('selGeoContext')
		cmds.draggerContext( 'selGeoContext', pressCommand = ctx, cursor='hand', projection = "s")
		cmds.setToolTo('selGeoContext')


class CreateCurveHair():
	def __init__(self, locsOn = True, crvOn = True, multCrvOn = False, crvNumber = 20, crvDgree = 1, snapToGeo = None,chuncksGeoOn = False, useUI = False):
		self.locsOn = locsOn
		self.crvOn = crvOn
		self.multCrvOn = multCrvOn
		self.crvNumber = crvNumber
		self.crvDgree = crvDgree
		self.snapToGeo = snapToGeo
		self.chuncksGeoOn = chuncksGeoOn
		self.useUI = useUI
		if self.useUI : self.doProgressBar()
		self.generate()

	def doProgressBar(self):
		if 'createCurvesFromGeo' in gui_utils.Container._instances  :
			the_window = gui_utils.Container._instances['createCurvesFromGeo'].children()[2]
			self.bar = the_window.findChild(QtGui.QProgressBar,"curveHairProgressBar")

	def generate(self):
		exist, hairList = self.getGeos()
		if not exist:
			return
		if self.useUI :
			valueToBar = 100.0/len(hairList)
			varNormal= 0

		allCurvesGrp = cmds.createNode("transform",name = "hair_curves_GRP")

		for hair in hairList:
			if self.useUI :
				varNormal += valueToBar
				self.bar.setValue(varNormal)
			# esto me selecciona todos los edge vertex , recordar apagar los constraints de seleccion :
			pym.select(hair)
			cmds.polySelectConstraint( m=3, t=1, w=1 )
			cmds.polySelectConstraint( dis=True )
			vtxL = pym.ls(sl=1,fl=1)
			# getOrderedLoops .- es el proceso para generar un dict de todos los loops de la geometria ordenados
			loopDict = self.getOrderedLoops(vtxL)

			if self.multCrvOn:
				tempFolyGrp = cmds.createNode("transform",name = "{0}_follicles_GRP".format(hair.name()))
			curveGrp = cmds.createNode("transform",name = "{0}_curves_GRP".format(hair.name()))
			centerList = []
			tempPlane = None
			folNames = []
			folAllPos = {}

			if self.locsOn :
				centerGrp = cmds.createNode("transform",name = "{0}_locators_GRP".format(hair.name()))
				cmds.parent(centerGrp,curveGrp)

			for edgeLoop in sorted(loopDict.keys()):
				strNames = [v.name() for v in loopDict[edgeLoop]]
				vtxPos = [cmds.xform (v,q=True, ws=True, t=True) for v in strNames]

				center = self.getCenterFromSel(strNames)

				if (self.snapToGeo is not None) and (edgeLoop == "0000"):
					snappedCenter = self.getClosestMeshPoint(self.snapToGeo,center)
					center = (snappedCenter[0],snappedCenter[1],snappedCenter[2])

				centerList.append(center)
				if self.multCrvOn:
					if not tempPlane:
						tempCir = cmds.circle(d=1,nr=(0,1,0),s=len(vtxPos),n="{0}_tempCircle".format(hair))
						cirPos = []
						for i in range(len(vtxPos)):
							cirPos.append(cmds.xform("{0}.cv[{1}]".format(tempCir[0],i),ws=True,t=True,q=1))
							if i == len(vtxPos)-1:
								cirPos.append(cmds.xform("{0}.cv[{1}]".format(tempCir[0],len(vtxPos)),ws=True,t=True,q=1))
						cmds.delete(tempCir)

						tempPlane = cmds.polyCreateFacet(name = "{0}_follyPlane".format(hair),p=cirPos[:-1])

						cmds.polyMultiLayoutUV(tempPlane[0], lm=1, sc=2, rbf=1, fr=1, ps= 0.1 , psc=0, su=2.1, sv = 2.1, ou = -1.05, ov =-1.05) # scale all the uv t the FULL U V space
						pmPlane = pym.PyNode(tempPlane[0])

						# Vogels algorthm
						golden_angle = math.pi * (3 - math.sqrt(5))
						points = []
						for i in xrange(self.crvNumber):
							theta = i * golden_angle
							r = math.sqrt(i) / math.sqrt(self.crvNumber)
							points.append((r * math.cos(theta), r * math.sin(theta)))
						# Vogels algorthm end

						for i in points:
							oFoll = self.create_follicle(pmPlane, i[0], i[1])
							cmds.parent(oFoll.getParent().name(), tempFolyGrp)
							folNames.append(oFoll.getParent().name())
							folAllPos[oFoll.getParent().name()] = []

						for pos in vtxPos:
							cmds.xform("{0}.vtx[{1}]".format(tempPlane[0],vtxPos.index(pos)),ws=True,t=(pos[0],pos[1],pos[2]))
					else :
						for pos in vtxPos:
							cmds.xform("{0}.vtx[{1}]".format(tempPlane[0],vtxPos.index(pos)),ws=True,t=(pos[0],pos[1],pos[2]))

					if (self.snapToGeo is not None) and (edgeLoop == "0000"):
						for fol in folNames:
							pos = cmds.xform(fol,ws=1,q=1,t=1)

							snappedCenterFol = self.getClosestMeshPoint(self.snapToGeo,pos)
							centerFol = [snappedCenterFol[0],snappedCenterFol[1],snappedCenterFol[2]]

							folAllPos[fol].append(centerFol)

					else:
						for fol in folNames:
							pos = cmds.xform(fol,ws=1,q=1,t=1)
							folAllPos[fol].append(pos)

				if self.locsOn :
					spaceLoc, = cmds.spaceLocator(name="{0}_{1}_center_LOC".format(hair.name(),edgeLoop))
					cmds.setAttr (spaceLoc+".t", *center)
					cmds.setAttr (spaceLoc+".s", *[0.1,0.1,0.1])
					cmds.parent(spaceLoc, centerGrp)

			if self.crvOn:
				centerCurveGrp = cmds.createNode("transform",name = "{0}_centerCurve_GRP".format(hair.name()))
				centerCurve = cmds.curve( d=float(self.crvDgree), p= centerList,name="{0}_center_curve_d1".format(hair))
				cmds.parent(centerCurve, centerCurveGrp)
				cmds.parent(centerCurveGrp,curveGrp)

			if self.multCrvOn:
				multiGrp = cmds.createNode("transform",name = "{0}_multiCurve_GRP".format(hair.name()))
				for fol in folNames:
					multCurve = cmds.curve( d=float(self.crvDgree), p= folAllPos[fol],name= "multi_curve_d1_{0}".format( fol.split("_")[-1] ) )
					cmds.parent(multCurve, multiGrp)
				cmds.parent(multiGrp,curveGrp)
				cmds.delete(tempPlane,tempFolyGrp)
			cmds.parent(curveGrp,allCurvesGrp)

			if self.chuncksGeoOn:
				origHairParent = cmds.listRelatives(hair.name(),p=1)
				hairChunksGRP,newhair= self.createChunksFromGeo(hair,loopDict)
				cmds.parent(hairChunksGRP,allCurvesGrp)
				if origHairParent != None :
					cmds.parent(newhair,origHairParent)

	def createChunksFromGeo(self,currHair,loopDict):
		import pprint as pp

		hairChunksGRP = cmds.createNode("transform",name = "{0}_hairChunksGeo_GRP".format(currHair.name()))
		deleted = False
		newHair= None

		justIndexDict = {}
		for edge in sorted(loopDict.keys()):
			justIndex = []
			for v in loopDict[edge] :
				justIndex.append(v.index())
			justIndexDict[edge] = justIndex

		for edge in sorted(justIndexDict.keys()):
			if int(edge)+1 >= len(justIndexDict):
				continue
			if deleted :
				currHair = pym.PyNode(newHair)

			hairShape = currHair.getShape().name()
			hairName = currHair.name()

			firstLoop = []
			secondLoop = []
			for vtx in justIndexDict[edge] :
				firstLoop.append(pym.MeshVertex(currHair,vtx))

			for vtx in justIndexDict['{:04d}'.format(int(edge)+1)] :
				secondLoop.append(pym.MeshVertex(currHair,vtx))

			pym.select(firstLoop + secondLoop)

			cmds.ConvertSelectionToContainedFaces()
			cmds.polyChipOff(ch=1,kft=1,dup=1,off=0)

			hairPieces = cmds.polySeparate(hairShape,rs=1,ch=1)

			for i in hairPieces: cmds.DeleteHistory(i)

			cmds.parent(hairPieces[1], hairChunksGRP)
			cmds.rename(hairPieces[1],"{0}_piece_{1}".format(hairName,edge))

			deletable, = cmds.listRelatives(hairPieces[0],p=1)
			cmds.parent(hairPieces[0],w=1)

			cmds.delete(deletable)
			newHair = cmds.rename(hairPieces[0],hairName)
			deleted = True

		return hairChunksGRP,newHair


	def getGeos(self):
		if len(cmds.ls(sl=1)) == 0:
			return False , "Please select a Hair Clump."
		hairList =  pym.ls(sl=1,sn=1)
		return True, hairList

	def getOrderedLoops(self,vtxL):
		comp = {"edge1":[],"edge2":[]}
		for v in vtxL:
			ring = []
			ring.append(v)
			neigh = v.connectedVertices()
			for n in neigh:
				if n in vtxL :ring.append( n)
			pym.select(ring)
			pym.polySelectSp (l=1)
			edge = pym.ls(sl=1,fl=1)
			if edge == comp["edge1"]:continue
			if len(comp["edge1"]) == 0 and len(comp["edge2"]) == 0:
				comp["edge1"] = edge
				continue
			comp["edge2"] = edge
		# aqui se calcula el vertice mas cercano de todos los vertices seleccionados
		loc = pym.PyNode('head_Loc')
		pos = loc.getRotatePivot(space='world')
		closestVert = None
		minLength = None
		secMinLength = None
		secClosestVert = None
		for v in vtxL:
			thisLength = (pos - v.getPosition(space='world')).length()
			if minLength is None or thisLength < minLength:
				minLength = thisLength
				closestVert = v
		# a partir del vtx mas cercano, comparamos con el loop mas cercano
		originEdge = [comp[edge]for edge in comp if closestVert in comp[edge]][0]
		# ahora encontramos el segundo mas cercano, para tener el orden de loop
		for neighb in closestVert.connectedVertices():
			if neighb not in originEdge:
				continue
			thisLength = (pos -  neighb .getPosition(space='world')).length()
			if secMinLength is None or thisLength < secMinLength:
				secMinLength = thisLength
				secClosestVert = neighb
		# ahora loopeamos a traves de todos los loops en orden, recursividad.
		# se nos genera "loopDict" un dict con todos los loops
		fullVerts = []
		loopDict = {}
		loopNumber = 0
		self.findAllLoops (originEdge ,fullVerts  , loopDict , loopNumber, closestVert ,secClosestVert)
		return loopDict

	def findAllLoops (self,currLoop, fullVerts  , ordVertsLoops , loopNumber ,closestVert , secClosestVert):
		"""Recursive function, to get all loops of a cylinder shape, with a given vertex border, and reordering the loops vertex

		Args:
			currLoop = pymel vertex list [MeshVertex(u'geo_Shape.vtx[1]'),...]. Use a border!
			fullVerts = []
			ordVertsLoops  = {}
			loopNumber = 0
			closestVert =
			secondClosestVert =

		Returns:
			ordVertsLoops = Dictionary of every loop in order, growing from the given one

		Raises:

		"""
		ordCurrentLoop = [closestVert,secClosestVert]
		newFirst = None
		newSec = None
		newLoop = []

		for v in currLoop:
			if v not in fullVerts:
				fullVerts.append(v)

		for vx in ordCurrentLoop:
			if ordCurrentLoop.index(vx) == 0:
				for n in vx.connectedVertices():
					if n not in fullVerts:
						newFirst = n
			if ordCurrentLoop.index(vx) == 1:
				for n in vx.connectedVertices():
					if n not in fullVerts:
						newSec = n

		for ordering in range(1, len(currLoop)):
			vtx = ordCurrentLoop[ordering]
			new = [v for v in vtx.connectedVertices() if (v not in ordCurrentLoop) and (v in currLoop)]
			if not new == []:
				ordCurrentLoop.append(new[0])

		for vx in currLoop:
			neighs = vx.connectedVertices()
			for n in neighs:
				if n not in fullVerts:
					newLoop.append(n)

		if newLoop == []:
			ordVertsLoops['{:04d}'.format(loopNumber)] = ordCurrentLoop
			return ordVertsLoops
		else:
			ordVertsLoops['{:04d}'.format(loopNumber)] = ordCurrentLoop
			loopNumber += 1
			ordVertsLoops['{:04d}'.format(loopNumber)] = newLoop
			self.findAllLoops(newLoop, fullVerts, ordVertsLoops, loopNumber,newFirst,newSec)

	def getCenterFromSel(self,objects):
		"""Gets the baricentral position depending on the vertex selection

		Args:
			objects = objects to get the center

		Returns:
			sumPt = A pymel datatype Point object with 3 coords

		Raises:

		"""
		if not objects:
			objects = cmds.ls(sl=1)

		pX, pY,	pZ = [0.0,0.0,0.0]
		sumPt = None

		for ob in objects:
			pass
			pos = cmds.xform(ob,q=True,ws=True,t=True)
			pX += pos[0]
			pY += pos[1]
			pZ += pos[2]

		finalPos = [pX/len(objects),pY/len(objects),pZ/len(objects)]
		finalCenter = [pX*(1./len(objects)),pY*(1./len(objects)),pZ*(1./len(objects))]

		return finalCenter

	def create_follicle(self,geo, uPos=0.0, vPos=0.0):
		"""Create a follicle in a geo mesh

		Args:
			geo = PyNode node from a geo ("pym.ls(sl=1)[0]")
			uPos= U position for the follicle . default is 0.0
			vPos= V position for the follicle . default is 0.0
		Returns:
			oFoll = PyNode Follicle Node

		Raises:

		"""
		if geo.type() == 'transform':
			geo = geo.getShape()
		elif geo.type() == 'nurbsSurface':
			pass
		else:
			'Warning: Input must be a nurbs surface.'
			return False

		# create a name with frame padding
		pName = '_'.join((geo.name(),'follicle','#'.zfill(2)))
		oFoll = pym.createNode('follicle', name=pName)
		#geo.local.connect(foll.inputSurface) if nurbs
		geo.outMesh.connect(oFoll.inputMesh)

		geo.worldMatrix[0].connect(oFoll.inputWorldMatrix)
		oFoll.outRotate.connect(oFoll.getParent().rotate)
		oFoll.outTranslate.connect(oFoll.getParent().translate)
		oFoll.parameterU.set(uPos)
		oFoll.parameterV.set(vPos)
		oFoll.getParent().t.lock()
		oFoll.getParent().r.lock()

		return oFoll

	def getClosestMeshPoint(self,meshName,startWP):
		"""Get the closest point between the position 1 points, and a Geo

		Args:
			meshName = String name of the mesh to check for collision
			startWP= start world position of the vector
		Returns:
			outPoint = MPoint position of the intersection

		Raises:

		"""
		sel=OpenMaya.MSelectionList()
		sel.add(meshName)

		obj=OpenMaya.MDagPath()
		sel.getDagPath(0,obj)

		fnMesh=OpenMaya.MFnMesh(obj)
		inPoint=OpenMaya.MPoint(startWP[0],startWP[1],startWP[2])
		outPoint=OpenMaya.MPoint()
		fnMesh.getClosestPoint(inPoint,outPoint,OpenMaya.MSpace.kWorld)

		return outPoint

	def getIntersectPoint(self,meshName,startWP,FinishWP):
		"""Get an intersecting point between the vector of 2 points, and a Geo

		Args:
			meshName = String name of the mesh to check for collision
			startWP= start world position of the vector
			FinishWP= finish world position of the vector
		Returns:
			hit = boolean, True if hit
			hitPoint = MFloatPoint position of the intersection

		Raises:

		"""
		def nameToDag( name ):#retireves the right DAG node for selected objects
				selectionList = om.MSelectionList()
				selectionList.add( name )
				node = om.MDagPath()
				selectionList.getDagPath( 0, node )
				return node
		#startWP = mc.xform('hair04_l_geo1_0000_center_LOC',q=1,rp=1,ws=1)
		#FinishWP = mc.xform('hair04_l_geo1_0001_center_LOC',q=1,rp=1,ws=1)
		vectBtwPnts=  ((startWP  [0] -FinishWP  [0])*-1), ((startWP  [1] - FinishWP  [1])*-1), ((startWP  [2] -FinishWP  [2])*-1)
		vectorToFinish = om.MFloatVector(vectBtwPnts[0],vectBtwPnts[1],vectBtwPnts[2])

		dag = nameToDag(meshName)

		meshFn = om.MFnMesh()
		meshFn.setObject( dag )

		raySource = om.MFloatPoint(startWP[0],startWP[1],startWP[2])
		rayDirection = vectorToFinish
		rayDirection = rayDirection.normal()

		#hitFacePtr = om.MScriptUtil().asIntPtr()
		hitFacePtr_u = om.MScriptUtil()
		hitFacePtr = hitFacePtr_u.asIntPtr()   # hitFacePtr only safe to use while hitFacePtr_u lives

		hitPoint   = om.MFloatPoint()

		idsSorted          = False
		testBothDirections = False
		faceIds            = None
		triIds             = None
		accelParams        = None
		hitRayParam        = None
		hitTriangle        = None
		hitBary1           = None
		hitBary2           = None
		maxParamPtr        = 99999999
		worldSpace         = om.MSpace.kWorld

		hit =  meshFn.closestIntersection(raySource,
		rayDirection,
		faceIds,
		triIds,
		idsSorted,
		worldSpace,
		maxParamPtr,
		testBothDirections,
		accelParams,
		hitPoint,
		hitRayParam,
		hitFacePtr,
		hitTriangle,
		hitBary1,
		hitBary2)

		return hit,hitPoint
