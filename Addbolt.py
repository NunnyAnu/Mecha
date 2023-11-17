import bpy
import json
from typing import List

def input_DataSize(path_to_datafile):
    with open(path_to_datafile, 'r') as openfile:
        json_object = json.load(openfile)        
        head_length = json_object["Head_Length"]
        head_dia = json_object["Head_Diameter"]
        thread_length = json_object["Thread_Length"]
        thread_dia = round(json_object["Thread_Diameter"])
        space_length = json_object["Space_Length"]
        head_type = json_object["type_head"]
        bit_type = json_object["type_bit"]
    return head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()


class BuildaBolt:
    def __init__(self, head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length, path_to_savefile):
      self.bf_Model_Type = 'bf_Model_Bolt'   
      self.bf_Head_Type = head_type          #select on ui
      self.bf_Bit_Type = bit_type            #select on ui 
      self.bf_Shank_Length = space_length    #space
      self.bf_Shank_Dia = thread_dia         #space
      self.bf_Hex_Head_Height = head_length  #head length    
      self.bf_Hex_Head_Flat_Distance = head_dia    #head radius
      self.bf_CounterSink_Head_Dia = head_dia      #head radius
      self.bf_Cap_Head_Height = thread_dia  #head length 
      self.bf_Cap_Head_Dia = head_dia       #head dia
      self.bf_Dome_Head_Dia = head_dia      #head dia
      self.bf_Pan_Head_Dia = head_dia       #head dia
      self.bf_Thread_Length = thread_length #thread length
      self.bf_Major_Dia = thread_dia        #thread
      self.bf_Crest_Percent = 10            #thread  
      self.bf_Root_Percent = 10             #thread
      self.bf_Div_Count = 36                #thread
      self.path_to_savefile = path_to_savefile

    def size_thread(self):
        #m1.4p0.3, m1.6p0.35, m2p0.4, m2.5p0.45
        thread_pitch = {'M3': 0.5, 'M4': 0.7, 'M5': 0.8, 'M6': 1, 'M8': 1.25, 'M10': 1.5, 'M12': 1.75, 'M14': 2, 'M16': 2}
        thread_minor = {'M3': 2.5, 'M4': 3, 'M5': 4, 'M6': 5, 'M8': 6, 'M10': 8, 'M12': 10, 'M14': 12, 'M16': 14}   
        boltM = 'M' + str(self.bf_Major_Dia)
        pitch = thread_pitch[boltM]                
        minor = thread_minor[boltM]
        return pitch, minor
        
    def size_head(self):
        #head_length = m size
        #Allen[depth, dist]
        Allen_bit = {'M3':[1.6, 2.5], 'M4':[2.2, 3], 'M5':[2.5, 4], 
                    'M6':[3, 5], 'M8':[4, 6], 'M10':[5, 8],
                    'M12':[6, 10], 'M14':[7, 12], 'M16':[8, 14]}
        #Torx[depth, size]
        Torx_bit = {'M3':[1.3, 10], 'M4':[1.6, 20], 'M5':[2, 25], 
                    'M6':[3.0, 30], 'M8':[3.3, 40], 'M10':[4.5, 50],
                    'M12':[5.2, 55], 'M14':[5.2, 55], 'M16':[5.2, 55]}
                    
        #Phillips[depth, dia]
        Phillips_bit = {'M3':[1.75, 3.6], 'M4':[2.3, 4.5], 'M5':[2.8, 5.1], 
                        'M6':[3.4, 6.7], 'M8':[4.4, 8.4], 'M10':[5.7, 10],
                        'M12':[5.7, 10], 'M14':[5.7, 10], 'M16':[5.7, 10]}
                        
        if self.bf_Head_Type == 'HEX':
            Head_Type = 'bf_Head_Hex'
        elif self.bf_Head_Type == 'CAP':
             Head_Type = 'bf_Head_Cap'
        elif self.bf_Head_Type == 'DOME':
             Head_Type = 'bf_Head_Dome'
        elif self.bf_Head_Type == 'PAN':
             Head_Type = 'bf_Head_Pan'
        elif self.bf_Head_Type == 'COUNTERSINK':
             Head_Type = 'bf_Head_CounterSink'
            
        
        boltM = 'M' + str(self.bf_Major_Dia)
        if self.bf_Bit_Type == 'ALLEN':
            Bit_Type = 'bf_Bit_Allen'
            depth = Allen_bit[boltM][0] 
            size_float = Allen_bit[boltM][1]
            size_str = "bf_Torx_T10" 
            
        elif self.bf_Bit_Type == 'TORX':
            Bit_Type ='bf_Bit_Torx'
            depth = Torx_bit[boltM][0]
            size_float = Torx_bit[boltM][1]
            size_str = "bf_Torx_T" + str(Torx_bit[boltM][1])
            
        elif self.bf_Bit_Type == 'PHILLIPS':
            Bit_Type ='bf_Bit_Phillips'
            depth = Phillips_bit[boltM][0]
            size_float = Phillips_bit[boltM][1]
            size_str = "bf_Torx_T10" 
            
        else:
            Bit_Type ='bf_Bit_None'
            depth = 0
            size_float = 0
            size_str = "bf_Torx_T10" 
        return Head_Type, Bit_Type, depth, size_float, size_str
        

    def addBolt(self):
        pitch, minor = self.size_thread()
        Head_Type, Bit_Type, depth, size_float, size_str = self.size_head()                                            
        bpy.ops.mesh.bolt_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=True, 
                                            bf_Model_Type = self.bf_Model_Type ,   #fix
                                            bf_Head_Type = Head_Type,     #select on ui
                                            bf_Bit_Type = Bit_Type,      #select on ui   
                                            bf_Shank_Length = self.bf_Shank_Length,              #0
                                            bf_Shank_Dia = self.bf_Shank_Dia,                 #0
                                            bf_Phillips_Bit_Depth = depth,  #bit type fix
                                            bf_Allen_Bit_Depth = depth,           #bit type fix 
                                            bf_Allen_Bit_Flat_Distance = size_float,   #bit type fix
                                            bf_Torx_Size_Type = size_str,            #bit type fix 
                                            bf_Torx_Bit_Depth = depth,            #bit type fix    
                                            bf_Hex_Head_Height = self.bf_Hex_Head_Height,           #head length    
                                            bf_Hex_Head_Flat_Distance = self.bf_Hex_Head_Flat_Distance,   #head radius
                                            bf_CounterSink_Head_Dia = self.bf_CounterSink_Head_Dia,        #head radius
                                            bf_Cap_Head_Height = self.bf_Cap_Head_Height,          #head length 
                                            bf_Cap_Head_Dia = self.bf_Cap_Head_Dia,             #head radius
                                            bf_Dome_Head_Dia = self.bf_Dome_Head_Dia,            #head radius
                                            bf_Pan_Head_Dia = self.bf_Pan_Head_Dia,             #head radius
                                            bf_Philips_Bit_Dia = size_float,          #bit type fix
                                            bf_Thread_Length = self.bf_Thread_Length,            #thread length
                                            bf_Major_Dia = self.bf_Major_Dia,                #thread
                                            bf_Pitch = pitch,                    #thread
                                            bf_Minor_Dia = minor,                #thread
                                            bf_Crest_Percent = 10,            #thread    
                                            bf_Root_Percent = 10,             #thread
                                            bf_Div_Count = 36)                #fix 

    def exportBolt(self):
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
        bpy.ops.export_scene.gltf(
            filepath = self.path_to_savefile,
            export_format='GLB',
            export_apply=True,  # Apply modifiers
            export_colors=True,  # Export vertex colors
            export_normals=True,  # Export normals
            export_cameras=True,  # Export cameras
            export_lights=True,  # Export lights
            export_yup=True  # Y-axis up
        )

if __name__ == '__main__':
    path_to_savefile ="/Users/nunny/Desktop/mechatronic_blender/3DModel/addbolt.glb" 
    path_to_datafile='/Users/nunny/Desktop/mechatronic_blender/data_size.json'
    head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length = input_DataSize(path_to_datafile)
    b1 = BuildaBolt(head_type, bit_type, head_length, head_dia, thread_length, thread_dia, space_length, path_to_savefile)
    b1.addBolt()
    b1.exportBolt()
    
 



