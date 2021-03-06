import Algorithmia
from Algorithmia.acl import ReadAcl, AclType
from PIL import Image
import io
import os
from os import listdir
from os.path import isfile, join


def test_algorithmia(name):
    apiKey='simXTatsEpxaO+Ehudqy2iC+a/j1'
    client = Algorithmia.client(apiKey)
    imgs_directory = client.dir("data://karimelghazouly/imgs_directory")
    if imgs_directory.exists() is False:
        imgs_directory.create()
    acl = imgs_directory.get_permissions()
    acl.read_acl == AclType.my_algos
    imgs_directory.update_permissions(ReadAcl.private)
    imgs_directory.get_permissions().read_acl == AclType.private
    img="data://karimelghazouly/imgs_directory/"+name
    if client.file(img).exists() is False:
	    client.file(img).putFile("data/"+name)
    input = {
        "image": "data://karimelghazouly/imgs_directory/"+name
    }
    algo = client.algo('deeplearning/ColorfulImageColorization/1.1.13')
    link=algo.pipe(input).result['output']
    last=client.file(link).getBytes()
    image = Image.open(io.BytesIO(last))
    type=name.split('.',1)[1]
    h=len(str(type))+1
    new_name= name[:-h]
    image = image.convert("RGB")
    image.save('data/colored-algorithmia/'+str(new_name)+"out."+str(type))
    image.show()

def test_colorize(name):
        type=name.split('.',1)[1]
        h=len(str(type))+1
        new_name= name[:-h]
        os.system("th colorize.lua data/"+name+" data/colored-siggraph/"+new_name+"out."+type)
        image=Image.open('data/colored-siggraph/'+new_name+"out."+type)
        image = image.convert("RGB")
        image.show()

onlyfiles = [f for f in listdir('data') if isfile(join('data', f))]
for i in onlyfiles:
    print("Testing " + i)
    test_algorithmia(i)
    test_colorize(i)
