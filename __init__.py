bl_info = {
    "name": "Camera Switcher",
    "description": "Switch between cameras in a scene with Shift+Num 0",
    "author": "Jakub Jaszewski",
    "version": (2, 0),
    "blender": (4, 2, 0),
    "location": "3D Viewport",
    "category": "3D View"
}

import bpy

def get_cameras(scene):
    """
    Get a list of all cameras in the scene
    """
    cameras = []
    for obj in scene.objects:
        if obj.type == 'CAMERA':
            cameras.append(obj)
    return cameras

class CameraSwitcherOperator(bpy.types.Operator):
    """
    Switch between cameras in the scene
    """
    bl_idname = "view3d.camera_switch"
    bl_label = "Camera Switcher"

    @classmethod
    def poll(cls, context):
        """
        Only show the operator in the 3D Viewport when cameras are available
        """
        return len(get_cameras(context.scene)) > 1

    def execute(self, context):
        """
        Cycle through cameras in the scene
        """
        cameras = get_cameras(context.scene)
        active_camera = context.scene.camera

        # Find the index of the active camera in the list of cameras
        try:
            index = cameras.index(active_camera)
        except ValueError:
            index = 0

        # Set the next camera in the list as active
        if index == len(cameras) - 1:
            context.scene.camera = cameras[0]
        else:
            context.scene.camera = cameras[index + 1]

        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(CameraSwitcherOperator)

    # Add keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(CameraSwitcherOperator.bl_idname, 'NUMPAD_0', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(CameraSwitcherOperator)

    # Remove keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()

if __name__ == "__main__":
    register()
