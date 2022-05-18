import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import streamlit as st
from PIL import Image

# Global Variables
CONST_COLS=3

# Initalize the states
if "df" not in st.session_state:
    st.session_state.df=df=pd.DataFrame(columns=['Filename','Sorted'])
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'imgs_per_row' not in st.session_state:
    st.session_state.imgs_per_row=None
    
st.title("Super Sniffer")
st.write("Use this app to modify any labels in your dataset.")
st.write("1. Upload the imagery and the corresponding csv file")
st.write("2. For set of images click Save Labels then Next to move to the next 3")

# Upload Widgets
with st.expander("See Upload Options"):
    with st.form("Upload_Form"):
        images_list = st.file_uploader("Choose a jpg file", accept_multiple_files=True)

        uploaded_csv = st.file_uploader("Upload a csv file", type=['csv'],accept_multiple_files=False)
        uploaded = st.form_submit_button("Upload Files")
if uploaded_csv and uploaded:
            st.session_state.df=pd.read_csv(uploaded_csv)


def handle_boxes(*boxes):
    # filename=str(images_list[st.session_state.img_idx].name)
    # old_label=st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"].to_string(index=False)
    # st.write("old_label",old_label)
    #num_boxes =number of boxes passed
    num_boxes=len(boxes)
    if any(boxes):
        for i in range(num_boxes):
            if boxes[i] == True:
                st.write("index",i)
                curr_idx=(st.session_state.img_idx+i)
                filename=str(images_list[curr_idx].name)
                old_label=st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"].to_string(index=False)
                if old_label != None:
                    # st.write("filename",filename)
                    # st.write("old_label",old_label)
                    new_label= "good "if old_label == "bad" else "bad"
                    #     new_label="good"
                    # else:
                    #     new_label="bad"
                    # st.write("new_label",new_label)
                    # st.write(st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"])
                    st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"]=new_label
                    # st.write(st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"])
        # st.write( st.session_state.df)
     
def create_csv():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    st.session_state.df.to_csv().encode('utf-8')
    return st.session_state.df.to_csv().encode('utf-8')

def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return  
 
def next_button(*boxes):
    # Save the data from the checkboxes to the csv file
    handle_boxes(*boxes)
    if -1 < st.session_state.img_idx <= (len(images_list)-1)   :
        st.session_state.img_idx += (CONST_COLS)
        imgs_left= len(images_list) - st.session_state.img_idx
        # not enough images left to populate an entire row
        st.write("imgs_left",imgs_left)
        if CONST_COLS>imgs_left :
            st.session_state.imgs_per_row=imgs_left
        else:
            st.session_state.imgs_per_row=None
    elif st.session_state.img_idx ==(len(images_list)):
        st.success('All images have been sorted!')
    else:
        st.warning(f'No more images to sort {st.session_state.img_idx}/{len(images_list)} ')


def back_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= (CONST_COLS)
        imgs_left= len(images_list) - st.session_state.img_idx
        # not enough images left to populate an entire row
        st.write("imgs_left",imgs_left)
        if CONST_COLS>imgs_left :
            st.session_state.imgs_per_row=imgs_left
        else:
            st.session_state.imgs_per_row=None
    else:
        st.warning('Cannot Undo')



# If no images can be displayed then don't show this form
if images_list!=[] and st.session_state.img_idx < len(images_list) and st.session_state.df.empty ==False and st.session_state.imgs_per_row != 0:
    st.write("Current Index: ",st.session_state.img_idx)
    form = st.form("checkboxes", clear_on_submit=True)
    cols=CONST_COLS
    with form:
        if st.session_state.imgs_per_row != None:
            st.write("imgs per row: ",st.session_state.imgs_per_row)
            cols_boxes=form.columns(st.session_state.imgs_per_row)
            cols=st.session_state.imgs_per_row
        else:
            if len(images_list) <= cols:
                cols_boxes=form.columns(len(images_list))
                cols=len(images_list)
            else:
                 cols_boxes=form.columns(cols)   
        # cols_boxes = form.columns(5), form.columns(5), form.columns(5)
        
        # Make the number of images to display match the checkboxes
        # If not all three images can be displayed this will decreaser to the 
        # number of images that can be displayed.
        # num_images will always be >= 1
        if cols >0:
            st.write("cols",cols)
            if images_list != []:
                for i in range(cols):
                    st.write("cols",cols)
                    # img = Image.open(images_list[st.session_state.img_idx+i])
                    # cols_boxes[i].image(img,width=100)
                labels=[""]*cols
                for i in range(cols):
                    curr_idx=(st.session_state.img_idx+i)
                    filename=str(images_list[curr_idx].name)
                    curr_label=st.session_state.df.loc[st.session_state.df["Filename"]==filename,"Sorted"].to_string(index=False)    
                    labels[i]=curr_label
                boxes = [
                        cols_boxes[j].checkbox(
                            f"r{0}:c{j}{labels[j]}", key=f"{j}", value=False
                        )
                        for j in range(cols)
                    ]
    form.form_submit_button("Save Labels")
    
    if boxes:
        st.button(label="Next",key="next_button",on_click=next_button,args=boxes)
elif st.session_state.df.empty or  images_list == []:
    if st.session_state.df.empty:
        st.write("Please upload a csv file to begin...")
    if images_list == []:
        st.write("Please upload a some imagery to begin...")     
              
if images_list!=[]:
    st.button(label="Back",key="back_button",on_click=back_button)  


    
st.download_button(
    label="Download data as CSV 💻",
    data=create_csv(),
    file_name= create_csv_name(),
    mime='text/csv',
)

    
with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.df)
    st.bar_chart(st.session_state.df['Sorted'].value_counts())