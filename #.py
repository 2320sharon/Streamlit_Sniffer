import streamlit as st
from PIL import Image
import os, io, glob
import zipfile

def rm_thumbnails():
    try:
        for k in glob.glob('*thumbnail*'):
            os.remove(k)
    except:
        pass

st.set_page_config(
     page_title="Create image thumbnails",
     page_icon="",
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "Resize your images!"
     }
 )

uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
images_list=uploaded_files

# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0

def create_zip():
    with zipfile.ZipFile('resized_images.zip', mode="w") as archive:
        for k in glob.glob("*thumbnail*"):
            archive.write(k)
    
    with open('resized_images.zip','rb') as f:
        g=io.BytesIO(f.read()) 
    os.remove('resized_images.zip')
    rm_thumbnails()
    return g

def do_resize(infile, outfile):
    size = 512, 512
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(outfile, "JPEG")

def resize_button():
    for k in range(len(images_list)):
        infile = images_list[k]
        outfile = os.path.splitext(infile.name)[0] + ".thumbnail"
        do_resize(io.BytesIO(infile.getvalue()), outfile)
        print(outfile)        
        st.session_state.img_idx += 1

# def next_button():
#     if -1 < st.session_state.img_idx < len(images_list)-1:
#         row={"Filename":images_list[st.session_state.img_idx],'Sorted':"bad",'Index':st.session_state.img_idx}
#         st.session_state.img_idx += 1
#     else:
#         st.warning('No more images')

if images_list==[]:
    image= Image.open("./assets/ResizeImages.drawio.png")
else:
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/ResizeImages.drawio.png")
    else:
        image = Image.open(images_list[st.session_state.img_idx])

st.title("ResizeImages")
st.image("./assets/ResizeImages.drawio.png")
# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1
my_bar = st.progress((st.session_state.img_idx)/num_images)

col1,col2,col3,col4=st.columns(4)
with col1:
    st.button(label="Resize",key="resize_button",on_click=resize_button)
    # st.button(label="View next image",key="next_button",on_click=no_button)    
with col2:
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/ResizeImages.drawio.png")
        st.image(image,width=300)
    else:
        # caption is none when images_list is empty otherwise it is the image name 
        caption = '' if images_list==[] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
        st.image(image, caption=caption,width=300)
    
with col4:
    st.download_button(
     label="Download resized imagery",
     data=create_zip(),
     file_name= 'resized_images.zip', 
 )

#