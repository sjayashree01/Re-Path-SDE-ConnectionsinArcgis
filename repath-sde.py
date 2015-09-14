# Author: Jayashree Surendrababu	
# ReMapping Existing SDE Connections inside ArcMap 
import arcpy, os  

try: 	
	arcpy.env.overwriteOutput = True
	folder_path = arcpy.GetParameterAsText(0)	
	arcpy.env.Workspace = folder_path	
	#   Set variables for creating new SDE Connection  	
	fileName = "Connection to Server.sde"  
	serverName = "yourServerName" #arcsde server machine name 
	serviceName = "yourServiceName"  #ArcSDE Service name or TCP port number
	databaseName = "yourDbName"  #db instance
	authType = "DATABASE_AUTH"  #authentication type. db type in our case
	username = "local"  
	password = "local"  
	folderName = "yourConnectionPath" #connection str path 
	saveUserInfo = "SAVE_USERNAME"  
	versionName = "SDE.DEFAULT"  
	saveVersionInfo = "SAVE_VERSION"    
  
	for  mxd_Name in os.listdir(folder_path):
		 fullpath = os.path.join(folder_path, mxd_Name)  
		 if os.path.isfile(fullpath):
			basename, extension = os.path.splitext(fullpath)
			if extension.lower() == ".mxd":				
				arcpy.CreateArcSDEConnectionFile_management(folderName, fileName, serverName, serviceName, databaseName, authType, username, password, saveUserInfo, versionName, saveVersionInfo)  
				mxd = arcpy.mapping.MapDocument(fullpath)
				for df in arcpy.mapping.ListDataFrames(mxd):  
					for lyr in arcpy.mapping.ListLayers(mxd):  
						if lyr.supports("SERVICEPROPERTIES"):  
							servProp=lyr.serviceProperties  
							#Replace old dataset name with new dataset name and replace  
							if (lyr.serviceProperties["ServiceType"]=="SDE") and (lyr.serviceProperties["Service"]== "PortName"):  
								dataSet=lyr.dataSource  								 
								sdeFile="Database Connections\\"+fileName  
								lyr.replaceDataSource(sdeFile,"SDE_Workspace",lyr.name,"")  		
				arcpy.RefreshTOC()  
				arcpy.RefreshActiveView() 
				mxd.save()		    
	del mxd
	
except arcpy.ExecuteError:
    arcpy.AddMessage("Error processing")	  
