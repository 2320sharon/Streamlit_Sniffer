from tkinter import image_names
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime

st.set_page_config(
     page_title="Sniffer",
     page_icon="🐕",
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': "https://github.com/2320sharon/Streamlit_Sniffer",
         'Report a bug': "https://github.com/2320sharon/Streamlit_Sniffer/issues",
         'About': "# Sniffer. Sort your *extremely* cool images!"
     }
 )

def get_percent_blk_pixels(img):
    img_array=np.array(img)
    w,h=img_array.shape[0:2]
    total_pixels=w*h if img_array.ndim<3 else w*h*img_array.shape[2]
    black_count = np.sum(img_array == 0)
    return np.round(black_count/total_pixels,3)


if 'length_images_list' not in st.session_state:
    st.session_state.length_images_list=-1
if 'blk_pxl_dict' not in st.session_state:
    st.session_state.blk_pxl_dict={}
if 'remove_imgs' not in st.session_state:
    st.session_state.remove_imgs=False

def remove_images_button():
    st.session_state.remove_imgs = not st.session_state.remove_imgs

with st.expander("Upload Images",expanded=True):
    uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
    max_blk_percent = st.slider("Percentage of Black Pixels Allowed:", key="upload",step=0.01, value=0.50, min_value=0.0, max_value=1.0)
    st.write("Would you like to remove the images that exceed the maximum percentage of black pixels?")
    st.button(label="Remove Images",key="remove_images",on_click=remove_images_button)
    if st.session_state.remove_imgs == True:
        idx_remove=[]
        for cnt,file in enumerate(uploaded_files):
            img = Image.open(file)
            blk_pixels=get_percent_blk_pixels(img)
            if blk_pixels > max_blk_percent:
                idx_remove.append(cnt)
        for idx in reversed(idx_remove):
             del uploaded_files[idx]
    
    images_list=uploaded_files
                

if st.session_state.length_images_list != len(images_list):
    st.session_state.length_images_list=len(images_list)
    for file in uploaded_files:
        if file.name not in st.session_state.blk_pxl_dict.keys():
            img = Image.open(file)
            blk_pixels=get_percent_blk_pixels(img)
            st.session_state.blk_pxl_dict[file.name]=blk_pixels
            
st.write(st.session_state.blk_pxl_dict)

def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return csv_filename

# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'df' not in st.session_state:
    st.session_state.df=pd.DataFrame(columns=['Filename','Sorted','Index'])


if st.session_state.img_idx > (len(images_list)+2):
    st.session_state.img_idx = (len(images_list)-1) if (len(images_list)-1)>0 else 0


def create_csv():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    st.session_state.df.to_csv().encode('utf-8')
    return st.session_state.df.to_csv().encode('utf-8')


def yes_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1)   :
        if st.session_state.blk_pxl_dict[images_list[st.session_state.img_idx].name] <= blk_percent:
            row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good",'Index':st.session_state.img_idx}
            st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx ==(len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} /{ len(images_list)} ')


def no_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1) :
        if st.session_state.blk_pxl_dict[images_list[st.session_state.img_idx].name] <= blk_percent:
            row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"bad",'Index':st.session_state.img_idx}
            st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == (len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx}/{ len(images_list)}')


def undo_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
        if images_list != [] and st.session_state.img_idx <= (len(images_list)-1) :
            drop_filename=images_list[st.session_state.img_idx].name
            index=st.session_state.df.loc[st.session_state.df['Filename'] == drop_filename].index.values
            st.session_state.df.drop(index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')


st.title("Sniffer🐕")
st.image("./assets/sniffer.jpg")

# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1

try:
    my_bar = st.progress((st.session_state.img_idx)/num_images)
except st.StreamlitAPIException:
    my_bar = st.progress(0)


col1,col2,col3,col4=st.columns(4)
with col1:
    blk_percent = st.slider("Percentage of Black Pixels Allowed:", step=0.01, value=0.50, min_value=0.0, max_value=1.0)
    st.write(blk_percent)
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",key="undo_button",on_click=undo_button)
    
with col2:
    st.write(f"{st.session_state.img_idx} of {num_images}")
    if images_list==[]:
        image= Image.open("./assets/new_loading_sniffer.jpg")
    else:
        # Display done.jpg when all images are sorted 
        if st.session_state.img_idx>=len(images_list):
            image = Image.open("./assets/done.jpg")
            st.image(image,width=300)
        else:
            st.session_state.blk_pxl_dict[images_list[st.session_state.img_idx].name]
            if st.session_state.blk_pxl_dict[images_list[st.session_state.img_idx].name] > blk_percent:
                st.write("This image exceeds the allowed \% black pixels. It will not be sorted.")
            if st.session_state.img_idx>=len(images_list):
                image = Image.open("./assets/done.jpg")
                st.image(image,width=300)
            else:
                # caption is "" when images_list is empty otherwise its image name 
                image = Image.open(images_list[st.session_state.img_idx])
                caption = '' if images_list==[] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
                st.image(image, caption=caption,width=300)
    
with col4:
    st.download_button(
     label="Download data as CSV 💻",
     data=create_csv(),
     file_name= create_csv_name(),
     mime='text/csv',
 )

with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.df)
    st.bar_chart(st.session_state.df['Sorted'].value_counts())
