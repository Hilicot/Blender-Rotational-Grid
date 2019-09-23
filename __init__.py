bl_info = {
    "name": "Rotational grid",
    "author": "Marco Porro",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "VIEW_3D > Tools > Matrix grid",
    "description": "generates a grid of objects with a rotation offset",
    "category": "Object",
    }

import bpy
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

#-------------FUNCTIONS------------------

def createGrid(obj):
    my_props = bpy.context.scene.my_props
    for col in range(my_props.numCol):
        for row in range(my_props.numRow):
            addObj(obj, row, col)

def deleteGrid(obj):
    list = bpy.context.scene["objList_"+obj.name]
    for ob in list:
        bpy.data.objects.remove(ob, do_unlink = True)
    obj.rotation_euler = [0,0,0]
    bpy.context.scene["objList_"+obj.name] = []


def addObj(obj, row, col):
    my_props = bpy.context.scene.my_props
    if (col != 0 or row != 0):
        newObj = obj.copy()
        bpy.context.scene.collection.objects.link(newObj)
        newObj.name = obj.name+"_grid_clone_"+str(row)+"_"+str(col)
        addToList(obj, newObj)
    else:
        newObj = obj
    newObj.rotation_euler = [0,0,0]

    if not my_props.invertAxis:
        newObj.location.x += my_props.colOffset * col
        if my_props.numCol is not 1:
            valueH = (my_props.maxAngleH-my_props.minAngleH)/(my_props.numCol-1)*col+my_props.minAngleH
            selectObj(newObj)
            bpy.ops.transform.rotate(value=-valueH, orient_axis='Z', orient_type='LOCAL')

    newObj.location.z -= my_props.rowOffset * row
    if my_props.numRow is not 1:
        valueV = (my_props.maxAngleV-my_props.minAngleV)/(my_props.numRow-1)*row+my_props.minAngleV
        selectObj(newObj)
        bpy.ops.transform.rotate(value=-valueV, orient_axis='X', orient_type='LOCAL')

    if my_props.invertAxis:
        newObj.location.x += my_props.colOffset * col
        if my_props.numCol is not 1:
            valueH = (my_props.maxAngleH-my_props.minAngleH)/(my_props.numCol-1)*col+my_props.minAngleH
            selectObj(newObj)
            bpy.ops.transform.rotate(value=-valueH, orient_axis='Z', orient_type='LOCAL')
    print(str(row) + " " + str(col) + " " + str(valueH) + " " + str(valueV) + " " )
    selectObj(obj)


def selectObj(obj):
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def addToList(obj, new_obj):
    list = bpy.context.scene["objList_"+obj.name]
    new_list = []
    for ob in list:
        new_list.append(ob)
    new_list.append(new_obj)
    bpy.context.scene["objList_"+obj.name] = new_list


#-------------CLASSES------------------

class OBJECT_OT_createGrid(bpy.types.Operator):
    '''Create the rotational grid of the selected object'''
    bl_idname = "object.create_rotational_grid"
    bl_label = "Create matrix grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        if len(bpy.context.selected_objects) is 0:
            print("error: no object is selected")
            return {'CANCELLED'}
        obj = bpy.context.selected_objects[0]
        if ("objList_"+obj.name) in bpy.context.scene.keys() and len(bpy.context.scene["objList_"+obj.name]) is not 0:
            deleteGrid(obj)
        else:
            bpy.context.scene["objList_"+obj.name] = []

        createGrid(obj)
        return {'FINISHED'}

class OBJECT_OT_updateGrid(bpy.types.Operator):
    '''Update the rotational grid of the selected object'''
    bl_idname = "object.update_rotational_grid"
    bl_label = "Update grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        if len(bpy.context.selected_objects) is 0:
            print("error: no object is selected")
            return {'CANCELLED'}
        obj = bpy.context.selected_objects[0]
        if not (("objList_"+obj.name) in bpy.context.scene.keys()) or len(bpy.context.scene["objList_"+obj.name]) is 0:
            return {'CANCELLED'}
        deleteGrid(obj)

        createGrid(obj)

        return {'FINISHED'}

class OBJECT_OT_deleteGrid(bpy.types.Operator):
    '''Delete the rotational grid of the selected object'''
    bl_idname = "object.delete_rotational_grid"
    bl_label = "Delete grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        if len(bpy.context.selected_objects) is 0:
            print("error: no object is selected")
            return {'CANCELLED'}
        obj = bpy.context.selected_objects[0]
        if not (("objList_"+obj.name) in bpy.context.scene.keys()) or len(bpy.context.scene["objList_"+obj.name]) is 0:
            return {'CANCELLED'}
        deleteGrid(obj)

        return {'FINISHED'}


#-------------------UI-----------------------------------------------------
class MySettings(PropertyGroup):

    numCol : IntProperty(
        name = "Columns",
        description = "the number of columns",
        default = 5,
        min = 1,
        )
    numRow : IntProperty(
        name = "Rows",
        description = "the number of rows",
        default = 5,
        min = 1,
        )
    rowOffset : FloatProperty(
        name = "Offset",
        description = "Row offset",
        default = 5,
        )
    colOffset : FloatProperty(
        name = "Offset",
        description = "Row offset",
        default = 5,
        )
    minAngleH : FloatProperty(
        name = "",
        description = "the minimum angle in a row",
        default = 0,
        subtype = 'ANGLE'
        )
    maxAngleH : FloatProperty(
        name = "",
        description = "the maximum angle in a row",
        default = 3.14,
        subtype = 'ANGLE'
        )
    minAngleV : FloatProperty(
        name = "",
        description = "the minimum angle in a column",
        default = 0,
        subtype = 'ANGLE'
        )
    maxAngleV : FloatProperty(
        name = "",
        description = "the maximum angle in a column",
        default = 3.14,
        subtype = 'ANGLE'
        )
    invertAxis : BoolProperty(
        name = "Invert",
        description = "use local transformation instead of global ones",
        default = False
        )

class PANEL_PT_UIclass(bpy.types.Panel):
    """Creates a Panel in the Tool tab"""
    bl_idname = "OBJECT_PT_matrix_grid_UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Matrix Grid"
    bl_context = "objectmode"
    bl_label = "Matrix Grid"

    @classmethod
    def poll(self,context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.my_props

        #Rows
        layout.label(text = "Rows")
        split = layout.split()
        col = split.column()
        col.prop(rd, "numRow")
        col.prop(rd,"rowOffset")
        col = split.column(align=True)
        col.prop(rd, "minAngleH")
        col.prop(rd, "maxAngleH")
        #column
        layout.label(text = "Columns")
        split = layout.split()
        col = split.column()
        col.prop(rd, "numCol")
        col.prop(rd,"colOffset")
        col = split.column(align=True)
        col.prop(rd, "minAngleV")
        col.prop(rd, "maxAngleV")
        layout.separator
        layout.prop(rd, "invertAxis")
        #operator
        layout.operator("object.create_rotational_grid", text = "Create Grid")
        layout.operator("object.update_rotational_grid", text = "Update Grid")
        layout.operator("object.delete_rotational_grid", text = "Delete Grid")

#-------------REGISTRATION--------------------
classes = (
    OBJECT_OT_createGrid,
    OBJECT_OT_updateGrid,
    OBJECT_OT_deleteGrid,
    PANEL_PT_UIclass,
    MySettings,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_props = PointerProperty(type=MySettings)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_props

if __name__ == "__main__":
    register()
    unregister()
    register()
