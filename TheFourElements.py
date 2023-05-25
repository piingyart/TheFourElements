bl_info = {
    "name" : "The Four Elements", #Add-on namn
    "verision" : (1,0), 
    "blender" : (3,3,0), #Blender verision
    "category" : "Materials"
    }


import bpy



#Skapar en klass som gör att vi kan se vårt tool när vi trycker på n
class ElementsPanel (bpy.types.Panel) :
    bl_label = "Elements Panel"
    bl_idname = "PT_ElementsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Elements"
    
    def draw(self, context) :
        layout = self.layout
        
        row = layout.row() # skapar ett "mellanrum"
        row.label(text = "Elements Add-on", icon = 'LIGHT_SUN')
        row = layout.row()
        row.label(text = "These Addons are more toward")
        row = layout.row()
        row.label(text = "the cheap verision of elements")
        row = layout.row()
        row.label(text = "Have Fun! :) ")
        
 
#Skapar en underrubrik i Elements Panelen, där man finner de fyra elementen
class EarthPanel(bpy.types.Panel) :
    bl_label = "Elements"
    bl_idname = "PT_Earth"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Elements"
    bl_parent_id = "PT_ElementsPanel" #parent-id är i den "kategorin" vi placerar dessa fyra element
    bl_options = {"DEFAULT_CLOSED"} #anger att underrubrkens innehåll ska vara stängt som default
    
    
    def draw(self, context) :
        layout = self.layout
        
        row = layout.row() 
        row.label(text = "Add Earth (Mud) material", icon = 'KEYTYPE_JITTER_VEC') #lägger till text till en knapp för Earth material
        row = layout.row() 
        row.operator("shader.earth_operator") #skapar själva kanppen "Earth Material"
        
        row = layout.row() 
        row.label(text = "Add Fire (Lava) material", icon = 'KEYTYPE_MOVING_HOLD_VEC') #lägger till en knapp för fire material
        row = layout.row() 
        row.operator("shader.fire_operator") #skapar själva kanppen "Fire Material"
        
        row = layout.row() 
        row.label(text = "Add Air (Ghost) material", icon = 'HANDLETYPE_FREE_VEC') #lägger till text till en knapp för Air material
        row = layout.row() 
        row.operator("shader.air_operator") #skapar själva kanppen "Air Material"
        
        row = layout.row() 
        row.label(text = "Add Water (Ocean) material", icon = 'KEYTYPE_BREAKDOWN_VEC') #lägger till text till en knapp för Water material
        row = layout.row() 
        row.operator("shader.water_operator") #skapar själva kanppen "Water Material"
        row = layout.row()         
        

############################################################################
                            
                            # EARTH MATERIAL #
 
