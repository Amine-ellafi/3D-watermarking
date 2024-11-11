import trimesh


def off_to_obj(input_path,output_path):
	# Load the .off file
	mesh = trimesh.load(input_path)

	# Export the mesh as an .obj file
	mesh.export(output_path)



def obj_to_off(input_path,output_path):
	# Load the .obj file
	mesh = trimesh.load(input_path)

	# Export the mesh as an .off file
	mesh.export(output_path)


if __name__=="__main__":
	input_path = "C:/Users/Amine ellafi/OneDrive/Desktop/hybrid/output/new.off"
	output_path = "output/new2.obj"

	off_to_obj(input_path,output_path)



