import bpy
import random

# Create a doughnut (torus)
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.4, location=(0, 0, 0))

# Select the doughnut object
doughnut = bpy.context.object

# Set the frame range for the animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# Insert keyframe for the initial rotation
doughnut.rotation_euler[0] = 0  # X-axis
doughnut.keyframe_insert(data_path="rotation_euler", frame=1, index=0)

# Insert keyframe for the final rotation (180 degrees)
doughnut.rotation_euler[0] = 3.14159  # 180 degrees in radians
doughnut.keyframe_insert(data_path="rotation_euler", frame=60, index=0)

# Create a new material
material = bpy.data.materials.new(name="RandomColorMaterial")

# Enable 'Use Nodes'
material.use_nodes = True
nodes = material.node_tree.nodes

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add a new Principled BSDF node
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Add a new Material Output node
material_output = nodes.new(type='ShaderNodeOutputMaterial')
material_output.location = (200, 0)

# Link the nodes
material.node_tree.links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])

# Assign a random color to the BSDF node
bsdf.inputs['Base Color'].default_value = (random.random(), random.random(), random.random(), 1)

# Assign the material to the doughnut
if doughnut.data.materials:
    # Assign to first material slot
    doughnut.data.materials[0] = material
else:
    # No slots, add a new one
    doughnut.data.materials.append(material)
