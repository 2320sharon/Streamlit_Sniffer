import streamlit as st
import streamlit.components.v1 as components
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

uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
images_list=uploaded_files


# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'df' not in st.session_state:
    st.session_state.df=pd.DataFrame(columns=['Filename','Sorted','Index'])


uploaded_csv = st.file_uploader("Upload a csv file", type=['csv'],accept_multiple_files=False)
if uploaded_csv != None:
    st.session_state.df=pd.read_csv(uploaded_csv)

    
def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return csv_filename


# img_idx will always be inside images_list
if st.session_state.img_idx > (len(images_list)+2):
    st.session_state.img_idx = (len(images_list)-1) if (len(images_list)-1)>0 else 0


def update_df(**kwargs):
    # st.write(kwargs.get('filename'))
    # st.write(kwargs.get('output'))
    filename=kwargs.get('filename')
    old_label=kwargs.get('output')
    # new_label will get the opposite value of its old value
    new_label= "good"if old_label == "bad" else "good"
    st.write(filename)
    st.write(new_label)
    # Assign the new label to the existing dataframe
    # st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"]=new_label
    st.write(st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"])
    st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"]=new_label
    st.write(st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"])
    st.write(st.session_state.df)
    

def create_img_with_label(index_add:int):
    """Creates an image at the st.session_state.img_idx + index_add
    Args:
        index_add (int): number to be added to st.session_state.img_idx
    """
    if st.session_state.img_idx+index_add < len(images_list):
                image = Image.open(images_list[st.session_state.img_idx+index_add])
                st.image(image,width=100)
                filename=str(images_list[st.session_state.img_idx+index_add].name)
                st.write("filename:",filename)
                output=st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"].to_string(index=False)
                st.write("output:",output)
                index=0 if output=="bad" else 1
                # radio_key=f"radio{index_add}"
                st.radio(label="",options=("bad","good"),index=index,key=f"radio{index_add}",on_change=update_df,kwargs={"output":output,"filename":filename})
                # Assign the new label to the existing dataframe
                # st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"]=new_label
                    

def create_csv():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    st.session_state.df.to_csv().encode('utf-8')
    return st.session_state.df.to_csv().encode('utf-8')

def yes_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1)   :
        # row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good",'Index':st.session_state.img_idx}
        # st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx ==(len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort {st.session_state.img_idx}/{len(images_list)} ')


def no_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1) :
        # row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"bad",'Index':st.session_state.img_idx}
        # st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == (len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort {st.session_state.img_idx}/{len(images_list)}')


def undo_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
    else:
        st.warning('Cannot Undo')


if images_list==[]:
    image= Image.open("./assets/new_loading_sniffer.jpg")

st.title("Sniffer🐕")

# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1

try:
    my_bar = st.progress((st.session_state.img_idx)/num_images)
except st.StreamlitAPIException:
    my_bar = st.progress(0)

col1,col2,col3,col4,col5,col6=st.columns(6)
with col1:
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",key="undo_button",on_click=undo_button)
    
with col2:
    st.write(f"{st.session_state.img_idx} of {num_images}")
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image,width=300)
    else:
        if images_list != []:
            if st.session_state.img_idx < len(images_list):
                create_img_with_label(0)
                # image = Image.open(images_list[st.session_state.img_idx])
                # st.image(image,width=100)
                filename=str(images_list[st.session_state.img_idx].name)
                output=st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"].to_string(index=False)
                # st.write(output)
                # index=0 if output=="bad"else 1
                # new_label=st.radio(label="",options=("bad","good"),index=index)
                # st.write(new_label)
                # st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"]=new_label
                create_img_with_label(1)
                create_img_with_label(2)
                # image3 = Image.open(images_list[st.session_state.img_idx+2])
                # st.image(image3,width=100)

with col4:
    st.write(f"{st.session_state.img_idx} of {num_images}")
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image,width=300)
    else:
        if images_list != []:
            image = Image.open(images_list[st.session_state.img_idx+3])
            st.image(image,width=100)
            image2 = Image.open(images_list[st.session_state.img_idx+4])
            st.image(image2,width=100)
            image3 = Image.open(images_list[st.session_state.img_idx+5])
            st.image(image3,width=100)
        
with col6:
    st.download_button(
     label="Download data as CSV 💻",
     data=create_csv(),
     file_name= create_csv_name(),
     mime='text/csv',
 )

with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.df)
    st.bar_chart(st.session_state.df['Sorted'].value_counts())