#skapar en klass för materialet Earth       
class shader_earth(bpy.types.Operator):
    bl_label = "Earth Material" #namnet på materialet
    bl_idname = "shader.earth_operator" #namnet som används när vi kallar på det
    
    def execute(self, context):
        
        materialEarth = bpy.data.materials.new(name = "Earth") #skapar ett nytt material
        materialEarth.use_nodes = True #Detta gör det möjligt att använda nodes
        
        materialEarth.node_tree.nodes.remove(materialEarth.node_tree.nodes.get('Principled BSDF')) #tar bort standard Principle BSDF - node
        materialEarth.node_tree.nodes.remove(materialEarth.node_tree.nodes.get('Material Output')) #tar bort standard Material Output - node
         
        bsdf = materialEarth.node_tree.nodes.new('ShaderNodeBsdfPrincipled') #skapar en ny Principle BSDF node som jag kallar bsdf
        materialOutput = materialEarth.node_tree.nodes.new('ShaderNodeOutputMaterial') #skapar en ny Material Output som jag kallar materialOutput
        materialOutput.location = (300,0) #anger plats på vart materialOutput ska befinna sig i node-tree
        

        #Lägger till en Color Rampen som ska placeras i Base Color på bsdf
        cRampColor = materialEarth.node_tree.nodes.new('ShaderNodeValToRGB')
        cRampColor.location = (-400,100) #anger plats i node-tree
        cRampColor.label = "Color Ramp Color" #Byter namn på ColorRamp för förenkling (med anleding till att jag har fler Color Ramps)
        cRampColor.color_ramp.elements.new(position = 0.5) # skapar ett nytt "color stop" med position 0.5
        cRampColor.color_ramp.elements[0].position = (0.3) #ändrar postition på första "color stop"
        #ändrar färg på respektive "color stop": 
        cRampColor.color_ramp.elements[0].color = (0,0,0,1) #svart färg
        cRampColor.color_ramp.elements[1].color = (0.024, 0.008, 0.002, 1) #brun-ish färg
        cRampColor.color_ramp.elements[2].color = (0.016, 0.008, 0.004, 1) #brun-isf färg 
        
        #lägger till colorrampen som ska placeras i Roughness
        cRampRough = materialEarth.node_tree.nodes.new('ShaderNodeValToRGB')
        cRampRough.location = (-400,-200)
        cRampRough.label = "Color Ramp Roughness" #Byter namn på ColorRamp för förenkling
        cRampRough.color_ramp.elements[0].position = (0.05) #ändrar postition på första color stop
        cRampRough.color_ramp.elements[1].position = (0.73) #ändrar postition på andra color stop
        
        #lägger till colorrampen som ska placeras i en Bump-node och sedan i Normal i bsdf
        cRampBump = materialEarth.node_tree.nodes.new('ShaderNodeValToRGB')
        cRampBump.location = (-900,-1000) #anger position
        cRampBump.label = "Color Ramp Bump" #Byter namn på ColorRamp för förenkling
        cRampBump.color_ramp.elements[0].position = (0.05)  #ändrar postition på första color stop
        cRampBump.color_ramp.elements[1].position = (0.13)  #ändrar postition på andra color stop
        
        #lägger till en Bump som jag namnger Bump1 som ska in i Normal på BSDF
        bump1 = materialEarth.node_tree.nodes.new('ShaderNodeBump')
        bump1.label = "Bump1"
        bump1.location = (-200,-800)
        
        #lägger till en Bump som jag namnger Bump2 som ska in i Normal på bump1
        bump2 = materialEarth.node_tree.nodes.new('ShaderNodeBump')
        bump2.label = "Bump2"
        bump2.inputs[0].default_value = 0.3
        bump2.location = (-500,-700)
        
        #lägger till en Bump som jag namnger Bump3 som ska in i Normal på bump2
        bump3 = materialEarth.node_tree.nodes.new('ShaderNodeBump')
        bump3.label = "Bump3"
        bump3.inputs[0].default_value = 0.7
        bump3.location = (-650,-400)
        
        #lägger till en noise texture 
        noise1 = materialEarth.node_tree.nodes.new('ShaderNodeTexNoise')
        noise1.location = (-1000, -150)
        noise1.inputs[2].default_value = 8 #ändrar värdet på scale på Noise Texturen till 8
        noise1.inputs[3].default_value = 16 #ändrar värdet på detail på Noise Texturen till 16
        
        #lägger till noise texture 2
        noise2 = materialEarth.node_tree.nodes.new('ShaderNodeTexNoise')
        noise2.location = (-1400, -800)
        noise2.inputs[2].default_value = 1 #ändrar värdet på scale på Noise Texturen till 1
        noise2.inputs[3].default_value = 16 #ändrar värdet på detail på Noise Texturen till 16
        
        
        #lägger till Musgrave Texture
        musgrave = materialEarth.node_tree.nodes.new('ShaderNodeTexMusgrave')
        musgrave.location = (-1000, -500)
        musgrave.inputs[2].default_value = 12 #ändrar värdet på scale på Musgrave Texture till 12
        
        #lägger till voronoi texture
        voronoi = materialEarth.node_tree.nodes.new('ShaderNodeTexVoronoi')
        voronoi.location = (-1200, -800)
        voronoi.feature = 'DISTANCE_TO_EDGE' #ändrar andra drop-down menyn från F1 till "Distance to edge"
        voronoi.inputs[2].default_value = 10 #ändrar scale på Voronoi Texture till 10
        
        #lägger till Mapping node
        map = materialEarth.node_tree.nodes.new('ShaderNodeMapping')
        map.location = (-1400, -00)
        
        #lägger till Texture Coordinate node
        texCoord = materialEarth.node_tree.nodes.new('ShaderNodeTexCoord')
        texCoord.location = (-1600, -200)
        
        
        ###Länkar ihop de olika nodes för Earth Material med varandra
        
        link = materialEarth.node_tree.links.new #variabel för förenkling av syntax
        
        link(cRampColor.outputs[0], bsdf.inputs[0]) #länkar Ramp Color Color med Prinsiple BSDF Color
        link(noise1.outputs[0], cRampColor.inputs[0]) #länkar noise texture fac med Color Ramp fac
        link(map.outputs[0], noise1.inputs[0]) #länkar mapping vector med noise texture vector
        link(texCoord.outputs[3], map.inputs[0]) #länkar Texture Cordinate Object med Mapping vector
       
        link(cRampRough.outputs[0], bsdf.inputs[9]) #länkar color ramp color med Principle bsdf roughness
        link(noise1.outputs[0], cRampRough.inputs[0]) #länkar noise texture fac med color ramp fac
        
        link(bump1.outputs[0], bsdf.inputs[22]) #länkar Bump Normal med Principle Bsdf Normal
        link(bump2.outputs[0], bump1.inputs[3]) #länkar Bump Normal med en annan Bump Normal
        link(bump3.outputs[0], bump2.inputs[3]) #länkar Bump Normal med en annan Bump Normal
        link(noise1.outputs[0], bump3.inputs[2]) #länkar Noise Texture fac med en Bump Normal
        
        link(musgrave.outputs[0], bump2.inputs[2]) #länkar Musgrave Height till en Bump Height
        link(map.outputs[0], musgrave.inputs[0]) #länkar Mapping Vector till Musgrave Texture Vector
        
        link(cRampBump.outputs[0], bump1.inputs[2]) #länkar en Color Ramp color med en Bump Height
        link(voronoi.outputs[0], cRampBump.inputs[0]) #länkar en Voronoi Texture Distance med en Color Ramp fac
        link(noise2.outputs[0], voronoi.inputs[0]) #länkar en Noise texture fac med en Voronoi Vector
        link(map.outputs[0], noise2.inputs[0]) #länkar Mapping Vector till en Noise Texture Vector
        
        link(bsdf.outputs[0], materialOutput.inputs[0]) #länkar Principled BSDF med Material Output
       
        
        bpy.context.object.active_material = materialEarth #ger objectet vårt material
        
        
        return {'FINISHED'}
        
       
