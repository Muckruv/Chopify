bl_info = {
    "name": "Chopify",
    "blender": (3, 0, 0),
    "category": "Animation",
    "author": "Muckruv",
    "version": (1, 0),
    "description": "Chopifies an objects animation.",
}

import bpy

class OBJECT_OT_chopify_animation(bpy.types.Operator):
    """Chopifies an object's animation"""
    bl_idname = "object.chopify_animation"
    bl_label = "Chopify"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj and obj.animation_data and obj.animation_data.action:
            action = obj.animation_data.action
            action.use_fake_user = True  # Preserve original animation

            new_action = action.copy()
            new_action.name = action.name + "_Chopified"
            obj.animation_data.action = new_action

            fcurves = new_action.fcurves
            start_frame = int(new_action.frame_range[0])
            end_frame = int(new_action.frame_range[1])

            for frame in range(start_frame, end_frame + 1):
                for fcurve in fcurves:
                    value = fcurve.evaluate(frame)
                    fcurve.keyframe_points.insert(frame, value, options={'FAST'})

            for fcurve in fcurves:
                keyframe_points = fcurve.keyframe_points
                for i in range(len(keyframe_points) - 1, -1, -1):
                    if i % 2 == 1:
                        keyframe_points.remove(keyframe_points[i])
                for keyframe in keyframe_points:
                    keyframe.interpolation = 'CONSTANT'

            self.report({'INFO'}, f"Chopified animation created: {new_action.name}")

        # Process material node keyframes
        if obj and obj.type == 'MESH':
            for mat in obj.data.materials:
                if mat and mat.node_tree and mat.node_tree.animation_data:
                    fcurves = mat.node_tree.animation_data.action.fcurves if mat.node_tree.animation_data.action else []
                    for fcurve in fcurves:
                        for frame in range(start_frame, end_frame + 1):
                            value = fcurve.evaluate(frame)
                            fcurve.keyframe_points.insert(frame, value, options={'FAST'})

                        keyframe_points = fcurve.keyframe_points
                        for i in range(len(keyframe_points) - 1, -1, -1):
                            if i % 2 == 1:
                                keyframe_points.remove(keyframe_points[i])
                        for keyframe in keyframe_points:
                            keyframe.interpolation = 'CONSTANT'

            self.report({'INFO'}, "Chopified effect applied to node keyframes.")

        return {'FINISHED'}


# UI Panel to add a button in the Object Properties
class OBJECT_PT_chopify_animation_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Chopify Animation"
    bl_idname = "OBJECT_PT_chopify_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Animation Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.chopify_animation")


# Register and Unregister Functions
def register():
    bpy.utils.register_class(OBJECT_OT_chopify_animation)
    bpy.utils.register_class(OBJECT_PT_chopify_animation_panel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_chopify_animation)
    bpy.utils.unregister_class(OBJECT_PT_chopify_animation_panel)


if __name__ == "__main__":
    register()
