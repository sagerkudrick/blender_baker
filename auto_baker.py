# bpy.context.selected_objects[0].data.uv_layers.new(name="LightMap")
# is the UV map...now need to select it

import bpy
objs = bpy.context.selected_objects
currentCollection = bpy.context.collection.name
collection_baked = currentCollection + "_baked_material"

print("selected objects collection name: " + currentCollection)
print("collection material file name: " + collection_baked)
for n in objs: 
    bpy.ops.image.new(name = collection_baked, width=1024, height=1024, color=(0.0, 0.0, 0.0, 1.0), 
    alpha=True, generated_type='BLANK', float=False, use_stereo_3d=False, tiled=False)
    material = n.data.materials
    
    print(n)
    lm = n.data.uv_layers.get(collection_baked)
    
    if lm is None:
        n.data.uv_layers.new(name = collection_baked)
        lm = n.data.uv_layers.get(collection_baked)
    
    # if this UV map exists, we select it...we're now editing this
    # specific UV mapping
    if lm is not None: 
        lm.active = True
        print("Active")
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT') # for all faces
        bpy.ops.uv.smart_project(angle_limit=66, island_margin = 0.02, scale_to_bounds = True)
        bpy.ops.object.editmode_toggle()

    for materials_selected in material:
        print(materials_selected)
        
        nodes = bpy.data.materials[materials_selected.name].node_tree.nodes
        node = nodes.new('ShaderNodeTexImage')
        node.location = (100,100)
        node.image = bpy.data.images[collection_baked]
        
        nodes.active = node

    bpy.ops.object.bake(type = "DIFFUSE")