###########################################################################   

###########################################################################

                                # Lava Element #
                        
#skapar en klass med ett Fire(Lava) material
class shader_fire(bpy.types.Operator):
    bl_label = "Fire Material" #namnet på materialet
    bl_idname = "shader.fire_operator" #namnet som används när vi kallar på denna klass
    
    def execute(self, context):
        
        materialFire = bpy.data.materials.new(name = "Fire") #skapar ett nytt material vid namn Fire
        materialFire.use_nodes = True #denna line gör det möjligt att använda nodes
        
        materialFire.node_tree.nodes.remove(materialFire.node_tree.nodes.get('Principled BSDF')) #tar bort default Principle BSDF node
        materialFire.node_tree.nodes.remove(materialFire.node_tree.nodes.get('Material Output')) #tar bort default Material Output node
         
        
        #lägger till en ny Principled BSDF node:
        bsdf = materialFire.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 500)
        bsdf.inputs[0].default_value = (0, 0.015, 0.015, 1) #ändrar Base Color på Principled Node till en blå-grön-ish färg
        bsdf.inputs[1].default_value = 0.01 #ändrar Subsurface på Principled node
        bsdf.inputs[3].default_value = (0.8, 0.014, 0, 1) #ändrar Subsurface färgen till en röd-orange färg
        bsdf.inputs[9].default_value = 0.86 #ändrar roughness
        bsdf.inputs[19].default_value = (1, 0.002, 0, 1) #ändrar Emission färgen till en röd färg
        bsdf.inputs[20].default_value = 0.01 #ändrar Emission Strenght
        
        #lägget till en ny Material Output node:
        materialOutput = materialFire.node_tree.nodes.new('ShaderNodeOutputMaterial')
        materialOutput.location = (700, 600)
                
        #lägger till en Mix Shader node
        mixShader = materialFire.node_tree.nodes.new('ShaderNodeMixShader')
        mixShader.location = (500, 440)
        
        #lägger till en Color Ramp node:
        cRamp = materialFire.node_tree.nodes.new('ShaderNodeValToRGB')
        cRamp.location = (-302, 800) 
        cRamp.color_ramp.elements[0].position = (0.5) #ändrar placering på första color-stop
        cRamp.color_ramp.elements[1].position = (0.9) #ändrar placering på andra color-stop 
        
        #lägger till en Emission node:
        emission = materialFire.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = (300, 200)
        emission.inputs[0].default_value = (1, 0.028480, 0, 1) #ändrar färg till en orange-röd färg
        emission.inputs[1].default_value = 50 #ändrar strenght till 50
        
        #lägger till en Bump node:
        bump = materialFire.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (-630, 200)
        bump.inputs[1].default_value = 5 #ändrar Distance till 5
        
        #lägger till en noise Texture:
        noise = materialFire.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-900, 470)
        noise.inputs[2].default_value = 5 #ändrar Scale till 5
        noise.inputs[3].default_value = 16 #ändrar Detail till 16
        
        #lägger till en Mapping node:
        map = materialFire.node_tree.nodes.new('ShaderNodeMapping')
        map.location = (-1150, 300)
        
        #lägger till en Texture Coordinate node:
        texCoord = materialFire.node_tree.nodes.new('ShaderNodeTexCoord')
        texCoord.location = (-1350, 520)       
                    
        #länkning av material:      
        link = materialFire.node_tree.links.new #variabel för förenkling
        
       
        link(texCoord.outputs[3], map.inputs[0]) #länkar TextureCoordinate Object till Mapping Vector
        link(map.outputs[0], noise.inputs[0]) #länkar Mapping Vector till NoiseTexture Vector
        link(noise.outputs[1], cRamp.inputs[0]) #länkar NoiseTexture Color till ColorRamp Fac
        link(noise.outputs[1], bump.inputs[2]) #länkar NoiseTexture Color till Bump Height 
        link(cRamp.outputs[0], mixShader.inputs[0]) #länkar ColorRamp Color till MixShader Fac
        
        link(bump.outputs[0], bsdf.inputs[22]) #länkar Bump Normal till Principled Normal
        link(bsdf.outputs[0], mixShader.inputs[1]) #länkar Principled BSDF till MixShader shader(1)
        link(emission.outputs[0], mixShader.inputs[2]) #länkar Emission Emission till MixShader shader(2)
        link(mixShader.outputs[0], materialOutput.inputs[0]) #länkat MixShader Shader till MaterialOutput Surface
        
        
        bpy.context.object.active_material = materialFire #ger objektet materialet som precis skapats
       
                            
        return {'FINISHED'}

########################################################################### 

###########################################################################

                                # Air Element #

#skapar en klass med ett Air (ghost) material
class shader_air(bpy.types.Operator):
    bl_label = "Air Material" #namnet på materialet
    bl_idname = "shader.air_operator" #namnet som används när man ska kalla på denna klass 
    
    def execute(self, context):
        
          
        materialAir = bpy.data.materials.new(name = "Air") #skapar ett nytt material vid namn Air
        materialAir.use_nodes = True #gör det möjligt att använda nodes
        
        materialAir.node_tree.nodes.remove(materialAir.node_tree.nodes.get('Principled BSDF')) #tar bort default Principle BSDF node
        materialAir.node_tree.nodes.remove(materialAir.node_tree.nodes.get('Material Output')) #tar bort default Material Output node
        
        #lägger till en ny Material Output node:
        materialOutput = materialAir.node_tree.nodes.new('ShaderNodeOutputMaterial')
        materialOutput.location = (700, -300) #position
        
        #lägger till en Mix Shader node:  
        shader = materialAir.node_tree.nodes.new('ShaderNodeMixShader')
        shader.location = (500, -300)
        
        #lägger till en MixRGB node, med följande inställningar:
        mixRGB = materialAir.node_tree.nodes.new('ShaderNodeMixRGB')
        mixRGB.location = (300, 100)
        mixRGB.inputs[0].default_value = 0.139 #ändrar Fac till 0.139
        
        #lägger till en Fresnel node, med följande inställningar:
        fresnel1 = materialAir.node_tree.nodes.new('ShaderNodeFresnel')
        fresnel1.location = (100, 200)
        fresnel1.inputs[0].default_value = 1.06 #ändrar IOR till 1.06
        
        #lägger till en Fresnel node:
        fresnel2 = materialAir.node_tree.nodes.new('ShaderNodeFresnel')
        fresnel2.location = (100, 0)
        
        #lägger till en Color Ramp node, med följande inställningar:
        cRamp = materialAir.node_tree.nodes.new('ShaderNodeValToRGB')
        cRamp.location = (-100, 100)
        cRamp.color_ramp.elements[1].position = (0.5) #ändrar positionen på en av Color Stop 
        
        #lägger till en Noise Texture node, med följande inställningar:
        noise = materialAir.node_tree.nodes.new('ShaderNodeTexNoise')
        noise.location = (-300, 0)
        noise.inputs[2].default_value = 65 #ändrar scale till 65
        noise.inputs[3].default_value = 10 #ändrar detail till 10
        
        #lägger till en Mapping node, med följande inställningar:
        map = materialAir.node_tree.nodes.new('ShaderNodeMapping')
        map.location = (-500, -100)
        map.inputs[3].default_value[0] = 0 #ändrar scale x-värde till 0
        map.inputs[3].default_value[1] = 0 #ändrar scale y-värde till 0
        map.inputs[3].default_value[2] = 1 #ändrar scale z-värde till 1
        
        #lägger till en Texture Coordinate node:
        texCoord = materialAir.node_tree.nodes.new('ShaderNodeTexCoord')
        texCoord.location = (-700, -100)
        
        #lägger till en Transparent node:
        transparent = materialAir.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        transparent.location = (100, -300)
        
        #lägger till en Emission node, med följande inställningar:
        emission = materialAir.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = (100, -500)
        emission.inputs[0].default_value = (0.239, 0.9, 1, 1) #ändrar färgen 
        emission.inputs[1].default_value = 8 #ändrar strenght
        
        
        #länkning av alla shaders:
        link = materialAir.node_tree.links.new #variabel för förenkling av syntax
        
        link(shader.outputs[0], materialOutput.inputs[0]) #länkar Mix Shader med Material Output
        link(mixRGB.outputs[0], shader.inputs[0]) #länkar MixRGB med Mix Shader
        link(fresnel1.outputs[0], mixRGB.inputs[1]) #länkar en av Fresnel till MixRGB
        link(fresnel2.outputs[0], mixRGB.inputs[2]) #länkar den andra Fresnel till MixRGB (input 2)
        link(cRamp.outputs[0], fresnel2.inputs[0]) #länkar ColorRamp med en av Fresnel
        link(noise.outputs[1], cRamp.inputs[0]) #länkar Noise Texture med ColorRamp
        link(map.outputs[0], noise.inputs[0]) #länkar Mapping med Noise Texture
        link(texCoord.outputs[0], map.inputs[0]) #länkar Texture Coordinate med Mappin
        
        link(transparent.outputs[0], shader.inputs[1]) #länkar Transparent med Mix Shader
        link(emission.outputs[0], shader.inputs[2]) #länkar Emission med Mix Shader
        
        
        bpy.context.object.active_material = materialAir #ger objectet det skapade materialet
        bpy.context.object.active_material.blend_method = 'BLEND' #aktiverar Alpha Blend under settings i materialet och
                                                                  #.. gör det möjligt att se detta materialet i Evee och inte bara Cycles
        
        return {'FINISHED'}

##########################################################################

                                # Water Element #

#skapar en klass med Water (ocean) material
class shader_water(bpy.types.Operator):
    bl_label = "Water Material" #namnet som kommer synas på "knappen"
    bl_idname = "shader.water_operator" #namnet som används när vi kallar på denna klass
    
    def execute(self, context):
        
        materialWater = bpy.data.materials.new(name = "Water") #skapar ett nytt material vid namn Water
        materialWater.use_nodes = True #gör det möjligt att använda nodes
        
        materialWater.node_tree.nodes.remove(materialWater.node_tree.nodes.get('Principled BSDF')) #tar bort default Principle BSDF node
        materialWater.node_tree.nodes.remove(materialWater.node_tree.nodes.get('Material Output')) #tar bort default Material Output node
        
        #lägger till en ny Material Output node:
        materialOutput = materialWater.node_tree.nodes.new('ShaderNodeOutputMaterial')
        materialOutput.location = (500, 200)
                
        #lägger till en ny Principled BSDF node med följande inställningar:
        bsdf = materialWater.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (200, 100)
        bsdf.inputs[0].default_value = (0.22, 0.53, 0.88, 1) #ändrar till en blå-ish färg
        bsdf.inputs[6].default_value = 0.76 #ändrar metallic värdet
        bsdf.inputs[9].default_value = 0.08 #ändrar roughness värdet
        bsdf.inputs[14].default_value = 0.4 #ändrar clearcoat värdet
        bsdf.inputs[21].default_value = 0.95 #ändrar alpa värdet
        
        #lägger till en Bump node:
        bump =  materialWater.node_tree.nodes.new('ShaderNodeBump')
        bump.location = (0,0)
        
        #lägger till en Musgrave Texture node, med följande inställningar:
        musgrave = materialWater.node_tree.nodes.new('ShaderNodeTexMusgrave')
        musgrave.location = (-200, 100)
        musgrave.inputs[1].default_value = 50 #ändrar scale till 50
        musgrave.inputs[2].default_value = 2 #ändrar detail
        musgrave.inputs[3].default_value = 2.3 #ändrar Dimension
        musgrave.inputs[4].default_value = 0.2 #ändrar Lacunarity
        
        #läggert till en Mapping node, med följande inställningar:
        map = materialWater.node_tree.nodes.new('ShaderNodeMapping')
        map.location = (-400, 0)
        map.inputs[3].default_value[0] = 1.2 #ändrar scale x värde till 1.2
        
        #lägger till en Texture Coordinate:
        texCoord = materialWater.node_tree.nodes.new('ShaderNodeTexCoord')
        texCoord.location = (-600, 0)
        
        #länkning av alla shaders:
        link = materialWater.node_tree.links.new #variabel för förenkling
        
        link(bsdf.outputs[0], materialOutput.inputs[0]) #länkar Principled BSDF med Material Output
        link(bump.outputs[0], bsdf.inputs[22]) #länkar Bump till PrincipledBSDF Normal
        link(musgrave.outputs[0], bump.inputs[2]) #länkar Musgrave till Bump height
        link(map.outputs[0], musgrave.inputs[0]) #länkar Mapping med musgrave
        link(texCoord.outputs[0], map.inputs[0]) #länkar Texture Coordinate med Mapping
        
        bpy.context.object.active_material = materialWater #ger objectet det skapade materialet
        
        return {'FINISHED'}

##########################################################################


#För att registrera klasserna:
#(med andra ord gör så att de syns i 3D View)   

def register():
    bpy.utils.register_class(ElementsPanel)
    bpy.utils.register_class(EarthPanel)
    
    bpy.utils.register_class(shader_earth)
    bpy.utils.register_class(shader_fire)
    bpy.utils.register_class(shader_air)
    bpy.utils.register_class(shader_water)
    
def unregisret():
    bpy.utils.unregister_class(ElementsPanel)
    bpy.utils.unregister_class(EarthPanel)
    
    bpy.utils.unregister_class(shader_earth)
    bpy.utils.unregister_class(shader_fire)
    bpy.utils.unregister_class(shader_air)
    bpy.utils.unregister_class(shader_water)
    
 
if __name__ == "__main__":
    register()
